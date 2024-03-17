import scrapy
from scrapy import Spider, Request
from antispider.items import MovieItem
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin

BASE_URL = 'https://antispider1.scrape.center/'

# Bypass Webdriver detection
js = """
Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
"""
async def init_page(page, request):
    await page.add_init_script(js)

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        yield scrapy.Request(
            url = BASE_URL,
            callback = self.parse,
            meta = {
                'playwright': True,
                'playwright_context': 'login',
                'playwright_include_page': True,
                'playwright_page_init_callback': init_page,
                'playwright_page_methods': [
                    PageMethod("wait_for_selector", ".el-pagination__total"),
                ]
            },
            errback = self.errback_close_page,
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        screenshot = await page.screenshot(path="./image/" + "web.png", full_page=True)

    async def errback_close_page(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
