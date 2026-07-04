"""Smoke + basic a11y checks for the Abraxor site."""
import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8095/"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.goto(URL, wait_until="networkidle", timeout=30000)

    checks = {
        "title": "Abraxor" in pg.title(),
        "h1 count == 1": pg.locator("h1").count() == 1,
        "skip link": pg.locator("a.skip-link").count() == 1,
        "landmarks": all(pg.locator(s).count() >= 1 for s in ["header", "main", "footer", "nav"]),
        "3 case studies": pg.locator("article.case").count() == 3,
        "spdr": "SPDR" in pg.content(),
        "UN DESA": "Economic and Social Affairs" in pg.content(),
        "HMRC": "HMRC" in pg.content(),
        "WCAG AAA": "WCAG AAA" in pg.content(),
        "contact mailto": pg.locator("a[href='mailto:hello@abraxor.com']").count() >= 1,
        "html lang": pg.locator("html[lang='en']").count() == 1,
        "images have alt": all(pg.locator("img").nth(i).get_attribute("alt") is not None
                               for i in range(pg.locator("img").count())),
        "no console errors": not errors,
        "css applied": pg.evaluate("() => getComputedStyle(document.querySelector('.stats')).backgroundColor") == "rgb(16, 29, 51)",
    }
    # keyboard: first Tab focuses skip link
    pg.keyboard.press("Tab")
    checks["tab -> skip link"] = pg.evaluate("() => document.activeElement.className") == "skip-link"

    pg.screenshot(path="/tmp/claude-1000/-home-wasim-projects-migrate-off-dreamhost/d7e74d43-01d9-4817-b694-c42547dc9b4f/scratchpad/abraxor_site.png", full_page=True)
    mobile = b.new_page(viewport={"width": 390, "height": 844})
    mobile.goto(URL, wait_until="networkidle")
    checks["no horiz scroll (mobile)"] = mobile.evaluate("() => document.documentElement.scrollWidth <= 390")
    mobile.screenshot(path="/tmp/claude-1000/-home-wasim-projects-migrate-off-dreamhost/d7e74d43-01d9-4817-b694-c42547dc9b4f/scratchpad/abraxor_site_mobile.png", full_page=True)

    ok = True
    for name, passed in checks.items():
        print(("PASS" if passed else "FAIL"), name)
        ok = ok and passed
    if errors:
        print("console errors:", errors)
    b.close()
    sys.exit(0 if ok else 1)
