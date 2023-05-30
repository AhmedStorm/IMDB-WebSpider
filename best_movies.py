import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0'

    def start_requests(self):
        yield scrapy.Request(url="https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type", headers={'User-Agent': self.user_agent})
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(
            restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        # print(response.url)
        yield{
            'name': response.xpath(" //div[@class='sc-b5e8e7ce-1 kNhUtn']/h1/text()").get(),
            'year': response.xpath("(//span[@class='sc-f26752fb-2 eqUJdo'])[1]/text()").get(),
            'duration': response.xpath("(//li[@class='ipc-inline-list__item'])[7]/text()").getall(),
            'genre': response.xpath("//div[@class='ipc-chip-list__scroller']/a/span/text()").getall(),
            'rate': response.xpath("(//span[@class='sc-e457ee34-1 gvYTvP'])[2]/text()").get(),
            'is_mature': response.xpath("(//span[@class='sc-f26752fb-2 eqUJdo'])[2]/text()").get(),
            'movie_url': response.url
        }
