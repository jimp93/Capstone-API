#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import time
import pandas as pd
import os
import numpy as np
import json
import re


# In[2]:


with open('../data/guardian_articles_analysis', 'rb') as f:
    articles_analysis=pickle.load(f)


# In[2]:


with open('../data/guardian_article_features', 'rb') as f:
    article_features=pickle.load(f)


# In[3]:


articles_analysis.isnull().values.any()


# # Make clean columns

# In[ ]:


# to save memory, new features will be save in a separate dataframe, and merged when required


# In[5]:


article_features_df = pd.DataFrame()


# In[6]:


article_features_df['category']=articles_analysis['category']


# In[8]:


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


# In[9]:


article_features_df['clean_noquotes'] = articles_analysis['artText'].apply(tidy_noquotes)


# In[7]:


article_features_df['clean'] = articles_analysis['artText']


# In[8]:


article_features_df


# # Standardise categories

# ## convert world into geographic area by checking for country names in headline/lead

# In[9]:


cat_dic=articles_analysis['category'].value_counts().to_dict()


# In[10]:


#use keys from cat dic and fit keys into standardised categories
cat_dic_raw={'commentisfree':'opinion',
               'football': 'sport',
               'sport': 'sport',
               'music': 'arts/entertainment',
               'business': 'business',
               'politics': 'politics',
               'us-news': 'us',
               'australia-news': 'asia/pac',
               'uk-news': 'uk',
               'world': 'world', 
               'lifeandstyle': 'lifestyle/culture',
               'film': 'arts/entertainment',
               'books':'arts/entertainment',
               'environment': 'science/environment',
               'society': 'lifestyle/culture',
               'tv-and-radio': 'arts/entertainment',
               'media': 'media',
               'stage': 'arts/entertainment',
               'technology': 'tech',
               'money': 'economy',
               'europe': 'europe',
               'artanddesign': 'arts/entertainment',
               'education': 'education',
               'asia/pac': 'asia/pac',
               'science': 'science/environment',
               'food': 'food/drink',
               'culture': 'lifestyle/culture',
               'global-development': 'opinion',
               'fashion': 'lifestyle/culture',
               'travel': 'travel',
               'news': 'misc',
               'mideast': 'mideast',
               'us': 'us',
               'childrens-books-site': 'arts/entertainment',
               'uk': 'uk',
               'games': 'arts/entertainment',
               'sustainable-business': 'business',
               'global': 'world',
               'cities': 'economy',
               'small-business-network': 'business',
               'africa': 'africa',
               'law': 'law/justice',
               'americas': 'americas',
               'public-leaders-network': 'opinion',
               'media-network': 'media',
               'crosswords': 'misc',
               'teacher-network': 'education',
               'healthcare-network': 'opinion',
               'working-in-development': 'opinion',
               'social-care-network': 'opinion',
               'voluntary-sector-network': 'opinion',
               'careers': 'misc',
               'global-development-professionals-network': 'opinion',
               'guardian-masterclasses': 'misc',
               'housing-network': 'property',
               'theguardian': 'misc',
               'theobserver': 'misc',
               'women-in-leadership': 'opinion',
               'membership': 522,
               'gnm-press-office': 458,
               'community': 408,
               'culture-professionals-network': 'opinion',
               'inequality': 'politics',
               'info': 289,
               'sustainability': 'science/environment',
               'big-energy-debate': 'science/environment',
               'guardian-foundation': 82,
               'weather': 'science/environment',
               'society-professionals': 65,
               'all-in-all-together': 'opinion',
               'extra': 58,
               'help': 53,
               'vital-signs': 'science/environment',
               'business-to-business': 'economy',
               'guardian-us-press-office': 43,
               'the-last-taboo': 36,
               'animals-farmed': 'science/environment',
               '100-teachers': 'education',
               'teacher-network/zurich-school-competition': 28,
               'small-business-network/trade-mission': 26,
               'big-ideas': 26,
               'higher-education-network': 'education',
               'side-hustle': 'lifestyle/culture',
               'guardian-masterclasses-australia': 22,
               'advertising': 22,
               'observer-food-monthly-awards': 20,
               'observer-ethical-awards': 19,
               'shelf-improvement': 18,
               'best-of-birmingham': 'opinion',
               'the-invested-generation': 'opinion',
               'guardian-professional': 15,
               'guardian-film-awards-site': 13,
               'see-if-its-time-to-sell': 13,
               'future-focused-it': 'tech',
               'gnm-archive': 12,
               'feasting-with-ocado': 12,
               'focus': 'opinion',
               'british-gas-smart-meter-challenge': 11,
               'new-faces-of-tech': 'tech',
               'thinking-about-money': 'economy',
               'reader-events': 10,
               'norm-and-als-guide-to-being-normal': 9,
               'cancer-revolutionaries': 'health',
               'freshers-week': 9,
               'guardian-live-australia': 9,
               'sony-run-your-way': 8,
               'commonwealth-bank-australia-next-chapter': 8,
               'the-unstoppables': 8,
               'destination-nsw-uncover-the-unspoilt-south-coast': 'travel',
               'xero-resilient-business': 'business',
               'break-into-tech': 'tech',
               'further-education-share-your-skills': 7,
               'guide-to-fundraising': 7,
               'open-days': 7,
               'housing-matters': 'property',
               'salesforce-the-unfair-advantage': 7,
               'game-changing-skincare': 7,
               'mental-health-supplement-2019': 'health',
               'nederburg-cycling': 6,
               'supercharge-your-business': 'business',
               'student-media-awards-2014': 6,
               'early-careers-hub': 6,
               'retail-reimagined': 6,
               'guardian-clearing': 6,
               'the-community-first-retailer': 'business',
               'powershop-power-potential': 'opinion',
               'sbs-on-demand': 5,
               'industry-superfunds-supercharged-future': 'economy',
               'de-bortoli-going-green': 'science/environment',
               'future-ready-leadership': 5,
               'chromebook-helping-chinatown': 5,
               'square-good-business': 5,
               'green-your-pension': 'economy',
               'dairy-australia-we-need-to-talk': 8,
               'sap-solutions': 5,
               'knowledge-is-pleasure': 5,
               'wellbeing-at-work': 'health',
               'health-revolution': 'health',
               'readings-the-bookshelf': 'arts/entertainment',
               'katine': 5,
               'professional-supplements': 5,
               'what-is-nano': 'tech',
               'canneslions': 5,
               'quest-apartment-hotels-as-local-as-you-like-it': 'travel',
               'trade-boost': 'business',
               'opsm-life-in-focus': 4,
               'westpac-scholars-rethink-tomorrow': 4,
               'sbs-a-world-of-difference': 4,
               'reimagining-sustainability': 'science/environment',
               'forward-women': 4,
               'helgas-capturing-kindness': 4,
               'guardian-green-jobs': 4,
               'living-with-sensitive-skin': 'health',
               'bank-australia-people-australia-needs': 4,
               'hbf-never-settle': 4,
               'sbs-on-demand-new-gold-mountain': 4,
               'bank-australia-collective-good': 4,
               'game-set-and-watch': 4,
               'plan-the-perfect-ski-break': 'travel',
               'a-better-workplace': 4,
               'nab-more-that-matters': 4,
               'sustainable-home-improvements': 'sceince/environment',
               'reimagining-work': 4,
               'ing-direct-dreamstarter': 4,
               'meta-buy-blak': 4,
               'specsavers-focus-on-health': 'health',
               'minority-writers-workshop': 3,
               'the-university-of-melbourne-graduating-performances': 3,
               'brother-doing-business-well': 3,
               'sutton-care-services': 3,
               'one-change-competition': 3,
               'sonos-roam-anywhere': 3,
               'curtin-university-why-study-law': 3,
               'mazda-sustainable-style': 'auto/transport',
               'welcome-to-ontario': 'travel',
               'mini-serious-fun': 3,
               'mg-motor-switch-to-electric': 'auto/transport',
               'spotify-find-the-one': 3,
               'westpac-foundation-investing-in-social-enterprise': 3,
               'guardian-cities-on-the-road': 3,
               'sap-smart-business': 'business',
               'american-express-business-class': 3,
               'a-time-for-japan': 'asia/pac',
               'dairy-australia-healthy-sustainable-diets': 'health',
               'ing-do-your-thing': 3,
               'dairy-australia-sustainable-futures': 3,
               'dairy-australia-the-food-matrix': 3,
               'australia-post-creating-connections': 3,
               'guardian-australia-press-office': 3,
               'black-hawk-every-ingredient-matters': 3,
               'cardiff': 'uk',
               'wwf-renew-normal': 3,
               'qantas-insurance-rewarding-loyalty': 2,
               'diversity-matters': 2,
               'media-network/adobe-partner-zone': 2,
               'linkedin-hybrid-workplace': 2,
               'opsm-optimal-health': 'health',
               'michelin-built-to-keep-you-moving': 2,
               'sonos-hyper-real': 2,
               'about': 2,
               'dairy-australia-green-solutions': 2,
               'museums-victoria-virtual-museum-experience-2020': 'travel',
               'sustainable-connections': 2,
               'qatar-airways-experience-europe-your-way': 'travel',
               'specsavers-an-eye-for-art': 2,
               'tourism-tasmania-awaken-your-curious-side': 'travel',
               'dairy-australia-listen-to-your-gut': 2,
               'mobile': 2,
               'wildlife-photographer-of-the-year-nhm': 2,
               'university-of-melbourne-developing-leadership': 2,
               'bmw-sustainable-mobility': 2,
               'mirvac-voyager': 2,
               'state-library-victoria-reward-your-curiosity': 2,
               'wehi-brighter-together': 2,
               'felix-mobile-the-only-one': 2,
               'experience-samsung': 2,
               'destination-nsw-road-trips': 'travel',
               'snooze-investing-in-sleep': 2,
               'victoria-university-block-model-2021': 2,
               'sbs-on-demand--are-you-addicted-to-technology': 2,
               'specsavers-liberty-london': 2,
               'amazon-prime-video-truth-seekers': 2,
               'sbs-addicted-australia': 2,
               'britbox-best-of-brit-tv': 2,
               'west-australian-opera-discover-season-2022': 1,
               'michelin-driving-the-future-psev': 1,
               'go-further-with-an-apprenticeship': 1,
               'melbourne-museum-unearthing-an-icon': 1,
               'toyota-australia-journey-to-electric': 'auto/transport',
               'local-government-network': 1,
               'southern-cross-university-better-energy': 1,
               'gnmexhibitions': 1,
               'plico-renewable-energy': 1,
               'recruiters': 1,
               'opportunity-international-roundtables': 1,
               'griffith-university-make-it-matter': 1,
               'rspca-australia-approved-farming-scheme': 1,
               'health-forecast': 1,
               'curtin-university-humanities': 1,
               'hawaii-for-foodies': 'food/drink',
               'macquarie-home-of-electric-vehicles': 1,
               'searchlight-pictures-the-french-dispatch': 1,
               'nitv-always-was-always-will-be': 1,
               'kyco-full-transparency': 1,
               'searchlight-pictures-nightmare-alley': 1,
               'social-enterprise-network': 1,
               'west-australian-opera-season-2021': 1,
               'canna-small-space-gardening': 1,
               'releaseit-ready-to-rent': 1,
               'barnardos-roundtable': 1,
               'hbf-healthy-choices': 1,
               'disney-wandavision': 1,
               'belvoir-stop-girl': 1,
               'sydney-olympic-park-come-play': 1,
               'universal-pictures-the-united-states-vs-billie-holiday': 1,
               'cmc-markets-trading-decoder': 1,
               'unicef-world-immunisation-week-2021': 1,
               'tourism-nt-territory-art-trails': 1,
               'marketing-luxury-goods-feb-15': 1,
               'inclusive-sustainable-future': 1,
               'hugo-boss-man-of-today': 1,
               'how-to-solve-a-murder': 1,
               'open-platform': 1,
               'try-swedish': 1,
               'tourism-wa-best-of-the-west': 'travel',
               'full-of-beanz': 1,
               'observer-ideas': 1,
               'discover-culture': 'culture/lifestyle',
               'wa-museum-discovering-ancient-greece': 'culture/lifestyle',
               'assa-abloy-australia-yale-smart-locks': 1,
               'socialsuite-esp-reporting-comes-of-age': 1,
               'bunya-productions-the-leadership': 1,
               'cashrewards-shop-smarter': 1,
               'prodigy-living-students': 1,
               'edinburgh': 'uk',
               'accenture': 1,
               'plan-international-australia-covid-19-ripple-effects': 1,
               'monash-university-ask-a-lawyer': 1,
               'boutique-homes-my-home-my-way': 1,
               'ageing-population-advertisement-features': 1,
               'how-to-solve-a-murder-a-detectives-dilemma': 1}


