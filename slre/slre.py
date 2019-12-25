from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import time
import subprocess
import requests
import zipfile
import os
import stat
import psutil
import sys
import shutil


if sys.platform == 'win32':
    chrome_driver = os.path.join(os.getcwd(), 'driver', 'chromedriver.exe')
else:
    chrome_driver = os.path.join(os.getcwd(), 'driver', 'chromedriver')
chrome_profile = os.path.join(os.getcwd(), 'profile')
if sys.platform == 'win32':
    google_command_string = 'START chrome.exe --remote-debugging-port=9223 --user-data-dir={0}'.format(chrome_profile)
else:
    google_command_string = 'google-chrome --remote-debugging-port=9223 --user-data-dir={0} &>/dev/null &'.format(chrome_profile)



class RemoteSelenium():
    def __init__(self,delete_profile = False):

        if delete_profile:
            quit_chrome_new_profile(chrome_profile)
        self.check_create_folders()
        launch_chrome_development()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "debuggerAddress", "127.0.0.1:9223")
        try:
            self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        except selenium.common.exceptions.WebDriverException as e:
            raise selenium.common.exceptions.WebDriverException("Please Download Chrome Driver And Place in driver folder ")
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")


    def check_create_folders(self):
        if os.path.exists(os.path.join(os.getcwd(), 'driver')):
            pass
        else:
            os.mkdir(os.path.join(os.getcwd(), 'driver'))

        if os.path.exists(os.path.join(os.getcwd(), 'profile')):
            pass
        else:
            os.mkdir(os.path.join(os.getcwd(),'profile'))


    def getsoup(self):
        sdriver = self.driver
        soup = BeautifulSoup(sdriver.page_source, 'html.parser')
        self.soup = soup
        return soup

    def getall_links(self, attr_name=None, attr_value=None, tagname='a', joinurls=True):
        soup = self.getsoup()
        all_links = []
        if attr_name and not attr_value:
            raise ValueError
        elif attr_value and not attr_name:
            raise ValueError

        if attr_name is None and attr_value is None:
            all_raw_data = soup.find_all(tagname)
            for link in all_raw_data:
                try:
                    ex_link = link['href']
                    all_links.append(ex_link)
                except KeyError:
                    pass
                    # No url
            if joinurls:
                return set([urljoin(self.driver.current_url, link) for link in all_links])
            return set(all_links)

        elif attr_name and attr_value:
            all_raw_data = soup.find_all(
                tagname, attrs={attr_name: attr_value})
            for link in all_raw_data:
                try:
                    ex_link = link['href']
                    all_links.append(ex_link)
                except KeyError:
                    pass
            if joinurls:
                return set([urljoin(self.driver.current_url, link) for link in all_links])
            return set(all_links)

    def textavailable(self, text_to_find):
        soup = self.getsoup()
        visible_text = u"".join(t.strip().lower()
                                for t in soup.findAll(text=True))
        return text_to_find.lower() in visible_text.lower()

    def get_one_element_by_attribute(self, tagname, attribute_name=None, attribute_value=None, soup=None):
        if soup is None:
            soup = self.getsoup()
        if attribute_name and not attribute_value:
            return ValueError
        elif attribute_value and not attribute_name:
            return ValueError
        elif tagname is None:
            return ValueError
        if tagname and attribute_name and attribute_value:
            try:
                return soup.find(tagname, attrs={attribute_name: attribute_value}).text.strip()
            except AttributeError:
                return None
        elif tagname and not attribute_name and not attribute_value:
            try:
                return soup.find(tagname).text.strip()
            except AttributeError:
                return None

    def handle_captcha(self):
        if self.textavailable('think you were a bot'):
            input("Bot Detection Triggered , Please Fix")
            self.handle_captcha()
        else:
            return True

    def click_by_text(self, next_page_text):
        nextpage_link = self.driver.find_element_by_link_text(next_page_text)
        nextpage_link.click()

    def click_by_css(self,css_selector):
        element = self.driver.find_element_by_css_selector(css_selector)
        element.click()
    def set_text(self,tagname , attributes =None):
        #tbox = self.driver.find_elements_by_css_selector(f'{tagname}[]')
        pass
    # box= rs.driver.find_element_by_css_selector('input[id="twotabsearchtextbox"]')

    def random_website(self, driver=None):
        # This will navigate to other websites sometime
        ghost_links = ''
        with open('ghostlinks.txt', 'r') as file:
            file_data = file.read()
            ghost_links = file_data.split(',')
        should_launch = bool(random.getrandbits(1))
        if should_launch:
            if driver is None:
                driver = self.driver
                driver.get(random.choice(ghost_links))
                time.sleep(random.randint(1, 10))

    def write_soup_to_file(self, filename, soup=None):
        if soup is None:
            soup = self.getsoup()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))


def launch_chrome_development():

    all_process = list(psutil.process_iter())
    if sys.platform == 'win32':
        run_status = 'chrome.exe' in (p.name() for p in all_process)
    else:
        run_status = 'chrome' in (p.name() for p in all_process)
    #print(run_status)

    if sys.platform == 'win32':
        pass
    else:
        os.chmod(chrome_driver, stat.S_IRWXU)

    if not run_status:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    else:
        print("Chrome Instance Already Running")
        return "Chrome Instance Already Running"

def quit_chrome_new_profile(profilename):

    all_process = list(psutil.process_iter())
    if sys.platform == 'win32':
        run_status = 'chrome.exe' in (p.name() for p in all_process)
    else:
        run_status = 'chrome' in (p.name() for p in all_process)
    #print(run_status)

    #If chrome is not running then do nothing
    if run_status:
        pass
    else:
        if os.path.exists(os.path.join(os.getcwd(), profilename)):
            shutil.rmtree(os.path.join(os.getcwd(), profilename))
        else:
            pass
        return
    

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    try:
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        driver.close()
        driver.quit()
    except selenium.common.exceptions.WebDriverException as e:
        raise selenium.common.exceptions.WebDriverException("Please Download Chrome Driver And Place in driver folder ") 
    
    time.sleep(3)
    if os.path.exists(os.path.join(os.getcwd(), profilename)):
        shutil.rmtree(os.path.join(os.getcwd(), profilename))
    else:
        pass


if __name__ == '__main__':
    rs = RemoteSelenium(True)

    