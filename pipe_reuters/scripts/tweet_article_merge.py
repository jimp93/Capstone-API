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

with open('../data/import_data/reuters_dic', 'rb') as f:
    dic1=json.load(f)

outlink_art_df=pd.DataFrame.from_dict(dic1, orient = 'index', columns=['expURL', 'category', 'headline', 'date', 'text'])
outlink_art_df.reset_index(inplace=True)
outlink_art_df.rename(columns={'index':'shortURL', 'text':'artText'}, inplace=True)


# link tweets df to the df above (one article maybe linked to by more than one tweet)
reuters_tweets = pd.read_csv('../data/reuters_tweets_df.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)
reuters_tweets=reuters_tweets.explode('Outlinks')
reuters_tweets.drop_duplicates(inplace=True)
reuters_tweets.reset_index(drop=True, inplace=True)
reuters_tweets.rename(columns={'headline':'tweetText','Outlinks': 'shortURL', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)
tweet_sc_art_join = outlink_art_df.merge(reuters_tweets, on='shortURL', how='outer')
tweet_sc_art_join.drop('date_x', axis=1, inplace=True)
tweet_sc_art_join.drop_duplicates(inplace=True)
tweet_sc_art_join.reset_index(drop=True, inplace=True)
tweet_sc_art_join.rename(columns={'date_y':'date'}, inplace=True)


# make another df linking the scraped articles and tweet where summary is same as headline
with open('../data/reuters_articles_df', 'rb') as f:
    reuters_scrape_articles=pickle.load(f)

reuters_tw_art = reuters_scrape_articles.merge(reuters_tweets, left_on='headline', right_on='tweetText')
reuters_tw_art.rename(columns={'URL':'expURL', 'text':'artText', 'date_x':'date', 'Text':'tweetText', 'Replies':'replies', 'Retweets':'retweets', 'Likes':'likes'}, inplace=True)
reuters_tw_art.drop('date_y', axis=1, inplace=True)
full_join = pd.concat([tweet_sc_art_join, reuters_tw_art])
full_join.reset_index(drop=True, inplace=True)

# full join is essentially reconstructing the original tweets dataframe, adding the articles. 
# we did this by linking rows where tweet was same as headline (cnn_tw_art) and by retrieving 
# articles where they weren't by opening the hyperlink in the tweet and scraping article (tweet_sc_art_join). 

# Make df of all articles, joining original scrape with twitter links

# we have the original scraped article df, but we may have found more when scraping from the tweet hyperlinks
# need to concat the two dataframes and drop duplicates 
reuters_scrape_articles.drop_duplicates(subset='headline', inplace=True)
reuters_scrape_articles.rename(columns={'text':'artText', 'URL':'expURL'}, inplace=True)
article_analysis = pd.concat([reuters_scrape_articles, full_join])
article_analysis.drop(['replies', 'retweets', 'likes', 'tweetText', 'shortURL'], axis=1, inplace=True)
article_analysis.drop_duplicates(subset=['headline', 'artText'], inplace=True)
article_analysis.reset_index(drop=True, inplace=True)
article_analysis=article_analysis.dropna(subset=['artText'])
index_names = article_analysis[article_analysis['artText'] == 'blanket' ].index
article_analysis.drop(index_names, inplace=True)
article_analysis.drop_duplicates(subset='headline', inplace=True)
article_analysis.reset_index(drop=True, inplace=True)
article_analysis['date'] = article_analysis['date'].replace('nan', np.nan).fillna(0)
article_analysis['date']=article_analysis['date'].astype(str)
article_analysis['date'] =article_analysis['date'].apply(lambda x: x[:10])

with open('../data/reuters_articles_analysis', 'wb') as f:
    pickle.dump(article_analysis, f)

# Make df of all tweets, linked to the article
twitter_article_analysis=full_join.copy()
twitter_article_analysis.drop('shortURL', axis=1, inplace=True)
twitter_article_analysis['date'] = twitter_article_analysis['date'].astype(str)
twitter_article_analysis['date'] = twitter_article_analysis['date'].apply(lambda x: x[:10])

with open('../data/reuters_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)
