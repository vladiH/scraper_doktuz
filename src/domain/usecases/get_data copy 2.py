import scrapy
import re
from scrapy.http import Response, Request
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class AfricanstudiesSpider(CrawlSpider):
    name = "africanstudies"

    allowed_domains = ["northwestern.edu"]
    start_urls = [
        "http://www.northwestern.edu/african-studies/about/"
    ]

   
    rules = (Rule(LinkExtractor(allow=(r'african-studies')),callback='parse_links',follow=True),)
   
    def parse_links(self, response):
      sel = scrapy.Selector(response)
      for href in sel.xpath('//a/@href').extract():
        print(href)
        url = response.url+ href
        yield Request(url, callback = self.parse_items)
           
    def parse_items(self, response):
      self.log('Hi, this is an item page! %s' % response.url)

      for sel in response.xpath('//div[2]/div[1]'):
          item = {}
          item['url'] = response.url
          item['title'] = sel.xpath('div[3]/*[@id="green_title"]/text()').extract()      
          item['desc'] = sel.xpath('div[4]/*').extract()      
          yield item

if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
    process = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'doktuz.json'
    })
    process.crawl(AfricanstudiesSpider)
    process.start()     
# EJECUCION
# scrapy runspider 4_tripadvisor.py -o tripadvisor_users.csv -t csv