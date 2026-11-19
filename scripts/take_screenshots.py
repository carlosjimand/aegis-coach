import os
import time
from playwright.sync_api import sync_playwright

os.makedirs('data/screenshots', exist_ok=True)
url = 'https://aegis-intervals-sync.uranuslabs.workers.dev'

with sync_playwright() as p:
    # 1. Mobile iPhone / Android viewport
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 412, 'height': 915},
        user_agent='Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    )
    page = context.new_page()
    page.goto(url, wait_until='networkidle')
    time.sleep(2) # ensure charts render

    # Screenshot 1: Mobile Dashboard Top
    page.screenshot(path='data/screenshots/mobile_dashboard_top.png')
    print('Saved data/screenshots/mobile_dashboard_top.png')

    # Screenshot 2: Mobile Dashboard Full Page
    page.screenshot(path='data/screenshots/mobile_dashboard_full.png', full_page=True)
    print('Saved data/screenshots/mobile_dashboard_full.png')

    # Screenshot 3: Switch to Gym tab
    page.click('#tab-btn-gym')
    time.sleep(1.5)
    page.screenshot(path='data/screenshots/mobile_gym_tab.png')
    print('Saved data/screenshots/mobile_gym_tab.png')

    # Screenshot 4: Full page Gym tab with exercises
    page.screenshot(path='data/screenshots/mobile_gym_full.png', full_page=True)
    print('Saved data/screenshots/mobile_gym_full.png')

    # Screenshot 5: Switch to Workouts tab
    page.click('#tab-btn-workouts')
    time.sleep(1)
    page.screenshot(path='data/screenshots/mobile_workouts_tab.png')
    print('Saved data/screenshots/mobile_workouts_tab.png')

    browser.close()

    # 2. Desktop View
    browser_desk = p.chromium.launch(headless=True)
    page_desk = browser_desk.new_page(viewport={'width': 1280, 'height': 800})
    page_desk.goto(url, wait_until='networkidle')
    time.sleep(2)
    page_desk.screenshot(path='data/screenshots/desktop_dashboard.png')
    print('Saved data/screenshots/desktop_dashboard.png')
    browser_desk.close()

print('All screenshots captured successfully!')
