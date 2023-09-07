import scrapy
from urllib.parse import urljoin


class bd_protidin(scrapy.Spider):
    name = "bd_protidin"
    start_urls = ['https://www.bd-pratidin.com/']

    def parse(self, response):
        for i in response.xpath("/html/body/div[6]/div/div[2]/div/div/ul/li"):
            url = urljoin(response.url, i.css("a").attrib['href'])
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        string = ""
        for info in response.xpath('//*[@id="bpsepnil"]/p/text()').getall():
            string += info
        store = str(response)[5:len(str(response))-1]
        yield {
            'title': response.xpath('/html/body/div[5]/div/div[1]/div[1]/div[2]/h1/text()').get().replace('\n', ''),
            'content': string.replace('\xa0', ''),
            'url': store
        }


