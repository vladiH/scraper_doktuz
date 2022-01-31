import scrapy
import re
from scrapy.http import Response
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
class DoktuzData(Item):
  codigo = Field()
  fecha = Field()
  empresa = Field()
  subcontrata = Field()
  proyecto = Field()
  t_exam = Field()
  paciente = Field()
  #imp = Field()
class BookstoscrapeItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    availability = scrapy.Field()

class BookSpiderSpider(scrapy.Spider):
    name = "book_spider"
    allowed_domains = ["books.toscrape.com"]
    def start_requests(self):
      urls = ["http://books.toscrape.com/"]
      for url in urls:
        yield scrapy.Request(url=url, callback=self.parse_pages)
    def parse_pages(self, response):
      books = response.xpath("//h3")
      for book in books:
        yield response.follow(url=book.xpath(".//a/@href").get(), callback=self.parse_books)
      next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
      if next_page_url is not None:
        yield response.follow(url=next_page_url, callback=self.parse_pages)

    def parse_books(self, response):
      title = response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get()
      price = response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="price_color"]/text()').get()
      stock = (
                response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="instock availability"]/text()')
                .getall()[-1]
                .strip()
            )
      rating = response.xpath('//div[@class="col-sm-6 product_main"]/p[3]/@class').get()
      item = BookstoscrapeItem()
      item["title"] = title
      item["price"] = price
      item["rating"] = rating
      item["availability"] = stock
      yield item

if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
    process = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'doktuz.json'
    })
    process.crawl(BookSpiderSpider)
    process.start()     
# EJECUCION
# scrapy runspider 4_tripadvisor.py -o tripadvisor_users.csv -t csv