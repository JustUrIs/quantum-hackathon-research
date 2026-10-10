"""Verify a failed backend is never silently replaced by a successful fallback."""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
out = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for slug in ("lost-signal", "qday-clock", "order"):
        page = b.new_page()
        requests = []

        def reject(route):
            requests.append(route.request.url)
            route.fulfill(
                status=503,
                content_type="application/json",
                body='{"error":"Injected provider outage"}',
            )

        page.route("**/api/backend_run", reject)
        page.goto(f"http://127.0.0.1:8766/{slug}/")
        page.wait_for_function(
            "document.getElementById('status').textContent.startsWith('Local model ready')"
        )
        page.locator("#runBackend").click()
        page.wait_for_function(
            "document.getElementById('auditStatus').textContent.includes('Injected provider outage')"
        )
        assert page.locator("#runBackend").is_disabled()
        page.locator("#export").click()
        d = json.loads(page.locator("#exportOutput").input_value())
        assert d["backend_evidence"] is None and d["local_model"] is not None
        assert len(requests) == 1
        out.append(
            {
                "project": slug,
                "failure_shown": True,
                "backend_evidence": None,
                "submissions": len(requests),
            }
        )
        page.close()
    b.close()
(ROOT / "artifacts/ui-failure-results.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("Backend-failure checks passed for all three projects.")
