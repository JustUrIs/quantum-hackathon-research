"""Numerical parity and user-flow checks for the static public reference site.

Starts its own localhost HTTP server; no QPU jobs, external navigation or auth.
"""

import functools
import json
import math
import os
import random
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
for folder in ("lost-signal-qollab", "order-qollab"):
    sys.path.insert(0, str(ROOT / folder))
from lostsignal import service as lost
from orderlab import service as order


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(
    ("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT / "docs"))
)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}"
records = []


def call(page, method, p):
    return page.evaluate(
        'async ([name,p])=>JSON.parse(await (await import("./preview-adapter.js"))[name].callPromising(JSON.stringify(p)))',
        [method, p],
    )


def close(actual, expected, tol=1e-10):
    if isinstance(expected, list):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            close(a, e, tol)
    elif isinstance(expected, dict):
        for k, v in expected.items():
            if k in ("origin",):
                continue
            close(actual[k], v, tol)
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
            actual,
            expected,
        )
    else:
        assert actual == expected, (actual, expected)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    page.goto(base)
    assert page.locator(".project").count() == 3
    page.screenshot(path=str(ROOT / "artifacts/preview-hub.png"), full_page=True)
    rng = random.Random(42)
    for slug in ("lost-signal", "qday-clock", "order"):
        errors = []

        def capture_error(error, collected=errors):
            collected.append(str(error))

        page.on("pageerror", capture_error)
        page.goto(base + "/" + slug + "/")
        page.wait_for_function(
            "document.getElementById('status').textContent.startsWith('Local model ready')"
        )
        assert page.locator("#runBackend").is_disabled()
        assert "no live Qiskit" in page.locator(".preview-banner").inner_text()
        cases = 0
        if slug == "lost-signal":
            old = Path.cwd()
            os.chdir(ROOT / "lost-signal-qollab")
            for n in range(1, 7):
                for eta in (0, 0.08, 0.3, 0.8):
                    opts = {"n": n, "eta": eta, "shots": 256}
                    close(
                        call(page, "evaluate", opts),
                        json.loads(lost.evaluate(json.dumps(opts))),
                    )
                    cases += 1
            os.chdir(old)
            for a in (0, 1):
                opts = {"field_ut": 26, "anisotropy": a}
                close(
                    call(page, "radical", opts),
                    json.loads(lost.radical(json.dumps(opts))),
                )
                cases += 1
            page.locator("#gps").click()
            assert "lost" in page.locator("#gpsLabel").inner_text()
        elif slug == "order":
            old = Path.cwd()
            os.chdir(ROOT / "order-qollab")
            angles = [(35, 70, 0), (0, 0, 0), (180, 180, 180), (35, 70, 65)] + [
                (rng.randrange(181), rng.randrange(181), rng.randrange(181))
                for _ in range(20)
            ]
            for theta, angle, info in angles:
                opts = {"theta": theta, "angle": angle, "info": info}
                close(
                    call(page, "evaluate", opts),
                    json.loads(order.evaluate(json.dumps(opts))),
                )
                cases += 1
            os.chdir(old)
            for _ in range(12):
                opts = {
                    "ab": [rng.randrange(1, 300) for _ in range(4)],
                    "ba": [rng.randrange(1, 300) for _ in range(4)],
                }
                close(
                    call(page, "audit_counts", opts),
                    json.loads(order.audit_counts(json.dumps(opts))),
                    2e-7,
                )
                cases += 1
            page.locator("#auditStudy").click()
            assert "500 AB responses" in page.locator("#studyResult").inner_text()
            page.locator("#classical").click()
            assert "model matches" in page.locator("#classicalResult").inner_text()
        else:
            fixture = page.evaluate(
                'async()=> (await import("./fixtures.js")).fixtures'
            )
            for key, expected in fixture["experiments"].items():
                n, a, bits = map(int, key.split(":"))
                close(
                    call(page, "evaluate", {"n": n, "a": a, "bits": bits, "mix": 0}),
                    expected,
                )
                cases += 1
                d = call(page, "evaluate", {"n": n, "a": a, "bits": bits, "mix": 1})
                close(d["display_success"], expected["random_phase_success"])
                cases += 1
            page.locator("#modulus").select_option("33")
            page.wait_for_function(
                "document.getElementById('histogramNote').textContent.includes('legitimate algorithmic failure')"
            )
            page.locator("#base").select_option("5")
            page.wait_for_function(
                "!document.getElementById('histogramNote').textContent.includes('legitimate algorithmic failure')"
            )
        page.locator("#export").click()
        export = json.loads(page.locator("#exportOutput").input_value())
        assert export["backend_evidence"] is None
        assert "preview" in export["local_model"]["origin"]
        page.locator("#exportDetails").evaluate("(e)=>e.open=false")
        for width in (390, 768, 1440):
            page.set_viewport_size({"width": width, "height": 950})
            assert page.evaluate(
                "document.documentElement.scrollWidth<=innerWidth+1"
            ), (slug, width)
        assert not errors, errors
        page.remove_listener("pageerror", capture_error)
        records.append(
            {
                "project": slug,
                "numerical_cases": cases,
                "status": "passed",
                "live_backend_disabled": True,
                "export_labels_source": True,
                "widths": [390, 768, 1440],
            }
        )
        print(slug, cases, "reference parity cases passed", flush=True)
    browser.close()
server.shutdown()
(ROOT / "artifacts/preview-results.json").write_text(
    json.dumps(records, indent=2) + "\n", encoding="utf-8"
)
