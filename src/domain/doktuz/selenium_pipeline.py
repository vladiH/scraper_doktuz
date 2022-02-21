import os
import json
import datetime
import time
from base64 import b64decode
from config import Config, Logger
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
class DoktuzSeleniumPipeline:
    def __init__(self,driver_path, local_dir):
        self.driver_path = driver_path
        self.local_dir = local_dir
        self.cookie = None
        self.tmp_file_name = "file.pdf"
    def open_spider(self, spider):
        try:
            self.local_dir = self.local_dir
            self.create_directory(self.local_dir)
            self.setup_driver()
        except Exception as e:
            Logger.critical("DoktuzSeleniumPipeline.open_spider: fail when spider was opening selenium driver", exc_info=True)
            raise e

    def setup_driver(self):
        try:
            if Config.BROWSER == 'chrome':
                self.setup_chrome_driver()
            elif Config.BROWSER == 'firefox':
                self.setup_motzilla_driver()
            else:
                raise Exception("browser not supported")
            #self.driver.set_page_load_timeout(60)
            #self.driver.set_script_timeout(60)
            if self.cookie is not None:
                self.driver.delete_all_cookies()
                self.driver.add_cookie({'name': self.cookie[0], 'value': self.cookie[1], 
                    'domain': 'intranet.doktuz.com', 'path': '/'})
        except Exception as e:
            Logger.critical('DoktuzSeleniumPipeline.setup_driver: {}'.format(e))
            raise e

    def close_spider(self, spider):
        self.driver.quit()
        
    @classmethod
    def from_crawler(cls, crawler):
        dp = Config.DRIVER_PATH
        return cls(
            driver_path=dp,
            local_dir = Config.PDF_OUTPUT_PATH
        )

    async def process_item(self, item, spider):
        try:
            if item!= None:
                Logger.info("Processing item: {}".format(item))
                if(self.cookie==None or self.driver.get_cookies()==[]):
                    self.cookie = item['cookie'].split('=')
                    self.driver.get('https://intranet.doktuz.com/Resultados/Empresa/resultados.php')
                    self.driver.delete_all_cookies()
                    self.driver.add_cookie({'name': self.cookie[0], 'value': self.cookie[1], 
                    'domain': 'intranet.doktuz.com', 'path': '/'})
                if(not self.driver.get_cookies()):
                    Logger.warning('DoktuzSeleniumPipeline.process_item: pdf has not been processed, not cookies. {}'.format(item))
                else:
                    dir_name = self.local_dir+'/'+item['codigo']
                    if('certificado' in item and item['certificado_downloaded']==False):
                        self.page_as_pdf(item['certificado'],dir_name,item['codigo']+"-certificado.pdf")
                        item['certificado_downloaded'] = True
                        item['certificado'] = item['codigo']+"-certificado.pdf"
                    if('imp' in item and item['imp_downloaded']==False):
                        self.page_as_pdf(item['imp'],dir_name,item['codigo']+"-imp.pdf")
                        item['imp_downloaded'] = True
                        item['imp'] = item['codigo']+"-imp.pdf"
        except Exception as e:
            Logger.error('DoktuzSeleniumPipeline.process_item: pdf has not been processed. {}, error:{}'.format(item, e))
            #self.setup_driver()
            Logger.warning('DoktuzSeleniumPipeline.page_as_pdf: driver seccessfully restarted')
        finally:
            if item!=None:
                item['fecha_downloaded'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                del item['cookie']
            return item

    def setup_chrome_driver(self):
        try:
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"  #  complete
            chrome_options = webdriver.ChromeOptions()
            settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF", "version": 2}
            prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument('--dns-prefetch-disable')
            chrome_options.add_argument("--aggressive-cache-discard")
            if Config.HIDDEN:
                chrome_options.add_argument('--single-process') # this option is not working for windows
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--kiosk-printing')
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options, desired_capabilities=caps,
            service_args=["--verbose", "--log-path=K:\WORKS\PYTHON\SIMPLEXGO\scraper_doktuz\pdfs\qc1.log"])
        except Exception as e:
            raise e

    def setup_motzilla_driver(self):
        try:
            caps = DesiredCapabilities().FIREFOX
            caps["pageLoadStrategy"] = "normal"  # eager none
            motzilla_options = webdriver.FirefoxOptions()
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0'
            motzilla_options.set_preference('profile_options = FirefoxProfile()', user_agent)

            motzilla_options.set_preference("print_printer", "PDF")

            motzilla_options.set_preference("print.always_print_silent", True)
            motzilla_options.set_preference("print.show_print_progress", False)
            motzilla_options.set_preference('print.save_as_pdf.links.enabled', True)
            motzilla_options.set_preference('print.tab_modal.enabled', False)

            motzilla_options.set_preference("print.printer_PDF.print_to_file", True)

            motzilla_options.set_preference('print.printer_PDF.print_to_filename', "testprint.pdf")

            motzilla_options.set_preference('print.printer_PDF.print_to_filename',self.local_dir+"/"+ self.tmp_file_name)
            motzilla_options.set_preference('print.printer_PDF.print_paper_size_unit',1)
            motzilla_options.set_preference('print.printer_PDF.print_bgcolor',True)
            motzilla_options.set_preference('print.printer_PDF.print_paper_height',"297")
            motzilla_options.set_preference('print.printer_PDF.print_paper_width',"210")
            #motzilla_options.set_preference('print.printer_PDF.print_resolution',1200)
            motzilla_options.set_preference('print.printer_PDF.print_shrink_to_fit',True)
            motzilla_options.set_preference('print.printer_PDF.print_paper_id','iso_a4')
            motzilla_options.set_preference('print.printer_PDF.print_margin_bottom',"0.2")
            motzilla_options.set_preference('print.printer_PDF.print_margin_top',"0.2")
            motzilla_options.add_argument('--no-sandbox')
            motzilla_options.add_argument('--disable-dev-shm-usage')
            if Config.HIDDEN:
                motzilla_options.add_argument('--headless')
                motzilla_options.add_argument("--disable-gpu")
            self.driver = webdriver.Firefox(executable_path=self.driver_path, options=motzilla_options, desired_capabilities=caps)
        except Exception as e:
            raise e

    def page_as_pdf(self, link, dir_name, file_name):
        try:
            self.driver.execute_script('''window.open();''')
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(link)
            self.wait_for_body()
            self.wait_for_ajax()
            self.wait_for_loading_fade()
            self.wait_until_images_loaded(self.driver)
            if Config.BROWSER == 'chrome':
                if Config.HIDDEN:
                    self.create_chrome_pdf(self.driver, file_name)
                    #self.print_headless_chrome_page(file_name, link)
                else:
                    self.print_chrome_page(file_name)
            elif Config.BROWSER == 'firefox':
                #self.create_chrome_pdf(self.driver, file_name)
                self.print_motzilla_page(file_name)
                self.rename_file(self.tmp_file_name, file_name)
            else:
                raise Exception('DoktuzSeleniumPipeline.page_as_pdf: browser not supported')
        except Exception as e:
            Logger.error('conversion error: {}'.format(e))
            raise e
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])  
           

    def wait_for_body(self):
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException as e:
            Logger.error('DoktuzSeleniumPipeline.wait_for_body: timeout waiting for body')

    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 60)
        try:
            is_jquery_present = self.driver.execute_script("return (typeof jQuery != 'undefined');")
            if is_jquery_present:
                wait.until(lambda driver: driver.execute_script("return !!window.jQuery && window.jQuery.active == 0"))
        except Exception as e:
            Logger.error('waiting error, ajax code error {}'.format(e), exc_info=True)

    def wait_for_loading_fade(self):
        try:
            #elements = self.driver.find_elements(by=By.CLASS_NAME, value='FacetDataTDM14')
            #print(self.driver.__sizeof__())
            #WebDriverWait(self.driver, 60, poll_frequency=0.1, ignored_exceptions=None).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME,'FacetDataTDM14'), "Cargando..."))
            '''
            file = open("sample.html","w")
            l = self.driver.page_source
            file.write(l)
            file.close()
            '''
            WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME,'imgLOAD')))
            WebDriverWait(self.driver, 60).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME,'FacetDataTDM14'), 'Cargando...'))
        except TimeoutException as timeout:
             Logger.error('waiting error, timeout loading fade error {}'.format(timeout))
             raise timeout
        except Exception as e:
            Logger.error('waiting error, loading fade error {}'.format(e))
            raise e
        
    def print_motzilla_page(self, file_name):
        try:
            # Define Configurations
            #self.driver.execute_script('document.title="{}";'.format(file_name)); 
            #self.driver.execute_script("window.print();")
            #save_me = ActionChains(self.driver).key_down(Keys.CONTROL)\
            element_search_field = self.driver.find_element_by_tag_name('body')
            element_search_field.send_keys('TSLA')
            element_search_field.send_keys(Keys.ENTER)
            self.driver.execute_script("window.print()")
            WebDriverWait(self.driver, 60).until(lambda wd:self.check_download_file_size(self.tmp_file_name) )
        except Exception as e:
            Logger.error('printing PDF error {}'.format(e))
            raise e

    def print_chrome_page(self, file_name):
        try:
            self.driver.execute_script('document.title="{}";'.format(file_name)); 
            self.driver.execute_script("window.print();")
        except Exception as e:
            Logger.error('printing PDF error {}'.format(e))
            raise e

    def print_headless_chrome_page(self, file_name, link):
        try:
            page = self.driver.execute_cdp_cmd( "Page.printToPDF", {'path': link, 
                                                                    'format': 'A4', 'landscape': False,
                                                                    'paperWidth': 8.27,
                                                                    'paperHeight': 11.69})
            # Define the Base64 string of the PDF file
            b64 = page['data']

            # Decode the Base64 string, making sure that it contains only valid characters
            bytes = b64decode(b64, validate=True)

            # Perform a basic validation to make sure that the result is a valid PDF file
            # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
            # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
            if bytes[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')
            # Write the PDF contents to a local file
            f = open(self.local_dir+'/'+file_name, 'wb')
            f.write(bytes)
            f.close()
        except Exception as e:
            Logger.error('printing headless PDF error {}'.format(e), exc_info=True)
            raise e
    
    def create_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            Logger.error('creation error, creating directory', exc_info=True)
            raise e

    def rename_file(self, name, new, iter=10):
        try:
            time.sleep(2)
            if iter == 0:
                raise Exception('renaming error, file not renamed')
            else:
                try:
                    os.rename(self.local_dir+'/'+name, self.local_dir+'/'+new)
                except FileExistsError:
                    os.remove(self.local_dir+'/'+new)
                    self.rename_file(name, new, iter-1)
                except Exception as e:
                    Logger.debug(e)
                    self.rename_file(name, new, iter-1)

        except Exception as e:
            Logger.error('renaming error, renaming file', exc_info=True)
            raise e
            

    def check_download_file_size(self, file_name):
        try:
            time.sleep(1)
            file_size = os.path.getsize(self.local_dir+'/'+file_name)
            if file_size == 0:
                return False
            return True
        except Exception as e:
            Logger.error('checking file size error {}'.format(e))
            raise e

    def wait_until_images_loaded(self, driver, timeout=120):
        try:
            elements = self.driver.find_elements(by=By.TAG_NAME, value='img')
            WebDriverWait(self.driver, timeout).until(lambda wd:self.all_array_elements_are_true(wd,elements) )
        except Exception as e:
            Logger.error('waiting image error  {}'.format(e), exc_info=True)
            raise e

    def all_array_elements_are_true(self,driver, elements):
        try:
            array = [driver.execute_script("return arguments[0].complete", img) for img in elements]
            for element in array:
                if not element:
                    return False
            return True
        except Exception as e:
            Logger.error('all_array_elements_are_true:  {}'.format(e), exc_info=True)
            return False
    
    def send_devtools(self, driver, command, params={}):
        try:
            resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
            url = driver.command_executor._url + resource
            body = json.dumps({"cmd": command, "params": params})
            resp = driver.command_executor._request("POST", url, body)
            return resp.get("value")
        except Exception as e:
            raise e

    def send_devtools_firefox(self, driver, command, params={}):
        try:
            resource = "/session/%s/moz/send_command_and_get_result" % driver.session_id
            url = driver.command_executor._url + resource
            command = 'send_command'
            driver.command_executor._commands['send_command'] = ('POST', url)
            body = json.dumps({"cmd": command, "params": params})
            resp = self.driver.execute(command)
            return resp.get("value")
        except Exception as e:
            raise e


    def create_chrome_pdf(self, driver, file_name):
        try:
            command = "Page.printToPDF"
            params = {'paper_width': '8.27', 'paper_height': '11.69'}
            result = self.send_devtools_firefox(driver, command,  params)
            self.save_pdf(result, file_name)
            return
        except Exception as e:
            Logger.error('send_devtools:  {}'.format(e), exc_info=True)
            raise e


    def save_pdf(self, data, file_name):
        try:
            name = self.local_dir+'/'+file_name
            with open(name, 'wb') as file:
                file.write(b64decode(data['data']))
            #print('PDF created')
        except Exception as e:
            raise e