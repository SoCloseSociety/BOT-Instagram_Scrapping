from calendar import c
from email import message
from itertools import count
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import socket


from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
import pyautogui
import pyperclip
import csv
import pandas as pd
from glob import glob
import os 
import random
import pickle
import re, itertools
from lxml import etree

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")


insta_email = input("Enter insta usetername/email : ")
insta_password = input("Enter insta password : ")
fileName = input("Enter file name : ")



def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)


driver.find_element(By.NAME, 'username').send_keys(insta_email)
driver.find_element(By.NAME, 'password').send_keys(insta_password)
        
driver.find_element(By.XPATH, "//button[@type='submit']").click()
WebDriverWait(driver, 60000).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@id,'mount')]")))

cursor = input("Put your cursor on from where you want to scrap the  profile & press G :")

links = []

count = 0
prev_links_length = 0
now_links_length = 0

if(cursor == "G"):

    while(True):
        count = count + 1
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        for a in soup.find_all('a', href=True):
            if a['href'].count('/') == 2:
                links.append(a['href'])
        
        links = list(set(links))



        now_links_length = len(links)

        print(prev_links_length)
        print(now_links_length)

        if now_links_length == prev_links_length:
            if count % 2000 == 0 :
                break
        else:
            prev_links_length = now_links_length

        pyautogui.scroll(-1000)
        time.sleep(0.5)

        #print(len(links))
        df = pd.DataFrame({"Profilelink" : links})       
        df.to_csv(fileName+".csv", index=False)

driver.quit()