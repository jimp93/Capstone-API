#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pickle
import time
import pandas as pd
import os
import numpy as np
import json
import re


# In[22]:


with open('../data/cnn_articles_analysis', 'rb') as f:
    articles_analysis=pickle.load(f)


# In[3]:


articles_analysis.isnull().values.any()


# In[25]:


article_features_df = pd.DataFrame()


# In[26]:


article_features_df['category']=articles_analysis['category']


# # clean

# In[23]:


def text_cleaner(x):
    try:
        x=x.partition("(CNN")
        if x[1] == '(CNN':
            x=x[2].strip(" )Business")
        else:
            x=x[0]
    except:
        print('no clean')
    return x


# In[36]:


article_features_df['clean'] = articles_analysis['artText'].apply(text_cleaner)


# In[38]:


def make_clean_noquotes(x):
    switcheroo = x.replace('."', '".')
    body=switcheroo.split('.')
    new_art=[]

    # keep track if next par is quote (odd no of quotes in this par)
    pq=False
    for t in body:
        counter = t.count('"')
        # no quotes, keep the full sentence
        if counter == 0 and pq==False:
            new_art.append(t.strip('" '))

        # if sentence is in the middle of a long quote
        elif counter == 0 and pq==True:
            continue

        # finds all quotes within a sentence and removes them, if odd no of quotes then sets pq to true
        elif counter >0:
            if counter ==1 and '"' not in t[:2]:
                qi = t.index('"')
                t=t[qi:]
                new_art.append(t.strip('"'))
                pq=False
            elif counter ==1 and t.strip(' ')[0]=='"':
                pq=True
                continue

            else:
                t = t.split('"')
                del t[1::2]
                temp_t_list=[]
                for tt in t:
                    temp_t_list.append(tt.strip('"'))

                t = ('').join(temp_t_list)
                new_art.append(t.strip('"'))  
                if counter % 2 == 0:
                    pq=False
                else:
                    pq=True

    end_string=(". ").join(new_art)
    end_string=end_string.replace(' .', '')
    end_string=end_string.strip(' ')
    return end_string


# In[39]:


article_features_df['clean_noquotes'] = article_features_df['clean'].apply(make_clean_noquotes)


# # Standardise categories

# In[43]:


# to save memory, new features will be save in a separate dataframe, and merged when required
# standardised categories will be in the features_df, along with cleaned text and no quote text
# world will be changed in main df to localised


# In[17]:


cat_dic=articles_analysis['category'].value_counts().to_dict()


# In[18]:


cat_dic


# In[41]:


#use keys from cat dic and fit keys into standardised categories
cat_dic_raw={'entertainment': 'arts/entertainment',
             'opinions': 'opinion',
             'asia': 'asia/pac',
             'middleeast': 'mideast',
             'investing': 'business',
             'weather': 'science/environment',
             'living': 'lifestyle/culture',
             'success': 'lifestyle/culture',
             'football': 'sport',
             'tennis': 'sport',
             'australia': 'asia/pac',
             'china': 'asia/pac',
             'perspectives': 'opinion',
             'cars': 'auto/transport',
             'golf': 'sport',
             'india': 'asia/pac',
             'motorsport': 'sport',
             'homes': 'property',
             'energy': 'science/environment',
             'celebrities': 'showbiz',
             'movies': 'arts/entertainment',
             'vr': 'world',
             'tv-shows': 'arts/entertainment',
             'app-news-section': 'misc',
             'justice': 'law/justice',
             'aviation': 'auto/transport',
             'business-food': 'business',
             'foodanddrink': 'food/drink',
             'videos': 'misc',
             'cnn10': 'misc',
             'homepage': 'misc',
             'intl_business': 'business',
             'photos': 'misc',
             'business-money': 'business',
             'app-politics-section': 'misc',
             'culture': 'lifestyle/culture',
             'politics-zone-injection': 'politics',
             'business-india': 'business',
             'intl_world': 'world',
             'style': 'lifestyle/culture',
             'arts': 'arts/entertainment',
             'cnn-underscored': 'misc',
             'sailing': 'sport',
             'airport-delays': 'auto/transport',
             'app-opinion-section': 'opinion',
             'app-tech-section': 'tech',
             'election-center-2016': 'us',
             'app-international-edition': 'world',
             'tv': 'arts/entertainment',
             'technology': 'tech',
             'travel-stay': 'travel',
             'intl_travel': 'travel',
             'worldsport': 'sport',
             'travel-play': 'travel',
             'news': 'misc'}


