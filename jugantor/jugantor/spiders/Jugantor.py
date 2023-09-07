import scrapy
from datetime import datetime

class JugantorSpider(scrapy.Spider):
    name = 'Jugantor'
    allowed_domains = ['jugantor.com']
    start_urls = ['https://www.jugantor.com/all-news']

    def parse(self, response):
        links = response.css('div.col-8')
        for link in links.css('a.text-decoration-none::attr(href)'):
            yield response.follow(link.get(), callback= self.parse_articles)
        
        next_page = response.css('a[rel="next"]::attr(href)').get()   
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_articles(self,response):
            body = response.css('div.IfTxty')
            date = response.xpath('/html/body/main/div[5]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/text()').get()
            shomoy = date.replace('  |','')
            for i in shomoy:
                if i == '১':
                    shomoy = shomoy.replace('১', '1')
                if i == '২':
                    shomoy = shomoy.replace('২', '2')
                if i == '৩':
                    shomoy = shomoy.replace('৩', '3')
                if i == '৪':
                    shomoy = shomoy.replace('৪', '4')
                if i == '৫':
                    shomoy = shomoy.replace('৫', '5')
                if i == '৬':
                    shomoy = shomoy.replace('৬', '6')
                if i == '৭':
                    shomoy = shomoy.replace('৭', '7')
                if i == '৮':
                    shomoy = shomoy.replace('৮', '8')
                if i == '৯':
                    shomoy = shomoy.replace('৯', '9')
                if i == '০':
                    shomoy = shomoy.replace('০', '0')

            shomoy = shomoy.replace('জানুয়ারি','january')
            shomoy = shomoy.replace('ফেব্রুয়ারী','February')
            shomoy = shomoy.replace('মার্চ','March')
            shomoy = shomoy.replace('এপ্রিল','april')
            shomoy = shomoy.replace('মে','may')
            shomoy = shomoy.replace('জুন','june')
            shomoy = shomoy.replace('জুলাই','july')
            shomoy = shomoy.replace('অগাস্ট','august')
            shomoy = shomoy.replace('সেপ্টেম্বর','september')
            shomoy = shomoy.replace('অক্টোবর','october')
            shomoy = shomoy.replace('নভেম্বর','november')
            shomoy = shomoy.replace('ডিসেম্বর','december')
            shomoy = shomoy.replace('এএম','am')
            shomoy = shomoy.replace('পিএম','pm')
            shomoy = shomoy.replace(' \xa0|\xa0 ','')
            date_time_str = shomoy
            input_format = ' %d %B %Y, %I:%M %p'
            date_time_obj = datetime.strptime(date_time_str, input_format)
            output_format = '%Y-%m-%d %H:%M:%S%z'
            output_str = date_time_obj.strftime(output_format)

            newdate= output_str+'+06:00'
            yield{
            'newspaper_name': 'Jugantor',
            'title': response.css('h3.font-weight-bolder::text').get(),   
            'category': (response.url).split("/")[3],
            'url': response.url,
            'content': body.css('p::text').getall(),
            'newspaper_language': 'bn',
            'news_time_at': newdate,
        }   




        