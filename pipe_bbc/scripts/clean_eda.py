import pickle
import time
import pandas as pd
import os
import numpy as np
import json
import re

with open('../data/bbc_articles_analysis', 'rb') as f:
    articles_analysis=pickle.load(f)

with open('../data/bbc_twitter_articles_analysis', 'rb') as f:
    twitter_articles_analysis=pickle.load(f)

articles_analysis.isnull().values.any()
twitter_articles_analysis.isnull().values.any()


# to save memory, new features will be save in a separate dataframe, and merged when required

article_features_df = pd.DataFrame()
article_features_df['category']=articles_analysis['category']

# clean article text and remove quotes

def tidy_text(x):
    try:
        tidy_list=[]
        x=x.replace('This video can not be played', ' ')
        x=x.split(". ")
        for tn in x:
            tn=tn.strip(' .')
            if tn:
                tidy_list.append(tn)
        end_string =('. ').join(tidy_list) 
    except:
        end_string=x
    return end_string

def tidy_noquotes(x):
    quote_list=[]
    reg = re.findall(re.escape('"')+"(.*?)"+re.escape('.'), x) 
    for q in reg:
        try:
            if q[0] ==' ':
                continue
            else:
                quote_list.append(q)
        except:
            print('no quote')
    no_q=x
    for sub in quote_list:
        try:
            no_q = no_q.replace(sub, '')
        except:
            print('cannot replace')

    neat_noq_list=[]
    no_q=no_q.split(".")
    for tn in no_q:
        tn=tn.strip('" .')
        if tn:
            neat_noq_list.append(tn)
    end_string =('. ').join(neat_noq_list) 
    return end_string

article_features_df['clean_text'] = articles_analysis['artText'].apply(tidy_text)
article_features_df['clean_noquotes'] = article_features_df['clean_text'].apply(tidy_noquotes)


# Standardise categories
cat_dic=articles_analysis['category'].value_counts().to_dict()
cat_dic_rname= {'Business': 'business',
                'sport': 'sport',
                'US & Canada': 'us',
                'Technology': 'tech',
                'blank': 'sport',
                'Entertainment & Arts': 'arts/entertainment',
                'Europe': 'europe',
                'Science & Environment': 'science/environment',
                'Middle East': 'mideast',
                'Health': 'health',
                'Asia': 'asia/pac',
                'Magazine': 'lifestyle/culture',
                'Africa': 'africa',
                'UK': 'uk',
                'Latin America & Caribbean': 'americas',
                'In Pictures': 'pics',
                'India': 'asia/pac',
                'UK Politics': 'politics',
                'China': 'asia/pac',
                'US Election 2016': 'politics',
                'Trending': 'lifestyle/culture',
                'Newsbeat': 'arts/entertainment',
                'World': 'opinion',
                'Australia': 'asia/pac',
                'Stories': 'lifestyle/culture',
                'England': 'uk',
                'Echo Chambers': 'opinion',
                'London': 'uk',
                'BBC Trending': 'opinion',
                'Magazine Monitor': 'offbeat',
                'News from Elsewhere': 'offbeat',
                'Scotland': 'uk',
                'Northern Ireland': 'uk',
                'Education & Family': 'misc',
                'EU Referendum': 'politics',
                'Scotland politics': 'politics',
                'Wales': 'uk',
                'Scotland business': 'business',
                'Glasgow & West Scotland': 'uk',
                'Edinburgh, Fife & East Scotland': 'uk',
                'Manchester': 'uk',
                'Leicester': 'uk',
                'China blog': 'opinion',
                'Norfolk': 'uk',
                'Birmingham & Black Country': 'uk',
                'Family & Education': 'misc',
                'Bristol': 'uk',
                'Hampshire & Isle of Wight': 'uk',
                'Gloucestershire': 'uk',
                'NE Scotland, Orkney & Shetland': 'uk',
                'Sussex': 'uk',
                'Essex': 'uk',
                'South East Wales': 'uk',
                'Highlands & Islands': 'uk',
                'Liverpool': 'uk',
                'Election 2015': 'politics',
                'World News TV': 'lifestyle/culture',
                'South Scotland': 'uk',
                'Tyne & Wear': 'uk',
                'Cylchgrawn': 'uk',
                'Lancashire': 'uk',
                'Cambridgeshire': 'uk',
                'Beds, Herts & Bucks': 'uk',
                'Cornwall': 'uk',
                'Derby': 'uk',
                'Devon': 'uk',
                'Leeds & West Yorkshire': 'uk',
                'Tayside and Central Scotland': 'uk',               
                'Suffolk': 'uk', 
                'Election 2017': 'politics',
                'Kent': 'uk',
                'Oxford': 'uk',
                'Nottingham': 'uk',
                'South West Wales': 'uk',
                'Wiltshire': 'uk',
                'Coventry & Warwickshire': 'uk',
                'Humberside': 'uk',
                'Brexit': 'politics',
                'Surrey': 'uk',
                'Dorset': 'uk',
                'Disability': 'misc',
                'Northampton': 'uk',
                'Somerset': 'uk',
                'Ouch': 'opinion',
                'Explainers': 'opinion',
                'Tees': 'uk',
                'Asia-Pacific': 'asia/pac',
                'Stoke & Staffordshire': 'uk',
                'Hereford & Worcester': 'uk',
                'Sheffield & South Yorkshire': 'uk',
                'Mid Wales': 'uk',
                'South Asia': 'asia/pac',
                'Election 2016': 'politics',
                'The Reporters': 'opinion',
                'Cumbria': 'uk',
                'Inside Europe Blog': 'europe',
                'York & North Yorkshire': 'uk',
                'Berkshire': 'uk',
                'Lincolnshire': 'uk',
                'Parliaments': 'politics',
                'Guernsey': 'uk',
                'Wales politics': 'politics',
                'North West Wales': 'uk',
                'Shropshire': 'uk',
                'North East Wales': 'uk',
                'Jersey': 'uk',
                'New Tech Economy': 'tech',
                'The Boss': 'misc',
                'Scotland Election 2016': 'politics',
                'Isle Of Man / Ellan Vannin': 'uk',
                'World Radio and TV': 'opinion',
                'US Election 2020': 'politics',
                'Foyle & West': 'uk',
                'The Papers': 'politics',
                'Newyddion a mwy': 'wales-uk',
                'Eisteddfod Genedlaethol': 'wales-uk',
                'N. Ireland Politics': 'politics',
                'Crossing Divides': 'misc',
                'Global education': 'misc',
                'Entrepreneurship': 'misc',
                '100 Women': 'misc',
                'Global Trade': 'economy',
                'Reality Check': 'misc',
                'The Disruptors': 'misc',
                'Technology of Business': 'economy',
                'CEO Secrets': 'economy'}

article_features_df['category_stand']=articles_analysis['category'].apply(lambda x: cat_dic_rname[x])
article_features_df['outlet']='bbc'

with open('../data/bbc_articles_features', 'wb') as f:
    pickle.dump(article_features_df, f)

twitter_articles_analysis['clean']=twitter_articles_analysis['artText'].apply(tidy_text)

def twitter_cat_stand(x):
    try:
        x=cat_dic_rname[x]
    except:
        x=x
    return x

twitter_articles_analysis['category']=twitter_articles_analysis['category'].apply(twitter_cat_stand)
twitter_articles_analysis

with open('../data/bbc_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_articles_analysis, f)

af1=article_features_df.to_json()

with open('../data/bbc_article_features_js', 'w') as f:
    json.dump(af1, f)




