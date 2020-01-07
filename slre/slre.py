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
import socket
    

def open_port():
    all_ports = []
    for i in range(5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        all_ports.append(port)
    return set(all_ports)





class RemoteSelenium():
    def __init__(self,delete_profile = False,port_number=9223):
        self.port_number= port_number
        self.chrome_profile = os.path.join(os.getcwd(), 'profile')
        self.chrome_driver = os.path.join(os.getcwd(), 'driver', 'chromedriver.exe')
        self.google_command_string = f'START chrome.exe --remote-debugging-port={self.port_number} --user-data-dir={self.chrome_profile}'

        if delete_profile:
            quit_chrome_new_profile(self.chrome_profile,port_number=self.port_number,chrome_driver=self.chrome_driver)
        self.check_create_folders()
        launch_chrome_development(self.google_command_string)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port_number}")
        try:
            self.driver = webdriver.Chrome(self.chrome_driver, options=chrome_options)
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

    def scroll_down(self):
    #Credits : https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-indynamically-loading-webpage
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    


def launch_chrome_development(google_command_string):

    all_process = list(psutil.process_iter())
    if sys.platform == 'win32':
        run_status = 'chrome.exe' in (p.name() for p in all_process)
    else:
        run_status = 'chrome' in (p.name() for p in all_process)
    #print(run_status)
    if not run_status:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    else:
        print("Chrome Instance Already Running")
        return "Chrome Instance Already Running"

def quit_chrome_new_profile(profilename,port_number,chrome_driver):

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
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port_number}")
    try:
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        driver.close()
        driver.quit()
    except selenium.common.exceptions.WebDriverException as e:
        raise e("Please Download Chrome Driver And Place in driver folder ") 
    
    time.sleep(3)
    if os.path.exists(os.path.join(os.getcwd(), profilename)):
        shutil.rmtree(os.path.join(os.getcwd(), profilename))
    else:
        pass


if __name__ == '__main__':
    rs = RemoteSelenium(delete_profile=False)
    #print(open_port())

    