import scrapy


class SamakalSpider(scrapy.Spider):
    name = 'Samakal'
    allowed_domains = ['samakal.com']
    start_urls = ['https://samakal.com/list/all']
    
    def parse(self, response):
        for link in response.css('a.link-overlay::attr(href)'):
            yield response.follow(link.get(), callback= self.parse_articles)

        next_page = response.css('a.relative::attr(href)').getall()[1]    
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            
    def parse_articles(self,response):
        body=response.css('div.description')
        datetime = response.css('p.detail-time::text').get()
        shomoy = datetime.split('|')[0].replace(' প্রকাশ: ','')
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
        newdate = shomoy.split(' ')
        datetime= '2023-01-'+ newdate[0]+ ' '+newdate[4]+':00+06:00'
        yield{
            'newspaper_name': 'samakal',
            'title': response.css('h1.font-xs-h::text').get(),   
            'category': (response.url).split("/")[3],
            'url': response.url,
            'content': body.css('span::text').getall() + body.css('p::text').getall(),
            'newspaper_language': 'bn',
            'news_time_at': datetime,
        }
    