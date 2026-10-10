"""Drive the dev harness in headless Chromium: play every level, toggle sources, screenshot."""
import sys
from playwright.sync_api import sync_playwright

OUT = "../shots"
errors = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1100, "height": 900})
    pg.on("console", lambda m: print("console:", m.text[:200]))
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto("http://localhost:8765/dev/harness.html")
    pg.wait_for_selector("#auditTable:not([hidden])", timeout=60000)
    print("AUDIT:", pg.inner_text("#auditStatus"), "|", pg.inner_text("#auditTable").replace("\n", " "))
    pg.screenshot(path=f"{OUT}/01_top.png")
    # level 1
    pg.click("#chshMany"); pg.wait_for_timeout(1500)
    print("CHSH you/q:", pg.inner_text("#chshYou"), pg.inner_text("#chshQ"), "|", pg.inner_text("#chshVerdict"))
    pg.click("#chshBot"); print("CHSH bot:", pg.inner_text("#chshVerdict"))
    pg.locator("#lv-chsh").screenshot(path=f"{OUT}/02_chsh.png")
    # urandom
    pg.click('#source [data-source="urandom"]'); pg.click("#chshMany"); pg.wait_for_timeout(1500)
    print("CHSH urandom q:", pg.inner_text("#chshQ"), "|", pg.inner_text("#chshVerdict"))
    pg.click('#source [data-source="audit"]'); pg.click("#chshMany"); pg.wait_for_timeout(1500)
    print("CHSH audit q:", pg.inner_text("#chshQ"), "|", pg.inner_text("#chshLast").splitlines()[-1])
    pg.click('#source [data-source="exact"]')
    # level 2
    pg.click("#tab-magic"); pg.click("#magicMany"); pg.wait_for_timeout(2500)
    print("MAGIC you/q:", pg.inner_text("#magicYou"), pg.inner_text("#magicQ"), "|", pg.inner_text("#magicConflicts"))
    pg.click("#magicBot"); pg.click("#magicMany"); pg.wait_for_timeout(2500)
    print("MAGIC after bot you/q:", pg.inner_text("#magicYou"), pg.inner_text("#magicQ"), "|", pg.inner_text("#magicVerdict"))
    pg.locator("#lv-magic").screenshot(path=f"{OUT}/03_magic.png")
    # level 3
    pg.click("#tab-zip"); pg.wait_for_function("document.querySelector('#zipChart').innerHTML.length > 100", timeout=120000)
    pg.fill("#zipK", "5"); pg.dispatch_event("#zipK", "input"); pg.click("#zipRun")
    print("ZIP n=8:", pg.inner_text("#zipYou"), pg.inner_text("#zipQ"), "|", pg.inner_text("#zipVerdict"))
    pg.select_option("#zipN", "12"); pg.wait_for_timeout(2000); pg.click("#zipRun")
    print("ZIP n=12:", pg.inner_text("#zipYou"), pg.inner_text("#zipQ"), "|", pg.inner_text("#zipVerdict"))
    pg.locator("#lv-zip").screenshot(path=f"{OUT}/04_zip.png")
    # mobile
    m = b.new_page(viewport={"width": 390, "height": 844})
    m.goto("http://localhost:8765/dev/harness.html"); m.wait_for_timeout(4000)
    m.screenshot(path=f"{OUT}/05_mobile.png", full_page=False)
    b.close()
print("PAGE ERRORS:", errors or "none")
sys.exit(1 if errors else 0)
