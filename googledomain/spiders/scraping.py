import scrapy
from scrapy import Request
from scrapy.item import Item, Field
import json
import csv

class SiteProductItem(Item):
    keyword = Field()
    domain = Field()


class GoogleScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.google.com']

    def __init__(self, **kwargs):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/57.0.2987.133 Safari/537.36"}

        with open('Search_Terms.csv', 'r') as csvfile:
            self.keyword_list = []
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.keyword_list.append(row[0])

    def start_requests(self):
        for keyword in self.keyword_list:
            search_url = 'https://www.google.com/search?q={}&num=200'.format(keyword)
            yield Request(url=search_url,
                          callback=self.parse_page,
                          headers=self.headers,
                          dont_filter=True,
                          meta={'keyword': keyword}
                          )

    def parse_page(self, response):
        keyword = response.meta['keyword']
        url_list = response.xpath('//div[@class="rc"]/div[@class="r"]/a/@href').extract()
        product = SiteProductItem()
        if len(url_list) > 0:
            for url in url_list:
                assert_domain_info = url.split('://')[1]
                if assert_domain_info:
                    domain = assert_domain_info.split('/')[0]
                    if keyword in domain:
                        product['keyword'] = keyword
                        product['domain'] = domain

                        yield product



