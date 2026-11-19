import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 420, 'height': 900})
        await page.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')

        await page.click('#dock-btn-gym')
        await page.wait_for_timeout(600)

        # R1 Ex 5
        await page.click('#gym-chip-1')
        await page.wait_for_timeout(600)
        img_b = page.locator('#gym-exercises-container img[src*="vector_ex_1_5"]')
        await img_b.scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        await img_b.screenshot(path='cloudflare/public_exercises/proof_img_bulgarian.png')

        # R4 Ex 5
        await page.click('#gym-chip-4')
        await page.wait_for_timeout(600)
        img_t = page.locator('#gym-exercises-container img[src*="vector_ex_4_5"]')
        await img_t.scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        await img_t.screenshot(path='cloudflare/public_exercises/proof_img_triceps.png')

        print('Image elements captured successfully!')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
