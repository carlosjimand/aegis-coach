import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser with mobile viewport (iPhone / Android)
        browser = await p.chromium.launch(headless=True)
        
        # Test 1: Mobile viewport 390x844 (like mobile Brave/Chrome)
        context_mobile = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
        )
        page_mobile = await context_mobile.new_page()
        
        errors = []
        page_mobile.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page_mobile.on("console", lambda msg: print(f"Console [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)
        
        print("Navigating to production on mobile...")
        res = await page_mobile.goto("https://aegis-intervals-sync.uranuslabs.workers.dev/", wait_until="networkidle")
        print(f"Response status: {res.status}")
        
        screenshot_path = os.path.join(os.getcwd(), "mobile_production_check.png")
        await page_mobile.screenshot(path=screenshot_path, full_page=False)
        print(f"Mobile screenshot saved to {screenshot_path}")
        
        # Check elements
        logo_el = page_mobile.locator("img[src*='logo'], svg, #app-logo")
        print(f"Logo elements found: {await logo_el.count()}")
        
        # Test full page height and see if something is huge
        body_box = await page_mobile.locator("body").bounding_box()
        print(f"Body bounding box: {body_box}")
        
        # Also check desktop
        context_desktop = await browser.new_context(viewport={"width": 1280, "height": 800})
        page_desktop = await context_desktop.new_page()
        await page_desktop.goto("https://aegis-intervals-sync.uranuslabs.workers.dev/", wait_until="networkidle")
        desktop_screenshot = os.path.join(os.getcwd(), "desktop_production_check.png")
        await page_desktop.screenshot(path=desktop_screenshot, full_page=False)
        print(f"Desktop screenshot saved to {desktop_screenshot}")
        
        await browser.close()
        print("Done diagnosing.")

if __name__ == "__main__":
    asyncio.run(main())
