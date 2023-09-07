import scrapy
from prothomalo.items import ProthomaloItem
from scrapy.loader import ItemLoader

class Prothomalo(scrapy.Spider):
    name = 'Prothomalo'
    allowed_domains =['prothomalo.com']
    start_urls = ['https://www.prothomalo.com/search']

    def parse(self, response):
        for link in response.css('a.card-with-image-zoom::attr(href)'):
            yield response.follow(link.get(), callback= self.parse_articles)

    def parse_articles(self,response):
        yield{
            'url': response.url,
            'title': response.css('h1.IiRps::text').get(),
            'article': response.css('p::text').getall(),
            
        }
