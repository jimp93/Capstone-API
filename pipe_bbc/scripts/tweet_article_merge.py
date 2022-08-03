#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import time
import pandas as pd
import os
import numpy as np
import json


# In[2]:


# Make df of articles to analyze. Is just a formatted copy of the scraped articles as we can't glean any
# from twitter outlinks as website doesn't allow it


# In[3]:


with open('../data/bbc_articles_df', 'rb') as f:
    bbc_scrape_articles=pickle.load(f)


# In[4]:


bbc_scrape_articles.drop_duplicates(subset='headline', inplace=True)


# In[5]:


bbc_scrape_articles.reset_index(drop=True, inplace=True)


# In[6]:


bbc_scrape_articles.rename(columns={'text':'artText', 'URL':'expURL'}, inplace=True)


# In[7]:


with open('../data/bbc_articles_analysis', 'wb') as f:
    pickle.dump(bbc_scrape_articles, f)


# In[ ]:





# In[8]:


# make df linking articles to tweets (import of colab created df which used similarity of tweets to article lead to link)


# In[9]:


with open('../data/import_data/bbc_tw_art_similar', 'rb') as f:
    bbc_tw_art_similar=pickle.load(f)


# In[10]:


bbc_tw_art_similar.drop(['headline_list', 'date_y', 'same_tweet?', 'text_list', 'tweet_summary', 'URL_list'], axis=1, inplace=True)


# In[11]:


bbc_tw_art_similar.rename(columns={'date_x':'date', 'text':'artText', 'Text':'tweetText', 'Replies':'replies', 'Retweets':'retweets', 'Likes':'likes'}, inplace=True)


# In[12]:


# bbc clean tweets was created in colab, combining world and uk dataframes
bbc_tweets = pd.read_csv('../data/import_data/all_bbc_tweets.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)


# In[13]:


def tweet_cleaner(df):
    t_url_list=df['URL_list'].tolist()
    new_list=[]
    for l in t_url_list:
        try:
            li = l[2:-2]
            li = li.split(', ')
        except:
            li=['blank']
        new_list.append(li)
    new_list_format=[]
    for n in new_list:
        row_list=[]
        for nn in n:
            nn=nn.strip('"')
            nn=nn.strip("'")
            row_list.append(nn)
        new_list_format.append(row_list)
    df['URL_list'] = new_list_format  
    return df


# In[14]:


bbc_tweets=tweet_cleaner(bbc_tweets)


# In[15]:


bbc_tweets=bbc_tweets.explode('URL_list')


# In[16]:


bbc_tweets.rename(columns={'Text': 'tweetText','URL_list': 'shortURL', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)


# In[17]:


# make dataframe of all tweets, with article if found


# In[18]:


twitter_article_analysis=pd.concat([bbc_tw_art_similar, bbc_tweets])


# In[19]:


twitter_article_analysis.drop_duplicates('tweetText', inplace=True)


# In[20]:


twitter_article_analysis.drop('shortURL', axis=1, inplace=True)


# In[21]:


twitter_article_analysis.reset_index(drop=True, inplace=True)


# In[22]:


for tw in ['replies', 'retweets', 'likes']:
    twitter_article_analysis[tw]=twitter_article_analysis[tw].astype(int)


# In[23]:


with open('../data/bbc_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)


# In[ ]:




