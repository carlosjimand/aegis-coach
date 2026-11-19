import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://aegis-intervals-sync.uranuslabs.workers.dev"

async def test_reproduce():
    async with async_playwright() as p:
        # Launch browser with persistent context or service workers enabled
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8; Brave) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()

        console_logs = []
        page.on("console", lambda m: console_logs.append(f"[{m.type}] {m.text}"))
        
        # 1st Visit
        print("--- Visit 1 (Clear context) ---")
        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(2000) # Give SW time to install & claim
        tailwind_v1 = await page.evaluate("() => typeof window.tailwind !== 'undefined'")
        print(f"Visit 1: window.tailwind defined = {tailwind_v1}")
        
        # 2nd Visit (Same context - simulating re-opening the app)
        print("--- Visit 2 (Reload / Reopen app with active SW) ---")
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(2000)
        tailwind_v2 = await page.evaluate("() => typeof window.tailwind !== 'undefined'")
        print(f"Visit 2: window.tailwind defined = {tailwind_v2}")
        
        sw_controller = await page.evaluate("() => Boolean(navigator.serviceWorker && navigator.serviceWorker.controller)")
        print(f"Visit 2: Service Worker controlling page = {sw_controller}")
        
        # Check computed style of a tailwind element
        btn_box = await page.locator("button:has-text('Ver Entreno')").bounding_box()
        print(f"Visit 2: 'Ver Entreno' bounding box = {btn_box}")

        for l in console_logs:
            if "error" in l.lower() or "warn" in l.lower() or "script" in l.lower() or "tailwind" in l.lower():
                print("  Console log:", l)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_reproduce())
