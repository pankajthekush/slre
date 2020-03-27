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
import psutil
import sys
import shutil
import socket
#import logging

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from shelp import copy_file_to

current_path = os.path.dirname(os.path.abspath(__file__))


    

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
    def __init__(self,delete_profile = False,port_number=92223,headless=False):
        self.port_number= port_number
        self.chrome_profile = os.path.join(current_path, str(self.port_number))
        self.chrome_driver = os.path.join(current_path,str(port_number), 'driver', 'chromedriver.exe')

        if headless == False:
            self.google_command_string = f'START chrome.exe --remote-debugging-port={self.port_number} --user-data-dir={self.chrome_profile}'
        else:
            self.google_command_string = f'START chrome.exe --headless --disable-gpu --remote-debugging-port={self.port_number} --user-data-dir={self.chrome_profile}'


        if delete_profile:
            quit_chrome_new_profile(self.chrome_profile,port_number=self.port_number,chrome_driver=self.chrome_driver)
        self.check_create_folders(profile_name=str(self.port_number))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port_number}")
        
        try:
            print("Launching Chrome,This will take some time...")
            self.driver = webdriver.Chrome(self.chrome_driver, options=chrome_options)
        except selenium.common.exceptions.WebDriverException:
            print("Launching Chrome")
            launch_chrome_development(self.google_command_string,override=True)
            self.driver = webdriver.Chrome(self.chrome_driver, options=chrome_options)
        
        
    def check_create_folders(self,profile_name):
        if os.path.exists(os.path.join(current_path,str(self.port_number))):
            pass
        else:
            os.mkdir(os.path.join(current_path,str(self.port_number)))

        if os.path.exists(os.path.join(current_path, profile_name,'driver')):
            copy_file_to(os.path.join(current_path, profile_name,'driver','chromedriver.exe'))
        else:
            os.mkdir(os.path.join(current_path,profile_name,'driver'))
            copy_file_to(os.path.join(current_path, profile_name,'driver','chromedriver.exe'),title_text="Choose Chromedriver.exe")


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


def clean_profile(remoteselenium = None):
    remoteselenium.driver.get('https://example.com/')
    remoteselenium.driver.delete_all_cookies()
    remoteselenium.driver.get('chrome://settings/clearBrowserData')
    sleep(3)
    
    try:
        remoteselenium.driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
    except Exception:
        print("Failed to Clear history")
    
    #close tab to clean local data
    
    curr_tab = remoteselenium.driver.window_handles[0]
    remoteselenium.driver.execute_script('window.open("https://www.google.com")')
    #logging.debug("Opening new tab")
    remoteselenium.driver.switch_to.window(window_name=curr_tab)
    remoteselenium.driver.close()
    curr_tab = remoteselenium.driver.window_handles[0]
    remoteselenium.driver.switch_to.window(window_name=curr_tab)

    #Open a new window


def launch_chrome_development(google_command_string,override=False):

    if  override == False:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    elif override==True:
        os.system(google_command_string)
        print('Started  google-chrome run command')
        return "Started google-chrome run command"
    

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
        if os.path.exists(os.path.join(current_path, profilename)):
            shutil.rmtree(os.path.join(current_path, profilename))
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
        raise (e + "Please Download Chrome Driver And Place in driver folder ") 
    
    time.sleep(3)
    if os.path.exists(os.path.join(current_path, profilename)):
        shutil.rmtree(os.path.join(current_path, profilename))
    else:
        pass


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
    rs = RemoteSelenium(port_number=54421)
    rs.driver.get('https://www.nokia.com')
     