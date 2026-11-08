"""Render a page's chart as a 1200x630 link-preview card (needs Playwright with Chromium).

    python scripts/make-og-image.py site/harnesses.html site/og-harnesses.png "same model, nine coding harnesses"
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

page_path, out, subtitle = sys.argv[1:4]
CSS = """
main { max-width: 860px !important; padding: 14px 0 0 !important; }
main > *:not(section[aria-labelledby="complexity"]) { display: none !important; }
section[aria-labelledby="complexity"] > *:not(#graph):not(#company-legend):not(#og-title) { display: none !important; }
#og-title { font-size: 30px; margin: 0 0 6px; }
#og-title span { font-weight: 400; color: #666; }
"""
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 630})
    page.goto(Path(page_path).resolve().as_uri())
    page.add_style_tag(content=CSS)
    page.evaluate("""s => { const h = document.createElement('h1'); h.id = 'og-title';
        h.innerHTML = '<b>Parsimony</b> <span>· ' + s + '</span>';
        document.querySelector('section[aria-labelledby="complexity"]').prepend(h);
        window.dispatchEvent(new Event('resize')); }""", subtitle)
    page.wait_for_timeout(500)
    page.screenshot(path=out, clip={'x': 0, 'y': 0, 'width': 1200, 'height': 630})
    browser.close()
