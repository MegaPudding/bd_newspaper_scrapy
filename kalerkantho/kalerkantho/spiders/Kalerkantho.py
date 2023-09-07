import scrapy
import json
import requests

class KalerkanthoSpider(scrapy.Spider):
    name = 'Kalerkantho'
    allowed_domains = ['kalerkantho.com']
    start_urls = ['http://kalerkantho.com/']

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}
        all_links=[]
        response = requests.get('https://bn-api.kalerkantho.com/api/online/Politics?page=1',headers=headers)
        body = json.loads(response.content)
        last_page = (body['category']['last_page'])
        for i in range(1, last_page+1):
            url = f'https://bn-api.kalerkantho.com/api/online/Politics?page={i}'
            response = requests.get(url,headers=headers)
            body_1 = json.loads(response.content)
            data_1=body_1['category']['data']
            for keyword in data_1:
                links = ("https://www.kalerkantho.com/online/" + keyword['cat_name']['slug']+'/'+keyword['f_date']+'/'+str(keyword['n_id']))
                all_links.append(links)

        response = requests.get('https://bn-api.kalerkantho.com/api/online/national?page=1',headers=headers)
        body = json.loads(response.content)
        last_page = (body['category']['last_page'])
        for i in range(1, 10):
            url = f'https://bn-api.kalerkantho.com/api/online/national?page={i}'
            response = requests.get(url,headers=headers)
            body_1 = json.loads(response.content)
            data_1=body_1['category']['data']
            for keyword in data_1:
                links = ("https://www.kalerkantho.com/online/" + keyword['cat_name']['slug']+'/'+keyword['f_date']+'/'+str(keyword['n_id']))
                all_links.append(links)

        response = requests.get('https://bn-api.kalerkantho.com/api/online/business?page=1',headers=headers)
        body = json.loads(response.content)
        last_page = (body['category']['last_page'])
        for i in range(1, last_page):
            url = f'https://bn-api.kalerkantho.com/api/online/business?page={i}'
            response = requests.get(url,headers=headers)
            body_1 = json.loads(response.content)
            data_1=body_1['category']['data']
            for keyword in data_1:
                links = ("https://www.kalerkantho.com/online/" + keyword['cat_name']['slug']+'/'+keyword['f_date']+'/'+str(keyword['n_id']))
                all_links.append(links)

        response = requests.get('https://bn-api.kalerkantho.com/api/online/country-news?page=1',headers=headers)
        body = json.loads(response.content)
        last_page = (body['category']['last_page'])
        for i in range(1, 10):
            url = f'https://bn-api.kalerkantho.com/api/online/country-news?page={i}'
            response = requests.get(url,headers=headers)
            body_1 = json.loads(response.content)
            data_1=body_1['category']['data']
            for keyword in data_1:
                links = ("https://www.kalerkantho.com/online/" + keyword['cat_name']['slug']+'/'+keyword['f_date']+'/'+str(keyword['n_id']))
                all_links.append(links)
        
        for link in all_links:
            links = link

            yield response.follow(links, callback= self.parse_articles)
        #print(len(all_links))

    def parse_articles(self,response):

            date = response.css('div.wBeSy::text').get()
            newdate = date.split(' ')
            time = newdate[3]+ ' ' + newdate[4]
            #in_time = datetime.strptime(time, "%I:%M %p")
            #out_time = datetime.strftime(in_time, "%H:%M:%S")

            #datetime1= '2023-01-'+ newdate[0]+ ' '+ out_time+'+06:00'
                    
            yield{
                'newspaper_name': 'Kalerkantho',
                'title': response.css('h1.my-3::text').get(),
                'category': (response.url).split("/")[4],
                'url': response.url,
                'content': response.css('p::text').getall(),
                'newspaper_language': 'bn',
                'news_time_at': date,
        }   
