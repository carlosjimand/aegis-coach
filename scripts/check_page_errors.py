import os
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')
FILE_URL = f"file:///{PROTOTYPE_PATH.replace(os.sep, '/')}"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"[PAGE CONSOLE] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))
        await page.goto(FILE_URL)
        await page.wait_for_timeout(1000)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
