from playwright.async_api import Browser
from playwright.sync_api import Page
from playwright_stealth import stealth_async


async def new_tab(browser: Browser, link) -> Page:
    page = await browser.new_page()
    await stealth_async(page)
    await page.goto(link, wait_until='networkidle', timeout=120000)

    return page

