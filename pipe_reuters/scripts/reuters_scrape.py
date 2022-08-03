#!/usr/bin/env python
# coding: utf-8

# In[11]:


import bs4 as bs
import pickle
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


# In[2]:


with open('date_list', 'rb') as fp:
    date_list = pickle.load(fp)


# In[13]:


wb_reuters_urls =[]

for ymd in date_list:
    try:
        url = f'http://archive.org/wayback/available?url=reuters.com&timestamp={ymd}'
        time.sleep(0.2)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        wb_url_list.append(data["archived_snapshots"]["closest"]["url"])
    except:
        print(ymd)

wb_reuters_urls_set=set(wb_reuters_urls)
wb_reuters_urls = list(wb_reuters_urls_set)


# In[ ]:


wb_reuters_urls


# In[17]:


reuters_urls = []
c=0
for wb_url in wb_reuters_urls:
    c+=1
    print(c)
    success = 'yes'
    try:
        soup = BeautifulSoup(requests.get(wb_url).text, "html.parser")
    except:
        print(wb_url, 'no cx')
        success = 'no'

    if success == 'no':
        continue

    try:
        ind = 0
        for a in soup.find_all('a', href=True):
            href = (a['href'])
            url_tuple = href.partition('https://www.reuters.com')
            if url_tuple[2][:8] =='/article':
                ind+=1
                url_final = url_tuple[1]+url_tuple[2]
                final_urls.append(url_final)
            url_p_tuple = href.partition('http://www.reuters.com')
            if url_p_tuple[2][:8] =='/article':
                ind+=1
                url_p_final = url_p_tuple[1]+url_tuple[2]
                reuters_urls.append(url_p_final)

    except:
        print(wb_url, 'no links')
        success = 'no'
  
    if success == 'no':
        continue

reuters_urls_set = set(reuters_urls)
reuters_urls = list(reuters_urls_set)


# In[ ]:


reuters_articles=[]

for ur in reut_url_list:
    time.sleep(0.05)
    article_data=[]
    try:
        soup = BeautifulSoup(requests.get(ur).text, "html.parser")

    except:
        soup = 'fail'
  
    if soup == 'fail':
        print(ur, 'no cx')
        continue

    try:
        section = soup.find("meta", attrs={'property':"og:article:section"}).attrs['content']

    except:
        try:
            section = soup.find("meta", attrs={'name':"analyticsAttributes.topicChannel"}).attrs['content']
        except:
            section = 'blank'
            print(ur, 'no section')

    try:
        headline = soup.find("meta", attrs={'name':"sailthru.title"}).attrs['content']
    except:
        try:
            headline = soup.find("meta", property="og:title").attrs['content']
        except:
            headline = 'blank'
            print(ur, 'no headline')
    try:
        dt = soup.find("meta", property='og:article:published_time').attrs['content']
    except:
        dt='blank'
        print(ur, 'no date')
    try:
        all_ps = soup.find_all(class_ = "text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__large__nEccO body__base__22dCE body__large_body__FV5_X article-body__element__2p5pI")
    except:
        try:
            all_divs = soup.find('body')
            div = all_divs.find(class_="ArticleBodyWrapper")
            all_ps = div.find_all(class_="Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x")
            body_string = ''
            for pp in all_ps:
                try:
                    body = pp.get_text()
                    body_string += body
                except:
                    print(pp)
        except:
            body_string='blank'

    article_data =[ur, section, headline, dt, body_string]
    reuters_articles.append(article_data)


# In[ ]:


reuters_articles_df = pd.DataFrame(reuters_articles, columns=['URL', 'category', 'headline', 'date', 'text'])


# In[11]:


with open('../articles/reuters_articles_df', 'wb') as f:
    pickle.dump(reuters_articles_df, f)


# In[3]:


with open('../articles/reuters_articles_df', 'rb') as f:
    reuters_articles_df=pickle.load(f)


# In[5]:


reuters_articles_df.drop_duplicates(subset='headline', inplace=True)


# In[7]:


reuters_articles_df.reset_index(inplace=True, drop=True)


# In[9]:


with open('../articles/reuters_articles_df', 'wb') as f:
    pickle.dump(reuters_articles_df, f)


# In[ ]:





# In[12]:


reuters_tweets=pd.read_csv('../twitter_dfs/reuters_tweets_df.csv')


# In[14]:


reuters_tweets.drop_duplicates(subset='headline', inplace=True)


# In[16]:


reuters_tweets.reset_index(inplace=True, drop=True)


# In[17]:


reuters_tweets


# In[18]:


reuters_tweets.to_csv('../twitter_dfs/reuters_tweets_df.csv', index=False)


# In[21]:


for index, row in reuters_tweets.iterrows():
    print(index)
    tuple_1= row['headline'].partition('. ')
    tuple_2= tuple_1[0].partition('http')[0].strip()
    reuters_tweets.loc[index, 'headline'] = tuple_2
    


# In[22]:


reuters_tweets.to_csv('../twitter_dfs/reuters_tweets_df.csv', index=False)


# In[24]:


reuters_tweets.loc[2, 'headline']


# In[ ]:




