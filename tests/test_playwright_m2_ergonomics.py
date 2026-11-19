import os
import asyncio
import pytest
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')
FILE_URL = f"file:///{PROTOTYPE_PATH.replace(os.sep, '/')}"

async def _check_mobile_header():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()
        await page.goto(FILE_URL, wait_until="networkidle")
        
        # Check header height on mobile
        header_box = await page.locator("header").bounding_box()
        assert header_box is not None
        assert abs(header_box["height"] - 52) <= 4, f"Header height should be ~52px on mobile, got {header_box['height']}"

        # Check Perfil & Telegram buttons are hidden on mobile
        profile_btn = page.locator("header button:has-text('Perfil')")
        count_visible = await profile_btn.count()
        if count_visible > 0:
            is_vis = await profile_btn.is_visible()
            assert not is_vis, "Profile button should be hidden in mobile header"

        await browser.close()

def test_mobile_header_height_and_buttons():
    asyncio.run(_check_mobile_header())

async def _check_steppers():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()
        await page.goto(FILE_URL, wait_until="networkidle")

        # Switch to gym tab
        await page.evaluate("switchTab('gym')")
        await page.wait_for_timeout(300)

        # Check +2.5 stepper button height
        plus_weight_btn = page.locator("button:has-text('+2.5')").first
        box = await plus_weight_btn.bounding_box()
        assert box is not None
        assert box["height"] >= 44, f"Stepper height must be >=44px, got {box['height']}"

        # Check +1 rep stepper button height
        plus_rep_btn = page.locator("button:has-text('+1')").first
        box_rep = await plus_rep_btn.bounding_box()
        assert box_rep is not None
        assert box_rep["height"] >= 44, f"Rep stepper height must be >=44px, got {box_rep['height']}"

        # Add a set so delete button appears
        await page.evaluate("addSetRow(2, 1)")
        await page.wait_for_timeout(300)

        delete_btn = page.locator("button[title='Eliminar serie']").first
        del_box = await delete_btn.bounding_box()
        assert del_box is not None
        assert del_box["width"] >= 44 and del_box["height"] >= 44, f"Delete button must be >=44x44px, got {del_box['width']}x{del_box['height']}"

        await browser.close()

def test_steppers_and_delete_button_touch_targets():
    asyncio.run(_check_steppers())

async def _check_rest_timer():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()
        await page.goto(FILE_URL, wait_until="networkidle")

        await page.evaluate("switchTab('gym')")
        await page.wait_for_timeout(300)

        # Start 90s timer
        await page.evaluate("startRestTimer(90)")
        await page.wait_for_timeout(300)

        banner = page.locator("#rest-timer-banner")
        is_visible = await banner.is_visible()
        assert is_visible, "Rest timer banner should be visible when timer is started"

        countdown_text = await page.locator("#rest-timer-countdown").text_content()
        assert "1:30" in countdown_text or "01:30" in countdown_text

        # Cancel timer
        await page.evaluate("cancelRestTimer()")
        await page.wait_for_timeout(200)
        is_hidden = not await banner.is_visible()
        assert is_hidden, "Rest timer banner should hide on cancel"

        await browser.close()

def test_rest_timer_interaction():
    asyncio.run(_check_rest_timer())

async def _check_tactical_widget():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()
        await page.goto(FILE_URL, wait_until="networkidle")

        # Check tactical widget card
        widget = page.locator("h3:has-text('Cross Popular Parque del Soto')").first
        is_visible = await widget.is_visible()
        assert is_visible, "Tactical widget Cross Popular Parque del Soto should be visible"

        content = await page.content()
        assert "Clavos" in content, "Widget should recommend spikes / clavos"
        assert "3:30" in content, "Widget should mention target pace 3:30/km"
        assert "días" in content or "restantes" in content, "Widget should mention countdown / días restantes"

        await browser.close()

def test_playwright_tactical_widget_cross_del_soto():
    asyncio.run(_check_tactical_widget())

async def _check_safe_area_insets():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()
        await page.goto(FILE_URL, wait_until="networkidle")

        # Verify bottom nav dock safe-area style
        dock = page.locator("nav.lg\\:hidden")
        dock_style = await dock.get_attribute("style")
        assert dock_style is not None and "safe-area-inset-bottom" in dock_style, (
            f"Dock style must include safe-area-inset-bottom, got {dock_style}"
        )

        # Verify main container safe-area style
        main = page.locator("main")
        main_style = await main.get_attribute("style")
        assert main_style is not None and "safe-area-inset-bottom" in main_style, (
            f"Main container style must include safe-area-inset-bottom, got {main_style}"
        )

        await browser.close()

def test_playwright_safe_area_insets():
    asyncio.run(_check_safe_area_insets())

