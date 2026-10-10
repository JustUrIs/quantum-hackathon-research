"""Browser integration tests against the isolated local development server."""

import json
from pathlib import Path
import argparse
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts"
OUT.mkdir(exist_ok=True)
ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=8766)
args = ap.parse_args()
results = []


def ready(page):
    page.wait_for_function(
        "document.getElementById('status').textContent.startsWith('Local model ready')",
        timeout=120000,
    )


def slider(page, id, value):
    page.locator("#" + id).fill(str(value))
    page.locator("#" + id).dispatch_event("input")
    ready(page)


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug in ("lost-signal", "qday-clock", "order"):
        page = browser.new_page(
            viewport={"width": 1440, "height": 1050}, device_scale_factor=1
        )
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"http://127.0.0.1:{args.port}/{slug}/")
        ready(page)
        if slug == "lost-signal":
            page.wait_for_function(
                "document.getElementById('birdStatus').textContent.includes('directional contrast')"
            )
            page.locator("#gps").click()
            assert page.locator("#gpsLabel").inner_text() == "GPS signal lost"
            assert float(page.locator("#gain").inner_text().replace("×", "")) > 1
            page.locator("#breakSensor").click()
            ready(page)
            assert float(page.locator("#gain").inner_text().replace("×", "")) < 1
            page.locator("#isotropic").click()
            page.wait_for_function(
                "document.getElementById('birdStatus').textContent.includes('Isotropic coupling')"
            )
            slider(page, "noise", 0.08)
        elif slug == "qday-clock":
            assert page.locator("#genuineQ").inner_text() == "10"
            for n in ("21", "33", "35", "15"):
                page.locator("#modulus").select_option(n)
                ready(page)
                assert (
                    "Classical trial division finds"
                    in page.locator("#trialDivision").inner_text()
                )
            page.locator("#randomize").click()
            ready(page)
            assert page.locator("#mixtureValue").inner_text() == "100.0%"
            page.locator("#randomize").click()
            ready(page)
            page.locator("#scenarioPreset").click()
            assert "confidentiality gap" in page.locator("#clockVerdict").inner_text()
        else:
            before = page.locator("#headline").inner_text()
            page.locator("#swap").click()
            assert before != page.locator("#headline").inner_text()
            assert page.locator("#qq").inner_text() == "0.0000"
            page.locator("#breakQQ").click()
            ready(page)
            assert abs(float(page.locator("#qq").inner_text())) > 0.1
            page.locator("#classical").click()
            assert (
                "classical model matches"
                in page.locator("#classicalResult").inner_text()
            )
            page.locator("#poll").select_option("rose-jackson")
            assert page.locator("#pollQQ").inner_text() == "0.1514"
            slider(page, "information", 0)
            page.locator("#auditStudy").click()
            page.wait_for_function(
                "document.getElementById('studyResult').textContent.includes('500 AB responses')"
            )
            page.locator("#studyCounts").fill("-1,0,0,0\n1,2,3,4")
            page.locator("#auditStudy").click()
            assert "Could not audit" in page.locator("#studyResult").inner_text()
            page.locator("#studyCounts").fill("250,50,100,100\n280,30,120,70")
            page.locator("#auditStudy").click()
            page.wait_for_function(
                "document.getElementById('studyResult').textContent.includes('500 AB responses')"
            )
        # All projects run one real BasicSimulator job and retain snapshot evidence.
        page.locator("#runBackend").click()
        page.wait_for_function(
            "document.getElementById('auditStatus').textContent.startsWith('Completed')",
            timeout=120000,
        )
        evidence = json.loads(page.locator("#auditOutput").inner_text())
        assert evidence["report"]["shots"] == 1024
        assert page.locator("#runBackend").is_disabled()
        (OUT / f"{slug}-local-backend.json").write_text(
            json.dumps(evidence, indent=2), encoding="utf-8"
        )
        page.locator("#export").click()
        export = json.loads(page.locator("#exportOutput").input_value())
        assert export["backend_evidence"]
        if slug == "order":
            assert "questionnaire_audit" in export["additional_experiments"]
        if slug == "qday-clock":
            assert (
                export["additional_experiments"]["planning_scenario"]["forecast"]
                is False
            )
        page.locator("#exportDetails").evaluate("(e)=>e.open=false")
        page.locator("#auditDetails").evaluate("(e)=>e.open=false")
        page.locator("h1").click()
        page.evaluate("window.scrollTo(0,0)")
        page.screenshot(path=str(OUT / f"{slug}-desktop.png"), full_page=True)
        for width in (390, 768):
            page.set_viewport_size({"width": width, "height": 844})
            if not page.evaluate(
                "document.documentElement.scrollWidth<=window.innerWidth+1"
            ):
                print(
                    page.evaluate(
                        "Array.from(document.querySelectorAll('*')).filter(e=>e.getBoundingClientRect().right>window.innerWidth+1).map(e=>[e.tagName,e.id,typeof e.className==='string'?e.className:'svg',e.getBoundingClientRect().width]).slice(0,20)"
                    ),
                    flush=True,
                )
                page.screenshot(path=str(OUT / f"{slug}-overflow.png"), full_page=True)
                raise AssertionError(f"{slug} overflows at {width}")
            if width == 390:
                page.screenshot(path=str(OUT / f"{slug}-mobile.png"), full_page=True)
        page.emulate_media(reduced_motion="reduce")
        # UI must remain keyboard operable, with named controls.
        assert page.locator("button").evaluate_all(
            '(xs)=>xs.every(x=>x.textContent.trim() || x.getAttribute("aria-label"))'
        )
        assert not errors, errors
        results.append(
            {
                "project": slug,
                "status": "passed",
                "backend": evidence["backend"],
                "shots": 1024,
                "viewports": [1440, 768, 390],
                "console_errors": errors,
            }
        )
        print(slug, "PASS", flush=True)
        page.close()
    browser.close()
(OUT / "ui-results.json").write_text(
    json.dumps(results, indent=2) + "\n", encoding="utf-8"
)
