import asyncio

from playwright.async_api import async_playwright
from loguru import logger

from contents import SiteVladeiNet


@logger.catch
async def main():
    async with async_playwright() as p:

        # device = p.devices['Desktop Firefox']
        # browser = await p.firefox.launch(
        #     headless=False,
        #     proxy={
        #         'server': 'http://193.218.222.74:47651',  # Замініть на ваш проксі-сервер
        #         'username': 'XMdi7O2e01jYN8X',  # Замініть на ваше ім'я користувача, якщо потрібно
        #         'password': 'eZI2tI9litVH4GO'  # Замініть на ваш пароль, якщо потрібно
        #     }
        # )
        # context = await browser.new_context(
        #     **device,
        # )

        phone = p.devices["Pixel 4a (5G)"]
        browser = await p.chromium.launch(
            headless=False,
            proxy={
                'server': 'http://host:22225',
                'username': 'user',
                'password': 'pswd'
            }
        )
        context = await browser.new_context(
            **phone,
        )

        async with SiteVladeiNet(context) as creator:
            # await creator.page.pause()

            # action on page
            await creator.find_images()

            # await creator.page.pause()

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
