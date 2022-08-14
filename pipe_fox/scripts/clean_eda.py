import pickle
import time
import pandas as pd
import os
import numpy as np
import json
import re

with open('../data/fox_articles_analysis', 'rb') as f:
    articles_analysis=pickle.load(f)

articles_analysis.isnull().values.any()


# to save memory, new features will be save in a separate dataframe, and merged when required
# standardised categories will be in the features_df, along with cleaned text and no quote text
# world will be changed in main df to localised

article_features_df = pd.DataFrame()
article_features_df['category']=articles_analysis['category']

def general_cleaner(x):
    try:
        x=x.split('. ')
        stripped=[]
        for xx in x:
            xx=xx.replace('\n', ' ')
            xx=xx.replace('\xa0', ' ')
            xx=xx.replace('/n', ' ').strip(' ')
            stripped.append(xx)
        x=('. ').join(stripped)
    except:
        x=x
    return x

def noquote_cleaner(x):
    sp=re.split('–|-',x)
    sp1=sp[0].strip(' \n')
    mlist=['Jan', 'Feb', 'Mar', 'March', 'Apr', 'April', 'May', 'Jun', 'June', 'Jul', 'July', 'Aug', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec']
    sp2=sp1.split(' ')
    if sp2[0].strip('.') in mlist or (sp2[0].isupper() and len(sp2[0])>1):
        sp.pop(0)
        x=('-').join(sp)
        x=x.strip(' -/n')
        x=x.split('. ')
        stripped=[]
        for xx in x:
            xx=xx.replace('\n', ' ')
            xx=xx.replace('\xa0', ' ')
            xx=xx.replace('/n', ' ').strip(' ')
            stripped.append(xx)
        x=('. ').join(stripped)
        return x
    else:
        x=x.split('. ')
        stripped=[]
        for xx in x:
            xx=xx.replace('\n', ' ')
            xx=xx.replace('\xa0', ' ')
            xx=xx.replace('/n', ' ').strip(' ')
            stripped.append(xx)
        x=('. ').join(stripped)
    return x

article_features_df['clean']=articles_analysis['artText'].apply(general_cleaner)
article_features_df['clean_noquote']=articles_analysis['artText'].apply(noquote_cleaner)

# Standardise categories
# convert world into geographic area by checking for country names in headline/lead

cat_dic=articles_analysis['category'].value_counts().to_dict()
raw_cat_dic={'auto': 'auto/transtport',
             'blank': 'delete',
             'category': 'loop',
             'entertainment': 'arts/entertainment',
             'faith-values': 'lifestyle/culture',
             'family': 'lifestyle/culture',
             'food-drink': 'food/drink',
             'fox_and_friends': 'opinion',
             'fox_nation': 'opinion',
             'great-outdoors': 'science/environment',
             'health': 'health',
             'lifestyle': 'lifestyle/culture',
             'official-polls': 'politics',
             'opinion': 'opinion',
             'person': 'misc',
             'features':'economy',
             'real-estate': 'property',
             'science': 'science/environment',
             'earth-space':'science/environment',
             'shows': 'arts/entertainment',
             'small-business': 'business',
             'sports': 'sport',
             'story': 'misc',
             'the_story': 'opinion',
             'transcript': 'opinion',
             'weather': 'science/environment',
             'world': 'world',
             'weather-news': 'science/environment',
             'extreme-weather': 'science/environment',
             'industrials':'economy',
             'learn':'misc',
             'financials':'economy',
             'personal-finance':'economy',
             'your_world': 'world'}

def cat_standardiser(x):
    try:
        x=raw_cat_dic[x]
    except:
        x=x
    return x

article_features_df['category_stand']=articles_analysis['category'].apply(cat_standardiser)
temp_df=articles_analysis[article_features_df['category_stand']=='world']

with open('country_zone_dict', 'r') as f:
    country_zone=json.load(f)

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
            lead= main_df.loc[i, 'clean'].split(".")[0]
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

global_to_local(temp_df, article_features_df)

#add outlet for use when merging into one df
article_features_df['outlet']='fox'

with open('../data/fox_articles_features', 'wb') as f:
    pickle.dump(article_features_df, f)

with open('../data/fox_twitter_articles_analysis', 'rb') as f:
    twitter_articles_analysis=pickle.load(f)

twitter_articles_analysis['clean']=twitter_articles_analysis['artText'].apply(general_cleaner)

def text_cleaner(x):
    x = x.partition('http')
    x=x[0].strip(' \n')
    return x

twitter_articles_analysis['tweetText']=twitter_articles_analysis['tweetText'].apply(text_cleaner)
twitter_articles_analysis['category']=twitter_articles_analysis['category'].apply(cat_standardiser)
tw_temp = twitter_articles_analysis[twitter_articles_analysis['category']=='world']
global_to_local(tw_temp, twitter_articles_analysis)

with open('../data/fox_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_articles_analysis, f)

af1=articles_analysis.to_json()

with open('../data/fox_articles_analysis_js', 'w') as f:
    json.dump(af1, f)
