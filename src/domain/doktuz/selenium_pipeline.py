import os
import json
from config import Config, Logger
from selenium import webdriver
from textwrap import dedent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class DoktuzSeleniumPipeline:
    def __init__(self,driver_path, local_dir):
        self.driver_path = driver_path
        self.local_dir = local_dir
        self.cookie = None

    def open_spider(self, spider):
        try:
            self.local_dir = self.local_dir + '/pdfs'
            self.create_directory(self.local_dir)
            chrome_options = webdriver.ChromeOptions()
            settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF", "version": 2}
            prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'savefile.default_directory': self.local_dir}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            #chrome_options.add_argument('--headless')
            chrome_options.add_argument('--kiosk-printing')
            
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
        except Exception as e:
            Logger.critical("DoktuzSeleniumPipeline.open_spider: fail when spider was opening selenium driver", exc_info=True)
            raise e

    def close_spider(self, spider):
        self.driver.close()
        
    @classmethod
    def from_crawler(cls, crawler):
        dp = Config.DRIVER_PATH
        return cls(
            driver_path=dp,
            local_dir = os.getcwd()
        )

    async def process_item(self, item, spider):
        try:
            Logger.info("Processing item: {}".format(item))
            if(self.cookie==None):
                self.cookie = item['cookie'].split('=')
                self.driver.get(item['imp'])
                self.driver.delete_all_cookies()
                self.driver.add_cookie({'name': self.cookie[0], 'value': self.cookie[1], 
                'domain': 'intranet.doktuz.com', 'path': '/', 'Expires': 'Session'})
            if(not self.driver.get_cookies()):
                Logger.warning('DoktuzSeleniumPipeline.process_item: pdf has not been processed, not cookies. {}'.format(item))
            else:
                dir_name = self.local_dir+'/'+item['codigo']
                if(item['imp']!=None):
                    self.page_as_pdf(item['imp'],dir_name,item['codigo']+"-imp.pdf")
                    item['imp_downloaded'] = True
                    item['imp'] = item['codigo']+"-imp.pdf"
                if(item['certificado']!=None):
                    self.page_as_pdf(item['certificado'],dir_name,item['codigo']+"-certificado.pdf")
                    item['certificado_downloaded'] = True
                    item['certificado'] = item['codigo']+"-certificado.pdf"
        except Exception as e:
            Logger.error('DoktuzSeleniumPipeline.process_item: pdf has not been processed. {}'.format(item), exc_info=True)
        finally:
            del item['cookie']
            return item
    def page_as_pdf(self, link, dir_name, file_name):
        try:
            self.driver.get(link)
            #self.wait_for_ajax()
            self.wait_for_loading_fade()
            self.wait_until_images_loaded(self.driver)
            #self.create_directory(dir_name)
            self.print_page(file_name)
        except Exception as e:
            Logger.error('fail when pages is converted as pdf')
            raise e   

    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            Logger.error('fail when waiting for ajax')
            raise e

    def wait_for_loading_fade(self):
        try:
            #elements = self.driver.find_elements(by=By.CLASS_NAME, value='FacetDataTDM14')
            WebDriverWait(self.driver, 30).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME,'FacetDataTDM14'), "Cargando..."))
        except Exception as e:
            Logger.error('fail when waiting for loading fade')
            raise e
        
    def print_page(self, file_name):
        try:
            self.driver.execute_script('document.title="{}";'.format(file_name)); 
            self.driver.execute_script("window.print();")
        except Exception as e:
            Logger.error('fail when printing page')
            raise e
    
    def create_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            Logger.error('fail when creating the pdf directory', exc_info=True)
            raise e

    def wait_until_images_loaded(self, driver, timeout=30):
        try:
            elements = self.driver.find_elements(by=By.TAG_NAME, value='img')
            WebDriverWait(self.driver, 30).until(lambda wd:self.all_array_elements_are_true(wd,elements) )
        except Exception as e:
            Logger.error('fail when waiting for images to load')
            raise e

    def all_array_elements_are_true(self,driver, elements):
        array = [driver.execute_script("return arguments[0].complete", img) for img in elements]
        for element in array:
            if not element:
                return False
        return True