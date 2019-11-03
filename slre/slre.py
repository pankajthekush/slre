from selenium import webdriver
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

currdir = os.path.dirname(os.path.realpath(__file__))
chrome_driver = '{}/driver/chromedriver'.format(currdir)
chrome_profile = '{}/resources'.format(currdir)
google_command_string = 'google-chrome --remote-debugging-port=9223 --user-data-dir={0} &>/dev/null &'.format(chrome_profile)
print(chrome_profile)


class RemoteSelenium():
    def __init__(self, beginurl='https://www.google.com'):
        download_driver()
        launch_chrome_development()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "debuggerAddress", "127.0.0.1:9223")
        chrome_driver = '{}/driver/chromedriver'.format(currdir)
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        self.driver.get(beginurl)
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

    def getsoup(self):
        sdriver = self.driver
        soup = BeautifulSoup(sdriver.page_source, 'html.parser')
        self.soup = soup
        return soup

    def getall_links(self, attr_name=None, attr_value=None, tagname='a', joinurls=False):
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

    def navigate_to_next_page(self, next_page_tag, next_page_attrib_name, next_page_attrib_value):
        soup = self.getsoup()
        next_pagae_element = soup.find(
            next_page_tag, attrs={next_page_attrib_name: next_page_attrib_value})
        next_pagae_element = next_pagae_element.find('a')['href']
        next_pagae_element = urljoin(
            self.driver.current_url, next_pagae_element)
        self.driver.get(next_pagae_element)
        if self.handle_captcha():
            time.sleep(random.randint(5, 10))

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




def download_driver():
    if os.path.exists(chrome_driver):
        print("Chrome Driver Already in Folder")
        return "Chrome Driver Already in Folder"

    chrome_version = subprocess.check_output(
        ['google-chrome', '--version']).decode("utf-8").replace('Google Chrome', '').strip()
    download_string = 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_linux64.zip'.format(
        chrome_version)
    print("Driver will be downloaded from {0} :".format(download_string))
    r = requests.get(download_string)
    with open('{}/driver/chromedriver.zip'.format(currdir), 'wb') as f:
        f.write(r.content)
# unzip

    with zipfile.ZipFile('{0}/driver/chromedriver.zip'.format(currdir), 'r') as zip_file:
        zip_file.extractall('{0}/driver'.format(currdir))
    os.remove('{}/driver/chromedriver.zip'.format(currdir))
    print("Download Chrome Driver in driver folder")
    return "Download Chrome Driver in driver folder"


def launch_chrome_development():
    all_process = list(psutil.process_iter())
    run_status = 'chrome' in (p.name() for p in all_process)
    os.chmod(chrome_driver, stat.S_IRWXU)
    if not run_status:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    else:
        print("Chrome Instance Already Running")
        return "Chrome Instance Already Running"


if __name__ == '__main__':
    rs = RemoteSelenium()
    rs.driver.get('https://www.google.com')
