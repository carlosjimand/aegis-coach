import time
from playwright.sync_api import sync_playwright

url = 'https://aegis-intervals-sync.uranuslabs.workers.dev?t=' + str(int(time.time()))

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 412, 'height': 915})
    page.goto(url, wait_until='networkidle')
    time.sleep(1.5)

    # 1. Switch to Workouts tab
    page.click('#tab-btn-workouts')
    time.sleep(1.5)
    page.screenshot(path='data/screenshots/test_workouts_today_expanded.png', full_page=True)
    print('Saved test_workouts_today_expanded.png')

    # 2. Click on Saturday 14 Nov to test accordion expansion
    page.click('#card-day-2026-11-14 button')
    time.sleep(1)
    page.screenshot(path='data/screenshots/test_accordion_saturday_expanded.png')
    print('Saved test_accordion_saturday_expanded.png')

    # 3. Test clicking deep link to Gym from Thursday (re-expand Thursday or click button)
    page.click('#card-day-2026-11-12 button')
    time.sleep(0.5)
    page.click('#detail-2026-11-12 button')
    time.sleep(1.5)
    page.screenshot(path='data/screenshots/test_deeplink_to_gym_routine3.png')
    print('Saved test_deeplink_to_gym_routine3.png')

    browser.close()

print('Playwright tests completed!')
