import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Test (1280x860)
        context_desktop = await browser.new_context(viewport={'width': 1280, 'height': 860})
        page_d = await context_desktop.new_page()

        errors_d = []
        page_d.on('pageerror', lambda err: errors_d.append(f'PAGE ERROR: {err}'))
        page_d.on('console', lambda msg: errors_d.append(f'CONSOLE: {msg.text}') if msg.type == 'error' else None)

        url = 'https://aegis-intervals-sync.uranuslabs.workers.dev'
        print(f"Navigating Desktop to {url}...")
        await page_d.goto(url, wait_until='networkidle')
        await page_d.wait_for_timeout(1000)

        # Desktop Dashboard Screenshot
        await page_d.screenshot(path='cloudflare/public_exercises/v9_desktop_dashboard.png', full_page=True)

        # 2. Mobile Test (390x844 iPhone 14 Pro)
        context_mobile = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        )
        page_m = await context_mobile.new_page()

        errors_m = []
        page_m.on('pageerror', lambda err: errors_m.append(f'PAGE ERROR: {err}'))
        page_m.on('console', lambda msg: errors_m.append(f'CONSOLE: {msg.text}') if msg.type == 'error' else None)

        print(f"Navigating Mobile to {url}...")
        await page_m.goto(url, wait_until='networkidle')
        await page_m.wait_for_timeout(1000)

        # Top mobile screen showing minimalist notification hero
        await page_m.screenshot(path='cloudflare/public_exercises/v9_mobile_top_screen.png')

        # Mobile Hero Notification Card Screenshot
        hero = page_m.locator('.hero-gradient-card').first
        await hero.screenshot(path='cloudflare/public_exercises/v9_mobile_hero_notification.png')

        # Click on "Ver Entreno" button to verify navigation to detailed workout in workouts tab
        btn = hero.locator('button:has-text("Ver Entreno")')
        await btn.click()
        await page_m.wait_for_timeout(800)
        await page_m.screenshot(path='cloudflare/public_exercises/v9_mobile_navigated_workout.png')

        print("Desktop Errors:", errors_d)
        print("Mobile Errors:", errors_m)
        print("Playwright screenshots generated successfully with v9!")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
