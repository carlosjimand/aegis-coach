import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile iPhone 14 Pro viewport
        context = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        )
        page = await context.new_page()

        errors = []
        page.on('pageerror', lambda err: errors.append(f'PAGE ERROR: {err}'))
        page.on('console', lambda msg: errors.append(f'CONSOLE: {msg.text}') if msg.type == 'error' else None)

        url = 'https://aegis-intervals-sync.uranuslabs.workers.dev'
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # 1. Check Hero Card
        hero = page.locator('.hero-gradient-card').first
        is_hero_visible = await hero.is_visible()
        print('Hero gradient card visible:', is_hero_visible)
        hero_text = await hero.inner_text()
        print('Hero contains En Curso:', 'EN CURSO' in hero_text.upper())
        await page.screenshot(path='cloudflare/public_exercises/v5_mobile_hero.png')

        # 2. Switch to Entrenos Tab
        print('Testing Entrenos Tab...')
        await page.click("#dock-btn-workouts")
        await page.wait_for_timeout(800)

        month_label = await page.locator('#calendar-month-label').inner_text()
        print('Current month label:', month_label)

        # Click previous month (should go to Octubre 2026)
        await page.click('#cal-btn-prev')
        await page.wait_for_timeout(500)
        oct_label = await page.locator('#calendar-month-label').inner_text()
        print('After 1 click prev:', oct_label)

        # Click previous month again (should go to Septiembre 2026)
        await page.click('#cal-btn-prev')
        await page.wait_for_timeout(500)
        sep_label = await page.locator('#calendar-month-label').inner_text()
        print('After 2 clicks prev:', sep_label)

        # Click next month back to Noviembre 2026
        await page.click('#cal-btn-next')
        await page.wait_for_timeout(300)
        await page.click('#cal-btn-next')
        await page.wait_for_timeout(500)
        nov_label = await page.locator('#calendar-month-label').inner_text()
        print('After 2 clicks next (back to Nov):', nov_label)

        # Click day 14 (6x800m workout)
        day14 = page.locator('#calendar-days-grid > div[data-date="2026-11-14"]')
        await day14.click()
        await page.wait_for_timeout(500)

        detail_title = await page.locator('#detail-title').inner_text()
        print('Day 14 Title:', detail_title)

        laps_section = await page.locator('#detail-laps-section').inner_text()
        print('Laps section length:', len(laps_section))
        print('Laps text preview:\n', laps_section[:300])

        notes_section = await page.locator('#detail-notes-section').inner_text()
        print('Notes section length:', len(notes_section))
        print('Notes text preview:\n', notes_section[:200])

        await page.screenshot(path='cloudflare/public_exercises/v5_calendar_nov14.png')

        # 3. Switch to Gym Tab
        print('Testing Gym Tab...')
        await page.click("#dock-btn-gym")
        await page.wait_for_timeout(800)

        # Select Routine 1
        await page.click('#gym-chip-1')
        await page.wait_for_timeout(800)
        await page.screenshot(path='cloudflare/public_exercises/v5_gym_r1.png')

        # Select Routine 4
        await page.click('#gym-chip-4')
        await page.wait_for_timeout(800)
        await page.screenshot(path='cloudflare/public_exercises/v5_gym_r4.png')

        # 4. Switch to Perfil Tab
        print('Testing Perfil Tab...')
        await page.click("#dock-btn-profile")
        await page.wait_for_timeout(800)
        bmi_val = await page.locator('#bmi-display-value').inner_text()
        print('BMI val:', bmi_val)
        await page.screenshot(path='cloudflare/public_exercises/v5_profile.png')

        print('Errors encountered:', errors)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
