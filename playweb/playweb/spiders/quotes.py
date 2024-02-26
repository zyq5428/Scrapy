import scrapy

from playweb.items import QuoteItem
from scrapy_playwright.page import PageMethod

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(
            url=url, 
            callback=self.parse,
            meta={
                "playwright": True,
                # "playwright_include_page": True,
                # "playwright_page_methods": [
                #     PageMethod("wait_for_selector", "div.quote")
                # ]
            },
            errback=self.errback
		)

    async def parse(self, response):
        # page = response.meta["playwright_page"]
        # await page.close()

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            print(quote_item)
            yield quote_item

    async def errback(self, failure):
        # page = failure.request.meta["playwright_page"]
        # await page.close()
        pass