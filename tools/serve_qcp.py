"""Local Qiskit development harness, bound to localhost. No arbitrary user exec."""
import argparse
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "qcp-qollab"
sys.path.insert(0, str(ROOT))
from qcp.service import evaluate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8771)
    parser.add_argument("--browser", action="store_true", help="Use browser worker instead of local Qiskit")
    args = parser.parse_args()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ROOT), **kw)

        def log_message(self, *a): pass

        def do_GET(self):
            if not args.browser and self.path.split('?')[0] in ('/', '/index.html'):
                html = (ROOT/'index.html').read_text(encoding='utf-8').replace('src="./main.js"','src="./qollab-main.js"')
                self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(html.encode())
            elif not args.browser and self.path.split('?')[0] == '/qollab-main.js':
                js = (ROOT/'qollab-main.js').read_text(encoding='utf-8').replace("import * as judge from 'qcp.service';", "const judge={catalog:{callPromising:async()=>await(await fetch('./catalog.json')).text()},evaluate:{callPromising: async (payload)=>{const r=await fetch('/api/judge',{method:'POST',headers:{'Content-Type':'application/json'},body:payload});if(!r.ok)throw Error('Judge request failed');return await r.text();}}};").replace("'Qollab · Qiskit Statevector'", "'Local harness · Qiskit Statevector'")
                self.send_response(200);self.send_header('Content-Type','text/javascript; charset=utf-8');self.end_headers();self.wfile.write(js.encode())
            else: super().do_GET()

        def do_POST(self):
            if self.path != '/api/judge': self.send_error(404);return
            length = int(self.headers.get('Content-Length',0))
            if length > 40000: self.send_error(413);return
            try:
                result=evaluate(self.rfile.read(length).decode())
                self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(result.encode())
            except Exception as exc:
                self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps({'error':str(exc)}).encode())

    print(f"QCP Arena: http://127.0.0.1:{args.port} ({'browser' if args.browser else 'Qiskit harness'})",flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()


if __name__ == '__main__': main()
