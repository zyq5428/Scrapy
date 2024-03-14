import scrapy
from scrapy import Spider, Request
from antispider.items import MovieItem
from urllib.parse import urljoin

BASE_URL = 'https://ssr1.scrape.center'

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            url = f'{BASE_URL}/page/{page}'
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        movies = response.css('.el-col .el-card')
        for movie in movies:
            item = MovieItem()
            item['name'] = movie.css('.name .m-b-sm::text').extract_first()
            # self.logger.debug('item: %s' % item)
            yield item