# In[11]:


cat_dic_rname={}
for k in cat_dic_raw.keys():
    if type(cat_dic_raw[k]) == int:
        cat_dic_rname[k]='misc'
    else:
        cat_dic_rname[k]=cat_dic_raw[k]


# In[12]:


article_features_df['category_stand']=articles_analysis['category'].apply(lambda x: cat_dic_rname[x])


# In[ ]:





# In[13]:


temp_df=articles_analysis[articles_analysis['category']=='world']


# In[14]:


article_features_df


# In[15]:


with open('../../global_data/country_zone_dict', 'rb') as f:
    country_zone=json.load(f)


# In[16]:


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
            lead=main_df.loc[i, 'clean_noquotes'].split(".")[0]
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
                main_df.loc[i, 'category_stand']=top_score
            else:
                main_df.loc[i, 'category_stand']='world'
        else:
            main_df.loc[i, 'category_stand']='world'

        


# In[17]:


global_to_local(temp_df, article_features_df)


# In[20]:


#add outlet for use when merging into one df
article_features_df['outlet']='guardian'


# In[21]:


article_features_df


# In[18]:


with open('../data/guardian_article_features', 'wb') as f:
    pickle.dump(article_features_df, f)


# # to use in main

# In[22]:


guardian_articles_clean=articles_analysis.copy()


