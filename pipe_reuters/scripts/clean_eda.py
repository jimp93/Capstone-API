import pickle
import time
import pandas as pd
import os
import numpy as np
import json
import re

with open('../data/reuters_articles_analysis', 'rb') as f:
    articles_analysis=pickle.load(f)

articles_analysis.isnull().values.any()


# Make new df for features, clean columns
article_features_df = pd.DataFrame()
article_features_df['category']=articles_analysis['category']

# cleaned to get lead
def text_cleaner(x):
    try:
        x=x.partition("(Reuters) -")
        x=x[2].strip(" ")
    except:
        x=x
    return x

article_features_df['clean'] = articles_analysis.artText.apply(text_cleaner)

def tidy_noquotes(x):
    quote_list=[]
    reg = re.findall(re.escape('“')+"(.*?)"+re.escape('”'), x) 
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
        tn=tn.strip(' “”.')
        tn=tn.replace('“”', '')
        if tn:
            neat_noq_list.append(tn)
    end_string =('. ').join(neat_noq_list) 
    return end_string

article_features_df['clean_noquotes'] = article_features_df['clean'].apply(tidy_noquotes)
article_features_df['clean'] = article_features_df['clean'].apply(lambda x: x.replace('.', '. '))
article_features_df['clean'] = article_features_df['clean'].apply(lambda x: x.replace('U. S. ', 'U.S.'))
article_features_df['clean'] = article_features_df['clean'].apply(lambda x: x.replace('U. K.', 'U. K.'))


# Standardise categories
# convert world into geographic area by checking for country names in headline/lead
cat_dic=articles_analysis['category'].value_counts().to_dict()

