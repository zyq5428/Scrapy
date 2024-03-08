import scrapy
import re
import json
from urllib.parse import urljoin
# from moviedyn.items import MoviedynItem
from scrapy_playwright.page import PageMethod

BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = 'https://login3.scrape.center/login'
USERNAME = 'admin'
PASSWORD = 'admin'
COOKIE_FILE = 'cookies.json'

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        yield scrapy.Request(
            url = LOGIN_URL,
            callback = self.simulate_login,
            meta = {
                'playwright': True,
                'playwright_context': 'login',
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod("wait_for_selector", "input[type='password']"),
                ]
            },
            errback = self.errback_close_page,
        )

    async def simulate_login(self, response):
        page = response.meta['playwright_page']
        title = re.search(r'center\/(.*)', response.url).group(1)
        try:
            self.logger.info('Start logging in %s...', response.url)
            await page.locator('input[type="text"]').fill(USERNAME)
            await page.locator('input[type="password"]').fill(PASSWORD)
            await page.locator("form").get_by_role("button", name="登录").click()
            await page.wait_for_load_state("networkidle")
            username = page.get_by_text(USERNAME)
            await username.wait_for()
            # In order to obtain the token of JWT
            await page.goto(BASE_URL)
            await page.wait_for_load_state("networkidle")
            # save storage_state to file
            storage = await page.context.storage_state(path=COOKIE_FILE)
            self.logger.debug('Cookies is saved to %s: \n %s', COOKIE_FILE, storage)
            screenshot = await page.screenshot(path="./image/" + title + "_succeed.png", full_page=True)
        except Exception as e:
            self.logger.error('error occurred while scraping %s', url, exc_info=True)

        yield scrapy.Request(
            url = BASE_URL,
            callback = self.scrape_index,
            meta = {
                'playwright': True,
                'playwright_context': 'login',
                'playwright_page_methods': [
                    PageMethod("wait_for_selector", ".el-card__body"),
                ]
            },
            errback = self.errback_close_page,
        )
        await page.close()
        self.logger.info('The login page are closed')

    async def scrape_index(self, response):
        storage_state = {}
        with open('cookies.json') as f:
            storage_state = json.load(f)
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            index_url = f'{BASE_URL}page/{page}'
            self.logger.debug('Get detail url: %s', index_url)
            yield scrapy.Request(
                url = index_url,
                callback = self.parse_index,
                meta = {
                    'playwright': True,
                    'playwright_context': 'index',
                    "playwright_context_kwargs": {
                        "storage_state": storage_state,
                    },
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", ".el-card__body"),
                    ]
                },
                errback = self.errback_close_page,
            )

    async def parse_index(self, response):
        page = response.meta['playwright_page']
        books = response.css('.el-row .el-col')
        print(books)
        for book in books:
            href = book.css('.name::attr("href")').extract_first()
            url = urljoin(BASE_URL, href)
            self.logger.info('Get detail url: %s', url)
            # yield scrapy.Request(
            #     url = url,
            #     callback = self.parse_detail,
            #     meta = {
            #         'playwright': True,
            #         'playwright_context': 'detail',
            #         "playwright_context_kwargs": {
            #             "storage_state": storage_state,
            #         },
            #         'playwright_include_page': True,
            #         'playwright_page_methods': [
            #             PageMethod("wait_for_selector", "img.cover"),
            #         ]
            #     },
            #     errback = self.errback_close_page,
            # )
        await page.close()

    # async def parse_detail(self, response):
    #     page = response.meta['playwright_page']
    #     await page.close()

    #     item = MoviedynItem()
    #     item['cover'] = response.css('img.cover::attr("src")').extract_first()
    #     item['name'] = response.css('a > h2::text').extract_first()
    #     item['categories'] = response.css('.categories button span::text').re('(.*)\\n')
    #     item['published_at'] = response.css('.info  span::text').re('(.*) 上映')[0]
    #     # published_at = response.css('.info span:contains("上映")::text').extract_first()
    #     # item['published_at'] = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(0) \
    #     #     if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None
    #     item['drama'] = response.css('.drama p::text').extract_first()
    #     score = response.css('.score::text').extract_first()
    #     item['score'] = float(score) if score else None
    #     self.logger.debug('item: %s' % item)

    #     yield item

    async def errback_close_page(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()