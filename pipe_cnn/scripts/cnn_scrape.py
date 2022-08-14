import bs4 as bs
import pickle
from bs4 import BeautifulSoup
import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta
import pickle

with open('../../global_data/date_list', 'wb') as f:
    date_list=pickle.load(f)

wb_url_list=[]
import time

# get wayback article url links
for ymd in date_list:
    try:
        url = f'http://archive.org/wayback/available?url=cnn.com&timestamp={ymd}'
        time.sleep(0.2)
        response = requests.get(url)
        data = response.json()
        wb_url_list.append(data["archived_snapshots"]["closest"]["url"])
    except:
        print(ymd)

wb_url_set=set(wb_url_list)
wb_cnn_url_list=list(wb_url_set)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# get actual url links
cnn_urls=[]
for wb_url in wb_cnn_url_list:
    success = 'yes'
    try:
        driver.get(wb_url)
    except:
        print(wb_url, "can't get page")
        success = 'no'
    if success == 'no':
        continue
    
    try:
        print('connected')
        elems = driver.find_elements(By.TAG_NAME, "a")
        links = [elem.get_attribute('href') for elem in elems]
    except:
        print(wb_url, "can't find links")
        success = 'no'
    if success == 'no':
        continue  
        
    try:
        for l in links:
            section_split = l.partition('www.cnn.com/')
            if section_split[2][:3].isdigit():
                cnn_urls_end.append(l)
    except:
        print(wb_url, "can't make new link")
        success = 'no'
    if success == 'no':
        continue  
cnn_urls_set = set(cnn_urls)
cnn_urls = list(cnn_url_set)

# parse, turn into df and save
cnn_articles=[]
c=0
for ur in cnn_urls:
    print(c)
    c+=1
    time.sleep(0.1)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    article_data=[]
    try:
        soup = BeautifulSoup(requests.get(ur, headers=headers, timeout=5).text, "html.parser")

    except:
        soup = 'fail'
  
    if soup == 'fail':
        print(ur, 'no cx')
        continue

    try:
        section = soup.find("meta", attrs={'name':"section"}).attrs['content']

    except:
        section = 'blank'
        print(ur, 'no section')
    try:
        headline = soup.find("meta", property="og:title").attrs['content']
    except:
        headline = 'blank'
        print(ur, 'no headline')
        
    try:
        date = soup.find("meta", property="og:pubdate").attrs['content']
    except:
        date='blank'
        print(ur, 'no date')
        
    try:
        first_par = soup.find("p", class_="zn-body__paragraph speakable").get_text()
        other_ps = soup.find_all("div", class_="zn-body__paragraph")
        body_string = first_par
        for p in other_ps:
            try:
                body = p.get_text()
                body_string += f" {body}"
            except:
                print(p)

    except:
        body_string='blank'

    article_data =[ur, section, headline, date, body_string]
    cnn_articles.append(article_data)
cnn_articles

cnn_articles_df = pd.DataFrame(cnn_articles, columns=['URL', 'category', 'headline', 'date', 'text'])

