#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import pandas as pd
import os
import numpy as np
import json 


# # make dataframe of articles scraped on colab using twitter outlinks

# In[2]:


# open the dic made in colab. The outlink from each tweet in the tweet_df is the key
# the headline, section, article text and expanded url are the values
# we only use outlinks for tweets where the tweet is differnt from the article headline, which we 
# found out be merging tweet_df and articles_df. Would be a waste of time to scrape those outlinks as 
# we already linked the tweet to article
with open('../data/import_data/cnn_dic', 'rb') as f:
    dic1=json.load(f)


# In[3]:


outlink_art_df=pd.DataFrame.from_dict(dic1, orient = 'index', columns=['expURL', 'category', 'headline', 'date', 'artText'])


# In[4]:


outlink_art_df.reset_index(inplace=True)


# In[5]:


outlink_art_df.rename(columns={'index':'shortURL', 'text':'artText'}, inplace=True)


# # link tweets df to the df above (one article maybe linked to by more than one tweet)

# In[6]:


cnn_tweets = pd.read_csv('../data/cnn_tweets_df.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)


# In[7]:


cnn_tweets=cnn_tweets.explode('Outlinks')


# In[8]:


cnn_tweets.rename(columns={'Text': 'tweetText', 'headline':'tweetText','Outlinks': 'shortURL', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)


# In[9]:


tweet_sc_art_join = outlink_art_df.merge(cnn_tweets, on='shortURL', how='outer')


# In[10]:


tweet_sc_art_join['Datetime'] = tweet_sc_art_join['Datetime'].apply(lambda x: x[:10])


# In[11]:


tweet_sc_art_join.drop('date', axis=1, inplace=True)


# In[12]:


tweet_sc_art_join.rename(columns={'Datetime': 'date'}, inplace=True)


# In[13]:


tweet_sc_art_join.drop_duplicates(inplace=True)


# In[14]:


tweet_sc_art_join.reset_index(drop=True, inplace=True)


# # make another df linking the scraped articles and tweet where summary is same as headline

# In[15]:


with open('../data/cnn_articles_df', 'rb') as f:
    cnn_scrape_articles=pickle.load(f)


# In[16]:


#need to clean tweets to get rid of hyperlink
cnn_tweets.Datetime=cnn_tweets.Datetime.apply(lambda x: x[:10])
cnn_tweets.rename(columns={'Datetime':'date'}, inplace=True)


# In[17]:


def text_cleaner(x):
    if x!='blank':
        x = x.partition('http')
        x=x[0].strip()
    return x


# In[18]:


cnn_tweets['tweetText']=cnn_tweets['tweetText'].apply(text_cleaner)


# In[19]:


cnn_tw_art = cnn_scrape_articles.merge(cnn_tweets, left_on='headline', right_on='tweetText')


# In[20]:


cnn_tw_art.rename(columns={'URL':'expURL', 'text':'artText', 'date_x':'date', 'Text':'tweetText', 'Replies':'replies', 'Retweets':'retweets', 'Likes':'likes'}, inplace=True)


# In[21]:


cnn_tw_art.drop('date_y', axis=1, inplace=True)


# In[22]:


full_join = pd.concat([tweet_sc_art_join, cnn_tw_art])


# In[23]:


full_join.reset_index(drop=True, inplace=True)


# In[29]:


#full join is essentially reconstructing the original tweets dataframe, adding the articles. 
# we did this by linking rows where tweet was same as headline (cnn_tw_art) and by retrieving 
# articles where they weren't by opening the hyperlink in the tweet and scraping article (tweet_sc_art_join). 
full_join


# # Make df of all articles, joining original scrape with twitter links

# In[24]:


# we have the original scraped article df, but we may have found more when scraping from the tweet hyperlinks
# need to concat the two dataframes and drop duplicates 
cnn_scrape_articles.drop_duplicates(subset='headline', inplace=True)


# In[25]:


cnn_scrape_articles.reset_index(drop=True, inplace=True)


# In[26]:


cnn_scrape_articles.rename(columns={'text':'artText', 'URL':'expURL'}, inplace=True)


# In[27]:


article_analysis = pd.concat([cnn_scrape_articles, full_join])


# In[28]:


article_analysis.drop(['replies', 'retweets', 'likes', 'tweetText', 'shortURL'], axis=1, inplace=True)


# In[29]:


article_analysis.drop_duplicates(subset=['headline', 'artText'], inplace=True)


# In[30]:


article_analysis.reset_index(drop=True, inplace=True)


# In[32]:


article_analysis=article_analysis.dropna(subset=['artText'])


# In[33]:


index_names = article_analysis[article_analysis['artText'] == 'blank' ].index
article_analysis.drop(index_names, inplace=True)


# In[41]:


index_names = article_analysis[article_analysis['artText'] == '' ].index
article_analysis.drop(index_names, inplace=True)


# In[ ]:


#for i, r in article_analysis.iterrows():
 #   if not r['artText'] or r['artText'] =='blank':
  #      c+=1
   #     print(i)
    #    article_analysis.drop(i, axis=0, inplace=True)
        


# In[43]:


article_analysis.reset_index(drop=True, inplace=True)


# In[44]:


article_analysis.drop_duplicates(subset='headline', inplace=True)


# In[45]:


article_analysis=article_analysis.dropna(subset=['artText'])


# In[46]:


article_analysis.reset_index(drop=True, inplace=True)


# In[47]:


with open('../data/cnn_articles_analysis', 'wb') as f:
    pickle.dump(article_analysis, f)


# # Make df of all tweets, linked to the article

# In[48]:


twitter_article_analysis=full_join.copy()


# In[49]:


twitter_article_analysis.drop('shortURL', axis=1, inplace=True)


# In[50]:


twitter_article_analysis.drop_duplicates(subset='tweetText', inplace=True)


# In[51]:


twitter_article_analysis.reset_index(drop=True, inplace=True)


# In[51]:


twitter_article_analysis


# In[52]:


for tw in ['replies', 'retweets', 'likes']:
    twitter_article_analysis[tw]=twitter_article_analysis[tw].astype(int)


# In[53]:


with open('../data/cnn_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)


# In[ ]:




