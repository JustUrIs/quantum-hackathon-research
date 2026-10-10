"""Local dev harness (not used on Qollab). Serves the project and bridges JS -> impostor.service
over HTTP, with qiskit's BasicSimulator standing in for Qollab's injected `backend`.
Run from the project root:  python dev/server.py  then open http://localhost:8765/dev/harness.html"""
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import os
os.chdir(ROOT)

from qiskit.providers.basic_provider import BasicSimulator  # noqa: E402
from impostor import service  # noqa: E402

_circuits = {}


class H(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        name = self.path.rsplit("/", 1)[-1]
        try:
            if name == "audit_circuit":
                qc = service.audit_circuit()
                _circuits["audit"] = qc
                out = json.dumps({"num_qubits": qc.num_qubits})
            elif name == "backend_run":
                counts = BasicSimulator().run(_circuits["audit"], shots=body["shots"]).result().get_counts()
                out = json.dumps(counts)
            else:
                out = getattr(service, name)(*body["args"])
            data, code = str(out).encode(), 200
        except Exception as e:  # surface errors to the page
            data, code = json.dumps({"error": repr(e)}).encode(), 500
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
