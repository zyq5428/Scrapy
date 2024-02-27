import scrapy
import re
from urllib.parse import urljoin
from moviedyn.items import MoviedynItem
from scrapy_playwright.page import PageMethod

BASE_URL = 'https://spa1.scrape.center'

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            url = f'{BASE_URL}/page/{page}'
            yield scrapy.Request(
                url = url,
                callback = self.parse,
                meta = {
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", ".el-card"),
                    ]
                },
                errback = self.errback_close_page,
            )

    async def parse(self, response):
        page = response.meta['playwright_page']
        title = re.search(r'page\/(\d*)', response.url).group(1)
        screenshot = await page.screenshot(path="./image/" + title + ".png", full_page=True)
        await page.close()
        movies = response.css('.el-col .el-card')
        for movie in movies:
            item = MoviedynItem()
            item['name'] = movie.css('.el-row .m-b-sm::text').extract_first()
            href = movie.css('.el-col-xs-8 a::attr("href")').extract_first()
            item['url'] = urljoin(BASE_URL, href)
            item['img'] = movie.css('.cover::attr("src")').extract_first()
            self.logger.debug('item: %s' % item)
            yield item

    async def errback_close_page(self, failure):
        page = failure.requests.meta['playwright_page']
        await page.close()