#use keys from cat dic and fit keys into standardised categories
cat_dic_raw={'Industrials': 'economy',
             '2020 - Buttigieg': 'politics',
             '2020 Candidate Slideshows': 'politics',
             '2020 U.S. Elections': 'politics',
             'AMERS': 'americas',
             'APAC': 'asia/pac',
             'Aerospace & Defense': 'economy',
             'Aerospace and Defense': 'economy',
             'Africa': 'africa',
             'Airlines': 'business',
             'Americas': 'americas',
             'Arts': 'arts/entertainment',
             'Asia Pacific': 'asia/pac',
             'Asian Markets': 'economy',
             'Autos': 'auto/transport',
             'Autos & Transportation': 'auto/transport',
             'Banks': 'economy',
             'Barack Obama': 'politics',
             'Biden 2020': 'politics',
             'Big Story 10': 'world',
             'Big Story 15': 'world',
             'Biotechnology': 'tech',
             'Bloomberg 2020': 'politics',
             'Bonds News': 'economy',
             'Breakingviews': 'opinion',
             'Breakingviews Coronavirus': 'opinion',
             'Brexit': 'politics',
             'Business': 'business',
             'Business News': 'business',
             'Business Special Reports': 'business',
             'COP26': 'science/environment',
             'COP27': 'science/environment',
             'Change Suite': 'opinion',
             'China': 'asia/pac',
             'Commentary': 'opinion',
             'Commodities': 'economy',
             'Commodities News': 'economy',
             'Consumer Financial Services': 'economy',
             'Consumer Goods & Retail': 'economy',
             'Coronavirus': 'health',
             'Coronavirus Explainers': 'health',
             'Coronavirus: Full Coverage': 'health',
             'Currencies': 'economy',
             'Cyber Risk': 'tech',
             'Deals': 'business',
             'Disrupted': 'tech',
             'ESG': 'business',
             'ESG Environment': 'business',
             'ETF News': 'tech',
             'Earnings': 'business',
             "Editor's Picks": 'world',
             "Editor's picks": 'world',
             'Emerging Markets': 'economy',
             'Energy': 'science/environment',
             'Energy & Environment': 'science/environment',
             'Entertainment News': 'arts/entertainment',
             'Environment': 'science/environment',
             'Europe': 'europe',
             'Europe News': 'europe',
             'European Currency News': 'economy',
             'European Markets': 'economy',
             'Film News': 'arts/entertainment',
             'Finance': 'economy',
             'Financial Regulatory Forum': 'economy',
             'Financial Services & Real Estate': 'economy',
             'Financials': 'economy',
             'Follow the money': 'health',
             'Foreign Exchange Analysis': 'economy',
             'France': 'europe',
             'Full coverage of the Winter Olympics.': 'sport',
             'Funds': 'economy',
             'Funds News': 'economy',
             'Future of Health': 'health',
             'Future of Money': 'economy',
             'Gabbard 2020': 'politics',
             'Global Investment 2018 Outlook': 'economy',
             'Global Investment Outlook 2019': 'economy',
             'Global Investment Outlook 2020': 'economy',
             'Golf': 'sport',
             'Government': 'politics',
             'Healthcare': 'health',
             'Healthcare & Pharma': 'health',
             'Healthcare & Pharmaceuticals': 'health',
             'Healthcare Facilities': 'health',
             'Healthcare Innovation': 'health',
             'Hedge Funds': 'economy',
             'India': 'asia/pac',
             'India Top News': 'asia/pac',
             'Industry, Materials & Utilities': 'economy',
             'Innovation and Intellectual Property': 'tech',
             'Internet News': 'tech',
             'Investment Trusts': 'economy',
             'Keeping Score Podcast': 'misc',
             'Legal ': 'law/justice',
             'Legal Industry': 'law/justice',
             'Lifestyle': 'lifestyle/culture',
             'Litigation': 'law/justice',
             'Live Coverage': 'world',
             'Markets': 'economy',
             'Media & Telecom': 'media',
             'Media Industry ': 'media',
             'Media News': 'media',
             'Media and Telecoms': 'media',
             'Medical Equipment, Supplies & Distribution': 'media',
             'Middle East': 'mideast',
             'Middle East & Africa': 'mideast',
             'Midterms: State of Play': 'politics',
             'Money': 'economy',
             'Money News': 'economy',
             'Music News': 'arts/entertainemnt',
             'News - ScribbleLive': 'us',
             'Oddly Enough': 'offbeat',
             'Olympics': 'sport',
             'On The Case': 'law/justice',
             'People & Celebrities': 'lifestyle/culture',
             'Picture': 'pic',
             'Politics': 'politics',
             'Politics Special Reports': 'politics',
             'Race for a cure': 'health',
             'Rates & Bonds': 'economy',
             'Regulatory News - Americas': 'economy',
             'Retail': 'economy',
             'Retail & Consumer': 'economy',
             'Retail - Drugs': 'economy',
             'Retirement': 'economy',
             'Reuters Com Service 2 MOLT': 'politics',
             'Reuters Next': 'opinion',
             'Sanders 2020': 'politics',
             'Science': 'science/environment',
             'Science & Space': 'science/environment',
             'Special Reports': 'economy',
             'Sports': 'sport',
             'Sports News': 'sport',
             'Stocks': 'economy',
             'Summit News': 'economy',
             'Sustainable Business': 'economy',
             'Take Five': 'economy',
             'Technology': 'tech',
             'Technology News': 'tech',
             'Technology, Media & Telecom - Innovation': 'tech',
             'Television News': 'arts/entertainment',
             'The Great Reboot': 'opinion',
             'Top News': 'world',
             'Transactional': 'business',
             'Trump 2020': 'politics',
             'Trump Effect': 'politics',
             'U.S. Legal News': 'law/justice',
             'U.S. Markets': 'economy',
             'U.S. News': 'us',
             'UK': 'uk',
             'UK Top News': 'uk',
             'US Markets': 'economy',
             'United Kingdom': 'uk',
             'United States': 'us',
             'Warren 2020': 'politics',
             'Wealth': 'economy',
             'Where to invest in 2021': 'economy',
             'Women': 'misc',
             'World': 'world',
             'World News': 'world',
             'World at Work': 'world',
             'americas-test-2': 'americas',
             'blank': 'blank',
             'everythingNews': 'world',
             'reboot-live': 'economy',
             'test': 'politics'}

def cat_standardiser(x):
    try:
        x=cat_dic_raw[x]
    except:
        x=x
    return x

article_features_df['category_stand']=articles_analysis['category'].apply(cat_standardiser)
temp_df=articles_analysis[article_features_df['category_stand']=='world']

with open('country_zone_dict', 'rb') as f:
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


global_to_local(temp_df, article_features_df)

#add outlet for use when merging into one df
article_features_df['outlet']='reuters'

with open('../data/reuters_articles_features', 'wb') as f:
    pickle.dump(article_features_df, f)


# check tweets df
with open('../data/reuters_twitter_articles_analysis', 'rb') as f:
    twitter_articles_analysis=pickle.load(f)

twitter_articles_analysis['clean']=twitter_articles_analysis['artText'].apply(text_cleaner)
twitter_articles_analysis['category']=twitter_articles_analysis['category'].apply(cat_standardiser)
tw_temp = twitter_articles_analysis[twitter_articles_analysis['category']=='world']
global_to_local(tw_temp, twitter_articles_analysis)

with open('../data/reuters_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_articles_analysis, f)

af1=articles_analysis.to_json()

with open('../data/reuters_articles_analysis_js', 'w') as f:
    json.dump(af1, f)
