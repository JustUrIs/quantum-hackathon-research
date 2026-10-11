"""Local harness for the standalone Qollab projects.

python tools/serve.py --port 8766
HTTP RPC is development-only. Qollab uses its Python bridge, not this server.
Bound to localhost; functions explicitly allowlisted; project workers isolate cwd.
"""

import argparse
import json
import mimetypes
import multiprocessing as mp
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    "ambulancias": ("ambulancias-qollab", "ambulancia.engine"),
    "darkroom": ("darkroom-qollab", "darkroom.engine"),
    "lost-signal": ("lost-signal-qollab", "lostsignal.service"),
    "qday-clock": ("qday-clock-qollab", "qday.service"),
    "order": ("order-qollab", "orderlab.service"),
}


def worker(conn, folder, module):
    import sys, importlib

    sys.path.insert(0, str(ROOT / folder))
    os.chdir(ROOT / folder)
    service = importlib.import_module(module)
    from qiskit.providers.basic_provider import BasicSimulator

    circuit = None
    while True:
        name, args = conn.recv()
        try:
            if name == "audit_circuit":
                circuit = service.audit_circuit(*args)
                out = json.dumps({"num_qubits": circuit.num_qubits})
            elif name == "backend_run":
                if circuit is None:
                    raise ValueError("Build a circuit first")
                out = json.dumps(
                    BasicSimulator()
                    .run(circuit, shots=int(args[0]), seed_simulator=91)
                    .result()
                    .get_counts()
                )
            elif name in ("evaluate", "radical", "ingest_audit", "audit_counts", "local_audit"):
                out = getattr(service, name)(*args)
            else:
                raise ValueError("Unknown method")
            conn.send((200, out))
        except Exception as exc:
            conn.send((400, json.dumps({"error": str(exc)})))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8766)
    opts = ap.parse_args()
    workers = {}
    for slug, (folder, module) in PROJECTS.items():
        parent, child = mp.Pipe()
        proc = mp.Process(target=worker, args=(child, folder, module), daemon=True)
        proc.start()
        workers[slug] = (parent, threading.Lock())

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, data, mime="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data.encode() if isinstance(data, str) else data)

        def do_POST(self):
            try:
                parts = urlparse(self.path).path.strip("/").split("/")
                slug, _, method = parts
                if parts[1] != "api":
                    raise ValueError("Invalid path")
                body = json.loads(
                    self.rfile.read(int(self.headers.get("Content-Length", 0)))
                )
                pipe, lock = workers[slug]
                with lock:
                    pipe.send((method, body.get("args", [])))
                    code, out = pipe.recv()
                self.send(code, out)
            except Exception as exc:
                self.send(400, json.dumps({"error": str(exc)}))

        def do_GET(self):
            path = unquote(urlparse(self.path).path)
            if path == "/":
                self.send(
                    200,
                    "<title>Quantum experiments</title><h1>Choose an experiment</h1>"
                    + "".join(f'<p><a href="/{s}/">{s}</a></p>' for s in PROJECTS),
                    "text/html",
                )
                return
            slug, *rest = path.strip("/").split("/")
            if slug not in PROJECTS:
                self.send(404, "Not found", "text/plain")
                return
            folder, module = PROJECTS[slug]
            base = ROOT / folder
            if not rest or rest == [""]:
                body = (base / "index.html").read_text(encoding="utf-8")
                html = body if "<!doctype html>" in body.lower() else f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{slug}</title><link rel="stylesheet" href="/{slug}/main.css"><body>{body}<script type="module" src="/{slug}/main.js"></script></body></html>'
                self.send(200, html, "text/html")
                return
            if rest == ["bridge.js"]:
                shim = (
                    (ROOT / "tools/bridge.js")
                    .read_text(encoding="utf-8")
                    .replace("__SLUG__", slug)
                )
                self.send(200, shim, "text/javascript")
                return
            target = (base / "/".join(rest)).resolve()
            if not target.is_relative_to(base.resolve()) or not target.is_file():
                self.send(404, "Not found", "text/plain")
                return
            if target.name == "main.js":
                js = (
                    target.read_text(encoding="utf-8")
                    .replace(f"'{module}'", "'./bridge.js'")
                    .replace(f'"{module}"', '"./bridge.js"')
                )
                self.send(200, js, "text/javascript")
            else:
                self.send(
                    200,
                    target.read_bytes(),
                    mimetypes.guess_type(str(target))[0] or "application/octet-stream",
                )

    print(f"Local projects: http://127.0.0.1:{opts.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", opts.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
