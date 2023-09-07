import scrapy
import requests
import re
import json


class BanglatribuneSpider(scrapy.Spider):
    name = 'Banglatribune'
    #allowed_domains = ['banglatribune.com']
    start_urls = ['https://www.banglatribune.com/api/theme_engine/get_ajax_contents?widget=10950&start=751&count=250&page_id=0&author=0&tags=&archive_time=']

    def parse(self, response):
        data= json.loads(response.body)
        body = data['html']
        matches = re.findall(r'"(?<=href=")(.*?)(?=")"', body, re.DOTALL)
        link=[]
        for i in range(len(matches)):
            txt = matches[i]
            x = re.split("\//", txt)
            link.append(x[1])

        for i in range(len(link)):
            yield response.follow("https://"+link[i], callback= self.parse_articles)
    
    def parse_articles(self,response):
        if (response.url).split("/")[3] in ('entertainment','lifestyle','jobs','video'):
            pass
        else:
            date = response.css('span.tts_time::attr(content)').get()
            date = date.replace('T',' ')
            yield{
                'newspaper_name':'Banglatribune',
                'title': response.css('h1.title::text').get(), 
                'category': (response.url).split("/")[3],
                'url': response.url,   
                'content': response.css('p::text').getall(),
                'newspaper_language': 'bn',
                'news_time_at': date,
        }
