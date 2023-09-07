import json
import scrapy


class ProthomaloSpider(scrapy.Spider):
    name = 'prothomalo'
    allowed_domains = ['prothomalo.com']
    start_urls = ['https://www.prothomalo.com/api/v1/collections/latest?offset=0&limit=1500']

    def parse(self, response):
        data= json.loads(response.body)
        body = data['items']
        for keyword in body:
            links = ("www.prothomalo.com/" + keyword['story']['slug'])

            yield response.follow(links, callback= self.parse_articles)

    def parse_articles(self,response):
        if (response.url).split("/")[3] in ('lifestyle','chakri','entertainment','fashion','poll','fun','travel','video','photo'):
            pass
        else:
            date = response.css('time::attr(datetime)').get()
            date = date.replace('T',' ')
            yield{
                'newspaper_name': 'Prothomalo',
                'title': response.css('h1.IiRps::text').get(),
                'category': (response.url).split("/")[3],
                'url': response.url,
                'content': response.css('p::text').getall(),
                'newspaper_language': 'bn',
                'news_time_at': date,            
        }

        

