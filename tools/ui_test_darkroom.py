"""Exercise the lesson and an unreachable selected backend without IonQ calls."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=8766)
args = ap.parse_args()
root = Path(__file__).resolve().parents[1]
for asset in ("lesson.js", "lesson.css"):
    assert (root / "darkroom-qollab" / asset).read_bytes() == (root / "darkroom-vercel" / asset).read_bytes()


def lesson(page):
    page.get_by_role("button", name="Español", exact=True).click()
    page.locator("#lessonNext").click()
    page.locator("#lessonNext").click()
    for _ in range(2):
        page.locator("#lessonAdvance").click()
    assert "D1 = 100%; D0 = 0%" in page.locator(".lesson-trace-result").inner_text()
    page.locator("#lessonNext").click()
    for _ in range(2):
        page.locator("#lessonAdvance").click()
    assert "D0 = 25%" in page.locator(".lesson-trace-result").inner_text()
    page.locator("#lessonNext").click()
    page.locator("#lessonNext").click()
    page.locator("#lessonGrade").click()
    assert "cuatro preguntas" in page.locator("#lessonScore").inner_text()
    for i, choice in enumerate((1, 1, 1, 2)):
        page.locator(f'input[name="lesson-q{i}"][value="{choice}"]').check()
    page.locator("#lessonGrade").click()
    assert "4/4" in page.locator("#lessonScore").inner_text()
    page.get_by_role("button", name="English", exact=True).click()
    assert "Correct concepts: 4/4" in page.locator("#lessonScore").inner_text()


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"http://127.0.0.1:{args.port}/darkroom/")
    page.wait_for_function("document.querySelector('#status').textContent.includes('Model checked')")
    lesson(page)
    # Model the reported browser/provider failure; never contact IonQ in tests.
    page.evaluate("globalThis.backend = {name: 'ionq_simulator', run: async () => {throw new Error('Failed to fetch')}}")
    page.locator("#runBackend").click()
    page.wait_for_function("document.querySelector('#auditStatus').textContent.includes('could not be reached')")
    assert page.locator("#errorDetails").is_visible()
    assert not page.locator("#runLocal").is_disabled()
    page.locator("#runLocal").click()
    page.wait_for_function("document.querySelector('#auditOutput').textContent.includes('local_qiskit_simulation')")
    report = json.loads(page.locator("#auditOutput").text_content())
    assert report["shots"] == 1024
    assert report["source"]["network_used"] is False
    assert report["source"]["quantum_hardware"] is False
    page.locator("#cycles").fill("6")
    page.locator("#cycles").dispatch_event("input")
    page.wait_for_function("document.querySelector('#cyclesValue').textContent === '6'")
    assert "2 cycles" in page.locator("#auditStatus").inner_text()
    page.locator("#runLocal").click()
    page.wait_for_function("JSON.parse(document.querySelector('#auditOutput').textContent).config.cycles === 6")
    page.set_viewport_size({"width": 390, "height": 844})
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert not errors, errors
    page.screenshot(path=str(root / "artifacts/darkroom-lesson-mobile.png"), full_page=True)

    preview = browser.new_page(viewport={"width": 1280, "height": 900})
    preview.goto((root / "darkroom-vercel/index.html").as_uri())
    preview.wait_for_function("document.querySelector('#status').textContent.includes('Analytic companion ready')")
    lesson(preview)
    preview.get_by_role("button", name="Español", exact=True).click()
    for _ in range(3):
        preview.locator("#lessonPrevious").click()
    preview.locator("#lessonAdvance").click()
    preview.locator("#lessonAdvance").click()
    preview.locator("#lesson").scroll_into_view_if_needed()
    preview.screenshot(path=str(root / "artifacts/darkroom-lesson-desktop.png"))
    browser.close()
    print("Lesson ES/EN, all four concepts, snapshot labels, local measurements, selected-backend failure and mobile layout: passed.")
