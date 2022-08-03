#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bs4 as bs
import pickle
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import os
import json
import numpy as np


# # make df linking articles to outlinks
# 

# In[2]:


# import dictionary from colab of outlinks where headline is not the same as tweets, and the headline.
# we can use this to link to article
with open('../data/import_data/guardian_dic', 'rb') as f:
    outlinks_headline=json.load(f)


# In[3]:


explode_dic={}
for k in list(outlinks_headline.keys()):
    if isinstance(outlinks_headline[k], list):
        raw =outlinks_headline[k][0]
    else:
        raw=outlinks_headline[k]
    raw=raw.split("|")[0].strip(" ")
    explode_dic[k] = raw
        


# In[4]:


outlinks_headline_df=pd.DataFrame.from_dict(explode_dic, orient='index', columns=['headline_link'])


# In[5]:


outlinks_headline_df.reset_index(inplace=True)
outlinks_headline_df.rename(columns={'index': 'outlink'}, inplace=True)


# In[6]:


outlinks_headline_df=outlinks_headline_df[outlinks_headline_df['headline_link']!='Page Not Found']


# In[7]:


outlinks_headline_df.reset_index(drop=True, inplace=True)


# In[8]:


guardian_tweets = pd.read_csv('../data/guardian_tweets_df.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)


# In[9]:


guardian_tweets['Datetime']=guardian_tweets['Datetime'].apply(lambda x: x[:10])
guardian_tweets.rename(columns={'Datetime': 'date'}, inplace=True)
guardian_tweets.rename(columns={'Text': 'tweetText', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)


# In[10]:


guardian_tweets=guardian_tweets.explode('Outlinks')


# In[11]:


for tw in ['replies', 'retweets', 'likes']:
    guardian_tweets[tw]=guardian_tweets[tw].astype(int)


# In[ ]:





# In[16]:


# make df linking scraped articles to their tweets, if the headline isnt the same as the tweet. 
#First add the headline to the tweet df by linking through outlinks


# In[12]:


twitter_article_analysis=guardian_tweets.merge(outlinks_headline_df, left_on='Outlinks', right_on='outlink')


# In[13]:


twitter_article_analysis.drop('Outlinks', axis=1, inplace=True)


# In[17]:


# link the rest of the article using the headline 


# In[14]:


with open('../data/guardian_articles_df', 'rb') as f:
    guardian_scrape_articles=pickle.load(f)


# In[15]:


guardian_scrape_articles.rename(columns={'text':'artText'}, inplace=True)


# In[16]:


guardian_scrape_articles['date']=guardian_scrape_articles['date'].apply(lambda x:x[:10])


# In[ ]:





# In[17]:


# full article analysis is just the articles scraped from API. Pointless scraping articles from tweets outlinks
# as the API returns all articles
article_analysis=guardian_scrape_articles.copy()


# In[18]:


with open('../data/guardian_articles_analysis', 'wb') as f:
    pickle.dump(article_analysis, f)


# In[ ]:


# merge tweets with articles


# In[19]:


twitter_article_analysis=guardian_scrape_articles.merge(twitter_article_analysis, left_on='headline', right_on='headline_link')


# In[20]:


twitter_article_analysis.drop(['headline_link', 'date_x', 'outlink'], axis=1, inplace=True)


# In[21]:


twitter_article_analysis.rename(columns={'date_y':'date'}, inplace=True)


# In[ ]:


# we now have linked articles to tweets where tweet is differnt to the headline (maybe just a link after the tweet). 
# We need to add rows where they are the same


# In[22]:


with open('../data/guardian_tw_art', 'rb') as f:
    guardian_tw_art=pickle.load(f)


# In[23]:


guardian_tw_art.drop(['date_y', 'URL_list'], axis=1, inplace=True)


# In[24]:


guardian_tw_art.rename(columns={'text':'artText', 'Text':'tweetText'}, inplace=True)


# In[25]:


guardian_tw_art.rename(columns={'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes', 'date_x':'date'}, inplace=True)


# In[26]:


for tw in ['replies', 'retweets', 'likes']:
    guardian_tw_art[tw]=guardian_tw_art[tw].astype(int)


# In[27]:


guardian_tw_art['date']=guardian_tw_art['date'].apply(lambda x: x[:10])


# In[28]:


twitter_article_analysis=pd.concat([twitter_article_analysis, guardian_tw_art])


# In[29]:


twitter_article_analysis.drop_duplicates(subset='tweetText', inplace=True)


# In[30]:


twitter_article_analysis.reset_index(drop=True, inplace=True)


# In[31]:


def clean_tweet(x):
    x=x.partition('http')[0].strip(' "!:,."')
    return x


# In[32]:


twitter_article_analysis['tweetText']=twitter_article_analysis['tweetText'].apply(clean_tweet)


# In[33]:


with open('../data/guardian_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)


# In[ ]:




