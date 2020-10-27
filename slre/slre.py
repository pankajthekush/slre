from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.parse import urljoin
import random
import time
import subprocess
import requests
import zipfile
import os,inspect
import stat
import sys
import shutil
import socket
from shelp2 import copy_file_to_no_tk
from pathlib import Path
#import logging


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)



current_path =  str(Path.home())


    

def open_ports():
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
    def __init__(self,port_number=54420,headless=False,proxy_host=None,proxy_port=None):
        self.port_number= port_number
        self.chrome_profile = os.path.join(current_path, str(self.port_number))
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

        self.chrome_driver = os.path.join(current_path,str(port_number), 'driver', 'chromedriver')
        self.google_command_string = f'google-chrome --remote-debugging-port={self.port_number} --no-sandbox --allow-running-insecure-content --no-first-run  --disable-gpu --disable-software-rasterizer --user-data-dir={self.chrome_profile}&'
             
        self.check_create_folders(profile_name=str(self.port_number))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port_number}")
        chrome_options.add_argument("--ignore-certificate-errors")

        if self.proxy_host is not None:
            chrome_options.add_argument('--proxy-server={host}:{port}'.format(host=self.proxy_host, port=self.proxy_port))

        print("Launching Chrome")
        launch_chrome_development(self.google_command_string,override=True)
        self.driver = webdriver.Chrome(self.chrome_driver, options=chrome_options)
        
        
    def check_create_folders(self,profile_name):
        if os.path.exists(os.path.join(current_path,str(self.port_number))):
            pass
        else:
            os.mkdir(os.path.join(current_path,str(self.port_number)))
        if sys.platform == 'linux':
            #copy chromedriver for linux

            if os.path.exists(os.path.join(current_path, profile_name,'driver')):
                copy_file_to_no_tk(os.path.join(current_path, profile_name,'driver','chromedriver'))
            else:
                os.mkdir(os.path.join(current_path,profile_name,'driver'))
                copy_file_to_no_tk(os.path.join(current_path, profile_name,'driver','chromedriver'))


        else:
            #for windows
            if os.path.exists(os.path.join(current_path, profile_name,'driver')):
                copy_file_to_no_tk(os.path.join(current_path, profile_name,'driver','chromedriver.exe'))
            else:
                os.mkdir(os.path.join(current_path,profile_name,'driver'))
                copy_file_to_no_tk(os.path.join(current_path, profile_name,'driver','chromedriver.exe'),title_text="Choose Chromedriver.exe")

    def clean_profile(self):
        self.driver.get('https://example.com/')
        self.driver.delete_all_cookies()
        self.driver.get('chrome://settings/clearBrowserData')
        
        sleep(3)
        
        try:
            self.driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
        except Exception:
            print("Failed to Clear history")
        
        #close tab to clean local data
        
        curr_tab = self.driver.window_handles[0]
        self.driver.execute_script('window.open("https://www.google.com")')
        #logging.debug("Opening new tab")
        self.driver.switch_to.window(window_name=curr_tab)
        self.driver.close()
        curr_tab = self.driver.window_handles[0]
        self.driver.switch_to.window(window_name=curr_tab)

       #Open a new window


    def remove_profile_folder(self):
        os.system("killall -KILL chromedriver") 
        os.system("killall -KILL chrome") 
        os.system("killall -KILL chromedriver") 
        os.system("killall -KILL chrome") 
        if os.path.exists(os.path.join(current_path,str(self.port_number))):
            try:
                shutil.rmtree(os.path.join(current_path,str(self.port_number)))
            except Exception:
                print('could not remove profile')



    #Credits : https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-indynamically-loading-webpage
    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to(self,points=500):
         self.driver.execute_script(f"window.scrollTo(0, {points});")

    def scroll_down_lazy(self,points=500):
        total_height = self.driver.execute_script(" return document.body.scrollHeight;")
        counter = 100
        while counter < total_height:
            self.driver.execute_script(f"window.scrollTo(0, {counter});")
            counter += 500
            total_height = self.driver.execute_script(" return document.body.scrollHeight;")
            time.sleep(1)



def launch_chrome_development(google_command_string,override=False):

    if  override == False:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    elif override==True:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    


def list_availble_profiles():
    current_path = os.path.dirname(os.path.abspath(__file__))
    dict_profiles = dict()
    c_profiles = os.listdir(current_path)
    r_profiles = [profile for profile in c_profiles if profile.isdigit()]

    for profile in r_profiles:
        lock_file = os.path.join(current_path,profile,'lockfile')
        curr_loc_file_state = 'INUSE' if os.path.exists(lock_file) else 'AVAILABLE'
        dict_profiles[profile] = curr_loc_file_state

    return dict_profiles


if __name__ == '__main__':
    rs = RemoteSelenium()
    rs.driver.get('https://www.google.com')
    input('here')
    print(rs.driver.page_source)
    rs.remove_profile_folder()