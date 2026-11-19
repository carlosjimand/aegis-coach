import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')

        # Gym tab
        await page.click('#dock-btn-gym')
        await page.wait_for_timeout(600)

        # Routine 1 - Exercise 5 (Bulgarian)
        await page.click('#gym-chip-1')
        await page.wait_for_timeout(600)
        # Scroll to Exercise 5
        card_r1_ex5 = page.locator('text=Sentadilla Búlgara con Mancuernas').locator('..').locator('..')
        await card_r1_ex5.scroll_into_view_if_needed()
        await page.wait_for_timeout(400)
        await card_r1_ex5.screenshot(path='cloudflare/public_exercises/proof_bulgarian_card.png')

        # Routine 4 - Exercise 5 (Triceps)
        await page.click('#gym-chip-4')
        await page.wait_for_timeout(600)
        card_r4_ex5 = page.locator('text=Tríceps en Polea Unilateral').locator('..').locator('..')
        await card_r4_ex5.scroll_into_view_if_needed()
        await page.wait_for_timeout(400)
        await card_r4_ex5.screenshot(path='cloudflare/public_exercises/proof_triceps_card.png')

        print("Screenshots taken successfully!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
