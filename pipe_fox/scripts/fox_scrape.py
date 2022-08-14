#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bs4 as bs
import pickle
from bs4 import BeautifulSoup
import requests
import time
from collections import Counter
import pandas as pd


# In[3]:


with open('date_list', 'rb') as fu:
    date_list = pickle.load(fu)   


# In[4]:


wb_fox_urls=[]

for ymd in date_list:
    try:
        url = f'http://archive.org/wayback/available?url=foxnews.com&timestamp={ymd}'
        response = requests.get(url)
        data = response.json()
        wb_fox_url_list.append(data["archived_snapshots"]["closest"]["url"])
    except:
        print(ymd)

wb_fox_urls_set=set(wb_fox_urls)
wb_fox_urls=list(wb_fox_urls_set)


# In[55]:


fox_urls=[]
part_list = ['http://smallbusiness.foxbusiness', 'https://smallbusiness.foxbusiness', 'http://www.foxnews.com', 'https://www.foxnews.com']
date_holder =[]

for wb_url in wb_fox_urls:
    success = 'yes'
    
    try:
        soup = BeautifulSoup(requests.get(wb_url).content, "html.parser")
        href_list = []
        for a in soup.find_all('a', href=True): 
            raw_fox_url = (a['href'])
            date_tuple = raw_fox_url.partition('.org/web/')
            date = f'{date_tuple[2][:4]}/{date_tuple[2][4:6]}'
            date_holder.append(date)
            href_list.append(raw_fox_url)
        occurence_count = Counter(date_holder)
        common = occurence_count.most_common(1)[0][0]
            
        for href in href_list:
            for part in part_list:     
                raw_tuple = href.partition(part)
                if raw_tuple[1][:4] == 'http':
                    raw_url = raw_tuple[1]+raw_tuple[2]
                    if common in raw_url and 'intcmp=trending' not in raw_url and 'opinion' not in raw_url and 'intcmp=latestnews'not in raw_url and 'on-air' not in raw_url and 'personal-finance' not in raw_url: 
                        fox_urls.append(raw_url)
                    elif '-' in raw_tuple[2]:
                        counter = raw_tuple[2].count('-')
                        if counter >3:
                            fox_urls.append(raw_url)
                        

    except:
        print(wb_url, 'no links')
        success = 'no'
    
    if success == 'no':
        continue
        
fox_urls_set = set(fox_urls)
fox_urls = list(fox_urls_set)


# In[7]:


fox_articles=[]

time.sleep(0.05)
for ur in fox_urls:
    article_data=[]
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        soup = BeautifulSoup(requests.get(ur, headers=headers, timeout=5).text, "html.parser")

    except:
        soup = 'fail'
  
    if soup == 'fail':
        print(ur, 'no cx')
        continue

    try:
        section = soup.find("meta", attrs={'data-hid':"prism.section"}).attrs['content']

    except:
        section = 'blank'
        print(ur, 'no section')

    try:
        headline = soup.find("meta", attrs={'data-hid':"dc.title"}).attrs['content']
    except:
        headline = 'blank'
        print(ur, 'no headline')
    try:
        dt = soup.find("meta", attrs={'data-hid':"dc.date"}).attrs['content']
    except:
        dt='blank'
        print(ur, 'no date')
    try:
        all_divs = soup.find('body')
        div = all_divs.find(class_="article-body")
        all_ps = div.find_all("p")
        body_string = ''
        for pp in all_ps:
            italic = pp.find('i')
            if italic:
                continue
            try:
                children = pp.findChildren()
                any_strong='no'
                for child in children:
                    strong = child.find('strong')
                    if strong:
                        any_strong='yes'
                if 'data-v-13907676' in pp.attrs or any_strong =='yes':
                    continue
                body = pp.get_text()
                if 'CLICK HERE TO GET THE FOX NEWS APP' in body:
                    continue
                to_add = f' {body}'
                body_string += to_add
            except:
                print(pp)
    except:
        body_string='blank'

    article_data =[ur, section, headline, dt, body_string]
    fox_articles.append(article_data)


# In[ ]:


fox_articles_df = pd.DataFrame(fox_articles, columns=['URL', 'category', 'headline', 'date', 'text'])


# In[14]:


with open('articles/fox_articles_df', 'rb') as f:
    pickle.dump(fox_articles_df, f)


# In[ ]:





# In[3]:


with open('../Reserves/fox_url_list', 'rb') as f:
    fox_url_list=pickle.load(f)


# In[4]:


fox_url_list


# In[ ]:


fox_ur_tweet=[]

for ur in fox_url_list:
    article_data=[]
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        soup = BeautifulSoup(requests.get(ur, headers=headers, timeout=5).text, "html.parser")

    except:
        soup = 'fail'
  
    if soup == 'fail':
        print(ur, 'no cx')
        continue

    try:
        section = soup.find("meta", attrs={'data-hid':"prism.section"}).attrs['content']

    except:
        section = 'blank'
        print(ur, 'no section')

    try:
        headline = soup.find("meta", attrs={'data-hid':"dc.title"}).attrs['content']
    except:
        headline = 'blank'
        print(ur, 'no headline')
    try:
        dt = soup.find("meta", attrs={'data-hid':"dc.date"}).attrs['content']
    except:
        dt='blank'
        print(ur, 'no date')
    try:
        all_divs = soup.find('body')
        div = all_divs.find(class_="article-body")
        all_ps = div.find_all("p")
        body_string = ''
        for pp in all_ps:
            italic = pp.find('i')
            if italic:
                continue
            try:
                children = pp.findChildren()
                any_strong='no'
                for child in children:
                    strong = child.find('strong')
                    if strong:
                        any_strong='yes'
                if 'data-v-13907676' in pp.attrs or any_strong =='yes':
                    continue
                body = pp.get_text()
                if 'CLICK HERE TO GET THE FOX NEWS APP' in body:
                    continue
                to_add = f' {body}'
                body_string += to_add
            except:
                print(pp)
    except:
        body_string='blank'

    article_data =[ur, section, headline, dt, body_string]
    fox_articles.append(article_data)

