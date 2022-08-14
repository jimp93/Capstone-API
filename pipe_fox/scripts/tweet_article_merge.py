import bs4 as bs
import pickle
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import os
import numpy as np


# make dataframe of articles scraped on colab using twitter outlinks

# open the dic made in colab. The outlink from each tweet in the tweet_df is the key
# the headline, section, article text and expanded url are the values
# we only use outlinks for tweets where the tweet is differnt from the article headline, which we 
# found out be merging tweet_df and articles_df. Would be a waste of time to scrape those outlinks as 
# we already linked the tweet to article
with open('../data/import_data/fox_dic', 'rb') as f:
    dic1=json.load(f)

outlink_art_df=pd.DataFrame.from_dict(dic1, orient = 'index', columns=['expURL', 'category', 'headline', 'date', 'artText'])
outlink_art_df.reset_index(inplace=True)
outlink_art_df.rename(columns={'index':'shortURL', 'text':'artText'}, inplace=True)

# link tweets df to the df above (one article maybe linked to by more than one tweet)

fox_tweets = pd.read_csv('../data/fox_tweets_df.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)
fox_tweets=fox_tweets.explode('Outlinks')
fox_tweets.rename(columns={'Text': 'tweetText', 'headline':'tweetText','Outlinks': 'shortURL', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)
tweet_sc_art_join = outlink_art_df.merge(fox_tweets, on='shortURL', how='outer')
tweet_sc_art_join['Datetime'] = tweet_sc_art_join['Datetime'].apply(lambda x: x[:10])
tweet_sc_art_join.drop('date', axis=1, inplace=True)
tweet_sc_art_join.rename(columns={'Datetime': 'date'}, inplace=True)
tweet_sc_art_join.drop_duplicates(inplace=True)
tweet_sc_art_join.reset_index(drop=True, inplace=True)

# make another df linking the scraped articles and tweet where summary is same as headline

with open('../data/fox_articles_df', 'rb') as f:
    fox_scrape_articles=pickle.load(f)

#need to clean tweets to get rid of hyperlink
fox_tweets.Datetime=fox_tweets.Datetime.apply(lambda x: x[:10])
fox_tweets.rename(columns={'Datetime':'date'}, inplace=True)

def tweet_cleaner(x):
    if x!='blank':
        x = x.partition('http')[0].strip('"\n .,!?"')
    return x

fox_tweets['tweetText'] = fox_tweets['tweetText'].apply(tweet_cleaner)
fox_tw_art = fox_scrape_articles.merge(fox_tweets, left_on='headline', right_on='tweetText')
fox_tw_art.rename(columns={'URL':'expURL', 'text':'artText', 'date_x':'date', 'Text':'tweetText', 'Replies':'replies', 'Retweets':'retweets', 'Likes':'likes'}, inplace=True)
fox_tw_art.drop('date_y', axis=1, inplace=True)
full_join = pd.concat([tweet_sc_art_join, fox_tw_art])
full_join.reset_index(drop=True, inplace=True)

#full join is essentially reconstructing the original tweets dataframe, adding the articles. 
# we did this by linking rows where tweet was same as headline (cnn_tw_art) and by retrieving 
# articles where they weren't by opening the hyperlink in the tweet and scraping article (tweet_sc_art_join). 

# Make df of all articles, joining original scrape with twitter links

# we have the original scraped article df, but we may have found more when scraping from the tweet hyperlinks
# need to concat the two dataframes and drop duplicates 

fox_scrape_articles.drop_duplicates(subset='headline', inplace=True)
fox_scrape_articles.reset_index(drop=True, inplace=True)
fox_scrape_articles.rename(columns={'text':'artText', 'URL':'expURL'}, inplace=True)
fox_scrape_articles
article_analysis = pd.concat([fox_scrape_articles, full_join])
article_analysis.drop(['replies', 'retweets', 'likes', 'tweetText', 'shortURL'], axis=1, inplace=True)
article_analysis.drop_duplicates(subset=['headline', 'artText'], inplace=True) 
article_analysis.reset_index(drop=True, inplace=True)
article_analysis=article_analysis.dropna(subset=['artText'])
index_names = article_analysis[article_analysis['artText'] == 'blank' ].index
article_analysis.drop(index_names, inplace = True)
article_analysis.reset_index(drop=True, inplace=True)
article_analysis.drop_duplicates(subset='headline', inplace=True)
article_analysis.reset_index(drop=True, inplace=True)

with open('../data/fox_articles_analysis', 'wb') as f:
    pickle.dump(article_analysis, f)


# Make df of all tweets, linked to the article
twitter_article_analysis=full_join.copy()
twitter_article_analysis.drop('shortURL', axis=1, inplace=True)
twitter_article_analysis.drop_duplicates(subset='tweetText', inplace=True)
twitter_article_analysis.reset_index(drop=True, inplace=True)

for tw in ['replies', 'retweets', 'likes']:
    twitter_article_analysis[tw]=twitter_article_analysis[tw].astype(int)

with open('../data/fox_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)
