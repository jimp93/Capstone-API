#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import time
import pickle
import snscrape.modules.twitter as sntwitter
from datetime import timedelta
from datetime import datetime


# In[2]:


def scrape_tweets(page, since, until, c, tweet_dic={}):
    '''takes in the page, search date parameters and returns all tweets -- text, links, replies, likes, shares and date
    complicated by the search loop in source code being a generator, if there is an exception the loop breaks
    if the loop breaks, scrape_tweets function calls itself again, starting from two days before the last date of succesful returned tweet
    we get a dicitonary returned, with each key representing a loop until an exception and each value a list of tweets'''
    new_date = str(datetime.strptime(until, '%Y-%m-%d') - timedelta(days=2))
    tweet_list = []
    try:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{page} since:{since} until:{until}').get_items()):
            try:
                tweet_list.append([tweet.date, tweet.content, tweet.outlinks,                                tweet.replyCount, tweet.retweetCount, tweet.likeCount])
                print(tweet.date)
                date= tweet.date.date()
                new_date = str(date - timedelta(days=2))
            except:
                print(tweet.content)
    except:
        c+=1
        tweet_dic[c] = tweet_list
        scrape_tweets(page, since, new_date, c, tweet_dic) 
    c+=1
    tweet_dic[c] = tweet_list
    return tweet_dic
    
        


# In[3]:


guardian_tweets=scrape_tweets('guardian','2013-01-01', '2022-04-26',0)


# In[ ]:


fox_tweets=scrape_tweets('FoxNews','2013-01-01', '2022-04-26',0)


# In[ ]:


cnn_tweets=scrape_tweets('CNN','2013-01-01', '2022-04-26',0)


# In[ ]:


bbc_uk_tweets=scrape_tweets('BBCNews','2013-01-01', '2022-04-26',0)


# In[ ]:


bbc_world_tweets=scrape_tweets('BBCWorld','2013-01-01', '2022-04-26',0)


# In[ ]:


reuters_tweets=scrape_tweets('Reuters','2013-01-01', '2022-04-26',0)


# In[ ]:


def make_tweets_df(filename, outlet, tweets_dic):
    dics_list=[]
    for key in tweets_dic:
        dics_list+=tweets_dic[key]  
    df = pd.DataFrame(dics_list, columns=['Datetime', 'Text','Outlinks', 'Replies', 'Retweets', 'Likes'])
    df.to_csv(f'../collect_{outlet}/data/{filename}', index=False)
    return df


# In[ ]:


make_tweets_df('fox_tweets_df.csv', 'fox', fox_tweets)


# In[ ]:


make_tweets_df('bbc_uk_tweets_df.csv', 'bbc_uk',  bbc_uk_tweets)


# In[ ]:


make_tweets_df('bbc_world_tweets_df.csv', 'bbc_world', bbc_world_tweets)


# In[ ]:


make_tweets_df('cnn_tweets_df.csv', 'cnn', cnn_tweets)


# In[ ]:


make_tweets_df('guardian_tweets_df.csv', 'guardian' guardian_tweets)


# In[ ]:


make_tweets_df('reuters_tweets_df.csv', 'reuters', reuters_tweets)

