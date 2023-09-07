import json
import scrapy
from datetime import datetime

class Bdnews24(scrapy.Spider):
    name = 'Bdnews24'
    allowed_domains =['bangla.bdnews24.com']
    start_urls = ['https://bangla.bdnews24.com/api/v1/collections/111686?item-type=story&offset=0&limit=700']

    def parse(self, response):
        data= json.loads(response.body)
        body = data['items']
        for keyword in body:
            links = ("bangla.bdnews24.com/" + keyword['story']['slug'])

            yield response.follow(links, callback= self.parse_articles)

    def parse_articles(self,response):
        if (response.url).split("/")[3] in ('arts','lifestyle','chobirbhasa','probash','blog','kidz','tube'):
            pass
        else:
            date = response.css('div.wBeSy::text').get()
            newdate = date.split(' ')
            time = newdate[3]+ ' ' + newdate[4]
            in_time = datetime.strptime(time, "%I:%M %p")
            out_time = datetime.strftime(in_time, "%H:%M:%S")

            datetime1= '2023-01-'+ newdate[0]+ ' '+ out_time+'+06:00'
                    
            yield{
                'newspaper_name': 'Bdnews24',
                'title': response.css('h2.MbPT-::text').get(),
                'category': (response.url).split("/")[3],
                'url': response.url,
                'content': response.css('p::text').getall(),
                'newspaper_language': 'bn',
                'news_time_at': datetime1,
        }
#2023-01-08 20:16:09+06:00
