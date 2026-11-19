import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://aegis-intervals-sync.uranuslabs.workers.dev"

async def capture_visit_2():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8; Brave) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
            device_scale_factor=2
        )
        page = await context.new_page()
        
        # 1st visit
        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        # 2nd visit (simulating closing and reopening app)
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        screenshot_path = "C:/Users/carlo/.gemini/antigravity/brain/d4e37e51-1f92-46c9-9a99-dcfde448f82c/mobile_verified_visit2_pwa.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"Saved visit 2 screenshot to: {screenshot_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_visit_2())
