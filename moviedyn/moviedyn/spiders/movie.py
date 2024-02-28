import scrapy
import re
from urllib.parse import urljoin
from moviedyn.items import MoviedynItem
from scrapy_playwright.page import PageMethod

BASE_URL = 'https://spa6.scrape.center'

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            url = f'{BASE_URL}/page/{page}'
            context_name = 'context' + str(page)
            yield scrapy.Request(
                url = url,
                callback = self.parse_index,
                meta = {
                    'playwright': True,
                    'playwright_context': context_name,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", ".el-card .name"),
                    ]
                },
                errback = self.errback_close_page,
            )

    async def parse_index(self, response):
        page = response.meta['playwright_page']
        title = re.search(r'page\/(\d*)', response.url).group(1)
        screenshot = await page.screenshot(path="./image/" + title + ".png", full_page=True)
        movies = response.css('.el-col .el-card')
        for movie in movies:
            # item = MoviedynItem()
            # item['name'] = movie.css('.el-row .m-b-sm::text').extract_first()
            # href = movie.css('.el-col-xs-8 a::attr("href")').extract_first()
            # item['url'] = urljoin(BASE_URL, href)
            # item['img'] = movie.css('.cover::attr("src")').extract_first()
            # self.logger.debug('item: %s' % item)
            # yield item
            href = movie.css('.name::attr("href")').extract_first()
            url = urljoin(BASE_URL, href)
            self.logger.debug('detail url: %s' % url)
            yield scrapy.Request(
                url = url,
                callback = self.parse_detail,
                meta = {
                    'playwright': True,
                    'playwright_context': response.meta['playwright_context'],
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", ".el-card .name"),
                    ]
                },
                errback = self.errback_close_page,
            )
        await page.close()

    async def parse_detail(self, response):
        page = response.meta['playwright_page']
        await page.close()

        item = MoviedynItem()
        item['cover'] = response.css('img.cover::attr("src")').extract_first()
        item['name'] = response.css('a > h2::text').extract_first()
        item['categories'] = response.css('.categories button span::text').re('(.*)\\n')
        item['published_at'] = response.css('.info span::text').re('(.*) 上映')[0]
        # published_at = response.css('.info span:contains("上映")::text').extract_first()
        # item['published_at'] = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(0) \
        #     if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None
        item['drama'] = response.css('.drama p::text').extract_first()
        score = response.css('.score::text').extract_first()
        item['score'] = float(score) if score else None
        self.logger.debug('item: %s' % item)

        yield item

    async def errback_close_page(self, failure):
        page = failure.requests.meta['playwright_page']
        await page.close()