# In[28]:


cat_dic_rname={}
for k in cat_dic_raw.keys():
    if type(cat_dic_raw[k]) == int:
        cat_dic_rname[k]='misc'
    else:
        cat_dic_rname[k]=cat_dic_raw[k]


# In[29]:


def cat_standardiser(x):
    try:
        x=cat_dic_rname[x]
    except:
        x=x
    return x


# In[30]:


article_features_df['category_stand']=articles_analysis['category'].apply(cat_standardiser)


# ## convert world into geographic area by checking for country names in headline/lead

# In[42]:


temp_df=articles_analysis[articles_analysis['category']=='world']


# In[43]:


with open('../../global_data/country_zone_dict', 'rb') as f:
    country_zone=json.load(f)


# In[57]:


def global_to_local(glob_df, main_df):
    
    cz_keys=list(country_zone.keys())
    for i, r in glob_df.iterrows():
        headline_list=r['headline'].split(' ')
        tally_dic={}
        caps_list=[]
        for h in headline_list:
            try:
                if h[0].isupper():
                    caps_list.append(h)
            except:
                print(h)

        lead_list=[]
        try:
            lead=main_df.loc[i, 'clean'].split(".")[0]
            lead_list=lead.split(" ")
            for l in lead_list:
                try:
                    if l[0].isupper():
                        caps_list.append(l)
                except:
                    print(l)
        except:
            print(h)
        if caps_list:
            for cz in cz_keys:
                for cl in caps_list:
                    if cz in cl or len(cl) >3 and cl in cz:
                        zone=country_zone[cz]
                        if zone in tally_dic.keys():
                            tally_dic[zone] +=1
                        else:
                            tally_dic[zone] =1
            if tally_dic:
                top_score = sorted(tally_dic.items(), key=lambda x:x[1], reverse=True)[0][0]
                main_df.loc[i, 'category']=top_score
            else:
                main_df.loc[i, 'category']='world'
        else:
            main_df.loc[i, 'category']='world'

        


# In[45]:


global_to_local(temp_df, article_features_df)


# In[46]:


#add outlet for use when merging into one df
article_features_df['outlet']='cnn'


# In[47]:


with open('../data/cnn_articles_features', 'wb') as f:
    pickle.dump(article_features_df, f)


# # check tweets df

# In[48]:


with open('../data/cnn_twitter_articles_analysis', 'rb') as f:
    twitter_articles_analysis=pickle.load(f)


# In[221]:


twitter_articles_analysis.isnull().values.any()


# In[49]:


twitter_articles_analysis['artText'] = twitter_articles_analysis['artText'].apply(text_cleaner)


# In[52]:


def text_cleaner(x):
    if x!='blank':
        x = x.partition('http')
        x=x[0].strip()
    return x


# In[53]:


twitter_articles_analysis['tweetText']=twitter_articles_analysis['tweetText'].apply(text_cleaner)


# In[ ]:





# In[55]:


twitter_articles_analysis['category']=twitter_articles_analysis['category'].apply(cat_standardiser)


# In[56]:


tw_temp = twitter_articles_analysis[twitter_articles_analysis['category']=='world']


# In[58]:


global_to_local(tw_temp, twitter_articles_analysis)


# In[61]:


with open('../data/cnn_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_articles_analysis, f)


# In[ ]:





# In[66]:


af1=article_features_df.to_json()


# In[67]:


with open('../data/cnn_article_features_js', 'w') as f:
    json.dump(af1, f)


# In[ ]:




