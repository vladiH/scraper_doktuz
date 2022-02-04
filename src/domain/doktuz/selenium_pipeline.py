import os
import json
import logging
from selenium import webdriver
from textwrap import dedent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

logger = logging.getLogger(__name__)
class DoktuzSeleniumPipeline:
    def __init__(self,driver_path):
        self.driver_path = driver_path
        self.cookie = None

    def open_spider(self, spider):
        try:
            local_dir = os.getcwd()
            local_dir = local_dir + '/pdfs'
            self.create_directory(local_dir)
            chrome_options = webdriver.ChromeOptions()
            settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF", "version": 2}
            prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'savefile.default_directory': local_dir}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--kiosk-printing')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
        except Exception as e:
            logger.warning('fail when spider was opening selenium driver', exc_info=True)

    def close_spider(self, spider):
        self.driver.close()
        
    @classmethod
    def from_crawler(cls, crawler):
        dp = crawler.settings.get('DRIVER_PATH')
        return cls(
            driver_path=dp,
        )

    async def process_item(self, item, spider):
        try:
            if(self.cookie==None):
                self.cookie = item['cookie'].split('=')
                self.driver.get(item['imp'])
                self.driver.delete_all_cookies()
                self.driver.add_cookie({'name': self.cookie[0], 'value': self.cookie[1], 
                'domain': 'intranet.doktuz.com', 'path': '/', 'Expires': 'Session'})
            if(not self.driver.get_cookies()):
                logger.info('pdf from item with code {} has not been processed, not cookies'.format(item['code']))
            else:
                if(item['imp']!=None):
                    self.driver.get(item['imp'])
                    self.wait_for_ajax()
                    self.wait_for_loading_fade()
                    self.wait_until_images_loaded(self.driver)
                    self.print_page(item['codigo'] + '.pdf')
                    item['imp'] = item['codigo'] + '.pdf'
            del item['cookie']
            return item
        except Exception as e:
            logger.warning('item with code {} has not been save'.format(item['imp']), exc_info=True)
        
    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            logger.info('fail when waiting for ajax', exc_info=True)
            raise e

    def wait_for_loading_fade(self):
        try:
            #elements = self.driver.find_elements(by=By.CLASS_NAME, value='FacetDataTDM14')
            WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME,'FacetDataTDM14'), "Cargando..."))
        except Exception as e:
            logger.info('fail when waiting for loading fade', exc_info=True)
            raise e
        
    def print_page(self, file_name):
        try:
            self.driver.execute_script('document.title="{}";'.format(file_name)); 
            self.driver.execute_script("window.print();")
        except Exception as e:
            logger.info('fail when printing page', exc_info=True)
            raise e
    
    def create_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            logger.critical('fail when creating the pdf directory', exc_info=True)
            raise e

    def wait_until_images_loaded(self, driver, timeout=30):
        try:
            elements = self.driver.find_elements(by=By.TAG_NAME, value='img')
            WebDriverWait(self.driver, 30).until(lambda wd:self.all_array_elements_are_true(wd,elements) )
        except Exception as e:
            logger.info('fail when waiting for images to load', exc_info=True)
            raise e
            
    '''def get_dni(self):
        try:
            return self.driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtDni"]').get_attribute('value')
        except Exception as e:
            logger.info('fail when getting dni', exc_info=True)
            raise e'''

    def all_array_elements_are_true(self,driver, elements):
        array = [driver.execute_script("return arguments[0].complete", img) for img in elements]
        for element in array:
            if not element:
                return False
        return True