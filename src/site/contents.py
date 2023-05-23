import asyncio
import os
from urllib.parse import urlparse

import aiofiles
import aiohttp
from fake_useragent import UserAgent
from loguru import logger
from playwright.async_api import Page
from handl_page import new_tab


class SiteVladeiNet:
    def __init__(self, browser):
        self.browser = browser

    async def __aenter__(self):
        self.page: Page = await new_tab(self.browser, 'https://vladey.net/en/artist/doping-pong')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.page.close()

    async def download_image(self, image_url, image_path, proxy=None, auth=None):

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, proxy=proxy,
                                   proxy_auth=auth, headers={'User-Agent': UserAgent().random}) as resp:

                if resp.status == 200:
                    f = await aiofiles.open(image_path, mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                else:
                    logger.error(f'Error: {resp.status}')

    async def find_images(self):
        proxy = 'http://host:22225'
        user = 'user'
        password = 'pswd'
        auth = aiohttp.BasicAuth(user, password)

        images = await self.page.locator('//img[contains(@src, "https://api.vladey.net/")]').all()

        # tasks = [asyncio.create_task(self.download_images(idx, image)) for idx, image in enumerate(images)]
        #
        # await asyncio.gather(*tasks)

        for idx, image_element in enumerate(images):
            if idx != 0:
                image_url = await image_element.get_attribute('src')
                logger.info(image_url)
                parsed_url = urlparse(image_url)
                file_extension = os.path.splitext(parsed_url.path)[1]
                path_to_photo = f'/home/albedo/PycharmProjects/vladei-net/src/site/images/{str(idx) + file_extension}'
                logger.info(path_to_photo)

                task = asyncio.create_task(self.download_image(image_url, path_to_photo, proxy, auth))
                await task

        logger.info('done')


