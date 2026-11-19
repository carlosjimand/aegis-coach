import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://aegis-intervals-sync.uranuslabs.workers.dev"

async def extract_compiled_css():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 390, "height": 844})
        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        # Grab all injected style tags from tailwind
        css_content = await page.evaluate("""() => {
            const styles = Array.from(document.querySelectorAll('style'));
            return styles.map(s => s.innerHTML).join('\\n/* --- NEXT STYLE --- */\\n');
        }""")
        
        print(f"Total compiled CSS length: {len(css_content)} characters")
        with open("cloudflare/public_exercises/compiled_tailwind.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        print("Saved to cloudflare/public_exercises/compiled_tailwind.css!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(extract_compiled_css())
