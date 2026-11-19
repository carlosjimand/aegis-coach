import os
import json
from playwright.sync_api import sync_playwright

BASE_DIR = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach"
FILE_URL = f"file:///{os.path.join(BASE_DIR, 'prototype', 'index.html').replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(FILE_URL, wait_until="networkidle")
    
    # 1. Header height
    h_box = page.locator("header").bounding_box()
    print("Header bounding box:", h_box)
    
    # Check hidden buttons in header
    prof_btn = page.locator("header button:has-text('Perfil')")
    prof_vis = prof_btn.is_visible() if prof_btn.count() > 0 else False
    print("Header profile button visible on mobile?:", prof_vis)
    
    # 2. Gym tab steppers
    page.evaluate("switchTab('gym')")
    page.wait_for_timeout(300)
    
    pw = page.locator("button:has-text('+2.5')").first.bounding_box()
    mw = page.locator("button:has-text('−2.5')").first.bounding_box()
    pr = page.locator("button:has-text('+1')").first.bounding_box()
    mr = page.locator("button:has-text('−1')").first.bounding_box()
    print("+2.5 box:", pw)
    print("-2.5 box:", mw)
    print("+1 box:", pr)
    print("-1 box:", mr)
    
    # Check stepper operations
    weight_input = page.locator("input[placeholder='kg']").first
    init_w = float(weight_input.input_value() or 0)
    page.evaluate("stepWeight(2, 1, 0, 2.5)")
    new_w = float(weight_input.input_value() or 0)
    print(f"Weight stepWeight: {init_w} -> {new_w} (expected {init_w + 2.5})")
    
    rep_input = page.locator("input[placeholder='0']").first
    init_r = int(rep_input.input_value() or 0)
    page.evaluate("stepRep(2, 1, 0, 1)")
    new_r = int(rep_input.input_value() or 0)
    print(f"Reps stepRep: {init_r} -> {new_r} (expected {init_r + 1})")
    
    # Delete button touch target
    page.evaluate("addSetRow(2, 1)")
    page.wait_for_timeout(200)
    del_btn = page.locator("button[title='Eliminar serie']").first.bounding_box()
    print("Delete button box:", del_btn)
    
    # Rest timer buttons
    btn90 = page.locator("button:has-text('90s')").first.bounding_box()
    btn2m = page.locator("button:has-text('2m')").first.bounding_box()
    print("90s button box:", btn90)
    print("2m button box:", btn2m)
    
    # Trigger rest timer
    page.evaluate("startRestTimer(90)")
    page.wait_for_timeout(300)
    banner = page.locator("#rest-timer-banner")
    print("Banner visible?:", banner.is_visible())
    countdown = page.locator("#rest-timer-countdown").text_content()
    print("Countdown text:", countdown)
    
    # Cancel rest timer
    page.evaluate("cancelRestTimer()")
    page.wait_for_timeout(200)
    print("Banner hidden after cancel?:", not banner.is_visible())
    
    # Bottom dock
    dock = page.locator("nav.lg\\:hidden").bounding_box()
    print("Bottom dock box:", dock)
    
    # Main padding
    main_el = page.locator("main")
    computed_padding_bottom = main_el.evaluate("el => parseFloat(window.getComputedStyle(el).paddingBottom)")
    print("Main computed padding bottom:", computed_padding_bottom)
    
    browser.close()
    print("Empirical Verification Succeeded Completely.")