# In[23]:


guardian_articles_clean.drop('category', axis=1, inplace=True)


# In[24]:


guardian_articles_clean['clean']=article_features_df['clean'].apply(lambda x: x)


# In[25]:


guardian_articles_clean['category']=article_features_df['category_stand'].apply(lambda x: x)


# In[27]:


guardian_articles_clean.rename(columns={'clean':'text'}, inplace=True)


# In[29]:


guardian_articles_clean.drop('artText', axis=1, inplace=True)


# In[31]:


guardian_articles_clean=guardian_articles_clean.to_json()


# In[32]:


with open('../data/guardian_articles_clean_js', 'w') as f:
    json.dump(guardian_articles_clean, f)


# # check tweets df

# In[8]:


with open('../data/guardian_twitter_articles_analysis', 'rb') as f:
    twitter_articles_analysis=pickle.load(f)


# In[4]:


twitter_articles_analysis.isnull().values.any()


# In[7]:


twitter_articles_analysis['category']=twitter_articles_analysis['category'].apply(lambda x: cat_dic_rname[x])


# In[10]:


tw_temp = twitter_articles_analysis[twitter_articles_analysis['category']=='world']


# In[15]:


global_to_local(tw_temp, twitter_articles_analysis)


# In[17]:


with open('../data/guardian_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_articles_analysis, f)


# In[ ]:





# In[2]:


with open('../data/guardian_articles_clean', 'rb') as f:
    guardian_articles_clean=pickle.load(f)


# In[4]:


article_features


# In[5]:


af1=article_features.to_json()


# In[6]:


with open('../data/guardian_article_features_js', 'w') as f:
    json.dump(af1, f)


# In[ ]:




