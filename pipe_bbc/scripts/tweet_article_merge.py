import pickle
import time
import pandas as pd
import os
import numpy as np
import json

# Make df of articles to analyze. Is just a formatted copy of the scraped articles as we can't glean any
# from twitter outlinks as website doesn't allow it

with open('../data/bbc_articles_df', 'rb') as f:
    bbc_scrape_articles=pickle.load(f)

bbc_scrape_articles.drop_duplicates(subset='headline', inplace=True)
bbc_scrape_articles.reset_index(drop=True, inplace=True)
bbc_scrape_articles.rename(columns={'text':'artText', 'URL':'expURL'}, inplace=True)

with open('../data/bbc_articles_analysis', 'wb') as f:
    pickle.dump(bbc_scrape_articles, f)

# make df linking articles to tweets (import of colab created df which used similarity of tweets to article lead to link)

with open('../data/import_data/bbc_tw_art_similar', 'rb') as f:
    bbc_tw_art_similar=pickle.load(f)

bbc_tw_art_similar.drop(['headline_list', 'date_y', 'same_tweet?', 'text_list', 'tweet_summary', 'URL_list'], axis=1, inplace=True)
bbc_tw_art_similar.rename(columns={'date_x':'date', 'text':'artText', 'Text':'tweetText', 'Replies':'replies', 'Retweets':'retweets', 'Likes':'likes'}, inplace=True)

# bbc clean tweets was created in colab, combining world and uk dataframes
bbc_tweets = pd.read_csv('../data/import_data/all_bbc_tweets.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)


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

bbc_tweets=tweet_cleaner(bbc_tweets)
bbc_tweets=bbc_tweets.explode('URL_list')
bbc_tweets.rename(columns={'Text': 'tweetText','URL_list': 'shortURL', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)

# make dataframe of all tweets, with article if found
twitter_article_analysis=pd.concat([bbc_tw_art_similar, bbc_tweets])
twitter_article_analysis.drop_duplicates('tweetText', inplace=True)
twitter_article_analysis.drop('shortURL', axis=1, inplace=True)
twitter_article_analysis.reset_index(drop=True, inplace=True)

for tw in ['replies', 'retweets', 'likes']:
    twitter_article_analysis[tw]=twitter_article_analysis[tw].astype(int)

with open('../data/bbc_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)
