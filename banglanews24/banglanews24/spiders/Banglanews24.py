import scrapy
from datetime import datetime


class Banglanews24Spider(scrapy.Spider):
    name = 'Banglanews24'
    allowed_domains = ['banglanews24.com']
    start_urls = ['https://www.banglanews24.com/category/%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%A8%E0%A7%80%E0%A6%A4%E0%A6%BF/1']

    def parse(self, response):
        body= response.css('td::text').getall()

        yield{
            'newspaper_name': body,
        }
    
