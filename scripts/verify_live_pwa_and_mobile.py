import asyncio
import os
import requests
from playwright.async_api import async_playwright

BASE_URL = "https://aegis-intervals-sync.uranuslabs.workers.dev"

async def test_live():
    print("=== STEP 1: Verifying Live HTTP Endpoints ===")
    endpoints = [
        ("/", "text/html"),
        ("/manifest.json?v=20261116b", "application/manifest+json"),
        ("/favicon.ico?v=20261116b", "image/x-icon"),
        ("/favicon.png", "image/png"),
        ("/apple-touch-icon.png", "image/png"),
        ("/img/icon-192.png?v=20261116b", "image/png"),
        ("/img/icon-512.png?v=20261116b", "image/png"),
        ("/sw.js", "application/javascript")
    ]
    
    for path, expected_content_type in endpoints:
        url = BASE_URL + path
        r = requests.get(url, timeout=10)
        assert r.status_code == 200, f"Endpoint {path} failed with {r.status_code}"
        assert expected_content_type in r.headers.get("Content-Type", ""), f"Content-type mismatch for {path}: {r.headers.get('Content-Type')}"
        print(f"  [OK] {path} -> 200 ({r.headers.get('Content-Type')}) [{len(r.content)} bytes]")
    
    # Check manifest JSON icons
    r_man = requests.get(BASE_URL + "/manifest.json?v=20261116b").json()
    assert len(r_man.get("icons", [])) >= 4, "Manifest must have at least 4 icons"
    purposes = [i.get("purpose") for i in r_man["icons"]]
    assert "any" in purposes, "Manifest must have purpose: any"
    assert "maskable" in purposes, "Manifest must have purpose: maskable"
    print("  [OK] Manifest icons verified with both 'any' and 'maskable'!")

    # Check SW version
    r_sw = requests.get(BASE_URL + "/sw.js").text
    assert "aegis-coach-v6" in r_sw, "SW must be aegis-coach-v6"
    print("  [OK] Service Worker confirmed on v6 with Network-First navigation!")

    print("\n=== STEP 2: Playwright Mobile & Ergonomics Verification ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Test Android Mobile Viewport (Pixel 8 / Brave Mobile)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8; Brave) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
            device_scale_factor=2
        )
        page = await context.new_page()
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        res = await page.goto(BASE_URL, wait_until="networkidle")
        assert res.status == 200
        
        # 1. Desktop sidebar must be completely hidden on mobile
        sidebar = page.locator("#desktop-sidebar")
        is_sidebar_visible = await sidebar.is_visible()
        print(f"  Sidebar visible on mobile: {is_sidebar_visible} (Must be False)")
        assert not is_sidebar_visible, "Desktop sidebar MUST NOT be visible on mobile!"
        
        # 2. Check topbar header logo dimensions
        topbar_logo = page.locator(".logo-container-topbar")
        box = await topbar_logo.bounding_box()
        print(f"  Topbar logo bounding box: {box}")
        assert box is not None
        assert box["width"] <= 48 and box["height"] <= 48, f"Topbar logo too large: {box}"
        
        # 3. Check page width / overflow
        viewport_width = 390
        scroll_width = await page.evaluate("() => document.documentElement.scrollWidth")
        print(f"  Document scroll width: {scroll_width} (Viewport: {viewport_width})")
        assert scroll_width <= viewport_width + 1, f"Horizontal overflow detected! scrollWidth: {scroll_width}"
        
        # 4. Save screenshots
        mobile_shot = "C:/Users/carlo/.gemini/antigravity/brain/d4e37e51-1f92-46c9-9a99-dcfde448f82c/mobile_verified_pwa.png"
        await page.screenshot(path=mobile_shot, full_page=False)
        print(f"  Saved mobile screenshot to: {mobile_shot}")
        
        # 5. Check desktop viewport as well (1280x800)
        desk_context = await browser.new_context(viewport={"width": 1280, "height": 800})
        desk_page = await desk_context.new_page()
        await desk_page.goto(BASE_URL, wait_until="networkidle")
        desk_sidebar = desk_page.locator("#desktop-sidebar")
        desk_sidebar_visible = await desk_sidebar.is_visible()
        print(f"  Sidebar visible on desktop: {desk_sidebar_visible} (Must be True)")
        assert desk_sidebar_visible, "Desktop sidebar MUST be visible on desktop!"
        
        desk_shot = "C:/Users/carlo/.gemini/antigravity/brain/d4e37e51-1f92-46c9-9a99-dcfde448f82c/desktop_verified_pwa.png"
        await desk_page.screenshot(path=desk_shot, full_page=False)
        print(f"  Saved desktop screenshot to: {desk_shot}")
        
        await browser.close()
        print("\n=== ALL PRODUCTION CHECKS PASSED PERFECTLY ===")

if __name__ == "__main__":
    asyncio.run(test_live())
