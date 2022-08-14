import bs4 as bs
import pickle
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from datetime import datetime, timedelta

with open('../../global_data/date_list', 'wb') as f:
    date_list=pickle.load(f)

# get wayback article url links from wayback machine
wb_bbc_urls = []
for ymd in date_list:
    try:
        url = f'http://archive.org/wayback/available?url=bbc.com&timestamp={ymd}'
        time.sleep(0.2)
        response = requests.get(url)
        data = response.json()
        wb_bbc_urls.append(data["archived_snapshots"]["closest"]["url"])
    except:
        print(ymd)

wb_bbc_urls_set = set(wb_bbc_urls)
wb_bbc_urls = list(wb_bbc_urls_set)

# get actual article links
bbc_urls = []
for wb_url in list(wb_bbc_urls):
    time.sleep(0.2)
      try:
        soup = BeautifulSoup(requests.get(wb_url).content, "html.parser")
        for a in soup.find_all('a', href=True):
            raw_bbc_url = (a['href'])
            if raw_bbc_url[-3:].isdigit():
                url_tuple = raw_bbc_url.partition('http://www.bbc')
                url_final = url_tuple[1]+url_tuple[2]
                if 'mundo' in url_final or 'urdu' in url_final or 'persian' in url_final or 'weather' in url_final or 'live' in url_final or url_final[-13:-8] == 'news/':
                    continue
                bbc_urls.append(url_final)
    except:
        print(wb_url)  


bbc_urls_set = set(bbc_urls)
bbc_urls = list(bbc_urls_set)

bbc_articles=[]

# parse articles, turn into dataframe and save
for ur in bbc_urls:
    time.sleep(0.2)

    article_data=[]
    try:
        soup = BeautifulSoup(requests.get(ur).text, "html.parser")

    except:
        soup = 'fail'
  
    if soup == 'fail':
        print(ur, 'no cx')
        continue
  
    vid = 'no'
    try:
        og_ur = soup.find("meta", property="og:url").attrs['content']
        if '/av/' in og_ur:
            vid = 'vid'

    except:
        print(ur, 'no og')

    if vid == 'vid':
        continue

    try:
        section = soup.find("meta", property="article:section").attrs['content']

    except:
        section = 'blank'
        print(ur, 'no section')
    try:
        headline = soup.find("title").get_text()
    except:
        headline = 'blank'
        print(ur, 'no headline')
        
    try:
        dt = soup.find('time').attrs['datetime']
    except:
        date='blank'
        print(ur, 'no headline')
    try:
        all_divs = soup.find('body')
        div = all_divs.find(class_="ssrcss-rgov1k-MainColumn e1sbfw0p0")
        all_ps = div.find_all(class_="ssrcss-1q0x1qg-Paragraph eq5iqo00")
        body_string = ''
        for pp in all_ps:
            try:
                body = pp.get_text()
                body_string += body
            except:
                print(pp)
    except:
        body_string='blank'
    if body_string=='blank':
        try:
            div = all_divs.find(class_="qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++")
            pars = div.find_all('p')
            body_string=''
            for p in pars:
                body = p.get_text()
                body_string += body
                try:
                    section_split = test.partition('http://www.bbc.com')
                    section = "-".join(section_split[2].split('/')[1:-1])
                except:
                    section= 'sport'
        except:
            body_string='blank'
    article_data =[ur, section, headline, dt, body_string]
    bbc_articles.append(article_data)

bbc_articles_df = pd.DataFrame(bbc_articles, columns=['URL', 'category', 'headline', 'date', 'text'])

with open('../data/bbc_articles_df', 'wb') as f:
    pickle.dump(bbc_articles_df, f)
