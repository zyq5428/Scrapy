import scrapy


class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
    	yield scrapy.Request(
            url = 'https://spa1.scrape.center/'
            callback = self.parse_first,
            meta = {
                'playwright': True,
                'playwright_include_page': True
                }
            errback = self.errback_close_page,
        )

    def parse_first(self, response):
        page = response.meta['playwright_page']

    async def parse_second(self, response):
        page = response.meta['playwright_page']

    async def errback_close_page(self, failure):
        page = failure.requests.meta['playwright_page']
        await page.close()
