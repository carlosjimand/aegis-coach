import os
from playwright.sync_api import sync_playwright

def capture():
    html_path = os.path.abspath("scripts/test_logos.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    print(f"Loading: {file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1800})
        page.goto(file_url, wait_until="networkidle")
        
        # Wait a moment for fonts and images to load
        page.wait_for_timeout(1000)

        # Full page screenshot
        page.screenshot(path="cloudflare/public_exercises/logo_concepts_overview.png", full_page=True)
        print("Captured: logo_concepts_overview.png")

        # Concepts grid screenshot
        grid_el = page.locator("#concepts-grid")
        if grid_el.count() > 0:
            grid_el.screenshot(path="cloudflare/public_exercises/logo_concepts_grid.png")
            print("Captured: logo_concepts_grid.png")

        browser.close()

if __name__ == "__main__":
    capture()
