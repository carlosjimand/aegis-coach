import os
import asyncio
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\carlo\.gemini\antigravity\brain\d4e37e51-1f92-46c9-9a99-dcfde448f82c"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')
FILE_URL = f"file:///{PROTOTYPE_PATH.replace(os.sep, '/')}"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Mobile Viewport (iPhone 14 / Pixel: 390x844)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=2,
            is_mobile=True
        )
        page = await context.new_page()
        await page.goto(FILE_URL, wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Screenshot: Mobile Dashboard with Compact Header & Notification Hero
        path_mobile_dash = os.path.join(ARTIFACT_DIR, "prototype_v10_mobile_dashboard.png")
        await page.screenshot(path=path_mobile_dash)
        print("Captured prototype_v10_mobile_dashboard.png")

        # Scroll down to see Tactical Widget and Area Chart
        await page.evaluate("window.scrollBy(0, 380)")
        await page.wait_for_timeout(500)
        path_mobile_chart = os.path.join(ARTIFACT_DIR, "prototype_v10_mobile_tactical_chart.png")
        await page.screenshot(path=path_mobile_chart)
        print("Captured prototype_v10_mobile_tactical_chart.png")

        # Switch to Gym Tab
        await page.evaluate("switchTab('gym')")
        await page.wait_for_timeout(800)

        # Trigger Rest Timer (90s)
        await page.evaluate("startRestTimer(90)")
        await page.wait_for_timeout(500)

        # Click +2.5 kg stepper on first exercise
        await page.evaluate("stepWeight(2, 1, 0, 2.5)")
        await page.wait_for_timeout(500)

        path_mobile_gym = os.path.join(ARTIFACT_DIR, "prototype_v10_mobile_gym_steppers.png")
        await page.screenshot(path=path_mobile_gym)
        print("Captured prototype_v10_mobile_gym_steppers.png")

        # 2. Desktop Viewport (1440x900)
        context_desktop = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.5
        )
        page_desktop = await context_desktop.new_page()
        await page_desktop.goto(FILE_URL, wait_until="networkidle")
        await page_desktop.wait_for_timeout(1000)

        path_desktop_dash = os.path.join(ARTIFACT_DIR, "prototype_v10_desktop_dashboard.png")
        await page_desktop.screenshot(path=path_desktop_dash)
        print("Captured prototype_v10_desktop_dashboard.png")

        # Switch to Gym on desktop
        await page_desktop.evaluate("switchTab('gym')")
        await page_desktop.wait_for_timeout(800)
        path_desktop_gym = os.path.join(ARTIFACT_DIR, "prototype_v10_desktop_gym.png")
        await page_desktop.screenshot(path=path_desktop_gym)
        print("Captured prototype_v10_desktop_gym.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
