import scrapy
import logging
import os
from scrapy.http import Response, Request
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from selenium.webdriver import Chrome
from src.domain.doktuz.items import DoktuzItem
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)
class Doktuz(CrawlSpider):
  #name = 'Doktuz'
  # custom_settings = {
  #   'USER_AGENT': ,
  #   #'CLOSESPIDER_PAGECOUNT': 3
  # }
  
  allowed_domains = ["intranet.doktuz.com"]

  #download_delay = 1

  rules = ( 
    Rule(
      LinkExtractor( 
        allow=r'page=', 
        allow_domains=('intranet.doktuz.com'),
      ), follow=True, callback='parse_data',),
  )

  def __init__(self,*args, **kwargs):
    self.name = kwargs['name']
    self.start_urls = []
    super(Doktuz, self).__init__(*args, **kwargs) 

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = cls(
      name = crawler.settings.get('BOT_NAME'),
    )
    spider._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)
    spider.crawler = crawler
    return spider

  def start_requests(self):
    try:
      return [scrapy.FormRequest("https://intranet.doktuz.com/index.php?usuario=PPAMOLSA&pass=PPAMOLSA&btnenviar=Aceptar",
                               formdata={'usuario': 'PPAMOLSA', 'pass': 'PPAMOLSA'},
                               callback=self.parse_resultados)]
    except Exception as e:
      logger.critical('fail when spider was starting', exc_info=True)
                               
  def parse_resultados(self, response:Response):
    self.cookie = response.request.headers.getlist('Cookie')[0].decode('utf-8')
    return Request(response.url+'?fechafinal=27-01-2022&fechainicio=01-01-2022&dnip=&descripcion=&proyecto=&idempresa4=')                            
  
  def parse_data(self, response:Response):
    try:
      sel = Selector(response)
      rows = sel.xpath('//div[@id="tabs-1"]/table/tr[3]/td/table/tr[@class="FacetFilaTD"]')
      for row in rows:
        item = ItemLoader(DoktuzItem(), row)
        #cod = row.xpath("td[2]/div/text()").get()
        item.add_xpath('codigo', "td[2]/div/text()")
        item.add_xpath('fecha', "td[3]/text()")
        item.add_xpath('empresa', "td[4]/text()")
        item.add_xpath('subcontrata', "td[5]/text()")
        item.add_xpath('proyecto', "td[6]/text()")
        item.add_xpath('t_exam', "td[7]/text()")
        item.add_xpath('paciente', "td[8]/div/text()")
        valueImp = row.xpath('td[35]/a/@onclick').get()
        item.add_value('imp', valueImp)
        item.add_value('cookie', self.cookie)
        '''if(cod=="PQ4412-000054"):
          self.parse_pdf_page(response)'''
        yield item.load_item()
    except Exception as e:
      logger.warning('fail when spider was recovering data from '+ response.url, exc_info=True)

  '''def parse_pdf_page(self, response:Response):
    sel = Selector(response)
    self.logger.info("parse_pdf_page")
    with open("out.html", 'wb') as html_file:
      html_file.write(response.body)

  def errback_httpbin(self, failure):
    self.logger.info("errback_httpbin", failure)
    print(failure)

  def check_folder(dir_name):
    return os.path.isdir(dir_name)'''

  

