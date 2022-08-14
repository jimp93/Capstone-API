import pickle
import pandas as pd
import os
import numpy as np
import json 


# make dataframe of articles scraped on colab using twitter outlinks

# open the dic made in colab. The outlink from each tweet in the tweet_df is the key
# the headline, section, article text and expanded url are the values
# we only use outlinks for tweets where the tweet is differnt from the article headline, which we 
# found out be merging tweet_df and articles_df. Would be a waste of time to scrape those outlinks as 
# we already linked the tweet to article

with open('../data/import_data/cnn_dic', 'rb') as f:
    dic1=json.load(f)

outlink_art_df=pd.DataFrame.from_dict(dic1, orient = 'index', columns=['expURL', 'category', 'headline', 'date', 'artText'])
outlink_art_df.reset_index(inplace=True)
outlink_art_df.rename(columns={'index':'shortURL', 'text':'artText'}, inplace=True)


# link tweets df to the df above (one article maybe linked to by more than one tweet)
cnn_tweets = pd.read_csv('../data/cnn_tweets_df.csv', converters={"Outlinks": lambda x: x.strip("[]").replace("'","").split(", ")}, low_memory=False)
cnn_tweets=cnn_tweets.explode('Outlinks')
cnn_tweets.rename(columns={'Text': 'tweetText', 'headline':'tweetText','Outlinks': 'shortURL', 'Replies':'replies', 'Retweets': 'retweets', 'Likes':'likes'}, inplace=True)
tweet_sc_art_join = outlink_art_df.merge(cnn_tweets, on='shortURL', how='outer')
tweet_sc_art_join['Datetime'] = tweet_sc_art_join['Datetime'].apply(lambda x: x[:10])
tweet_sc_art_join.drop('date', axis=1, inplace=True)
tweet_sc_art_join.rename(columns={'Datetime': 'date'}, inplace=True)
tweet_sc_art_join.drop_duplicates(inplace=True)
tweet_sc_art_join.reset_index(drop=True, inplace=True)

# make another df linking the scraped articles and tweet where summary is same as headline
with open('../data/cnn_articles_df', 'rb') as f:
    cnn_scrape_articles=pickle.load(f)

#need to clean tweets to get rid of hyperlink
cnn_tweets.Datetime=cnn_tweets.Datetime.apply(lambda x: x[:10])
cnn_tweets.rename(columns={'Datetime':'date'}, inplace=True)

def text_cleaner(x):
    if x!='blank':
        x = x.partition('http')
        x=x[0].strip()
    return x

cnn_tweets['tweetText']=cnn_tweets['tweetText'].apply(text_cleaner)
cnn_tw_art = cnn_scrape_articles.merge(cnn_tweets, left_on='headline', right_on='tweetText')
cnn_tw_art.rename(columns={'URL':'expURL', 'text':'artText', 'date_x':'date', 'Text':'tweetText', 'Replies':'replies', 'Retweets':'retweets', 'Likes':'likes'}, inplace=True)
cnn_tw_art.drop('date_y', axis=1, inplace=True)
full_join = pd.concat([tweet_sc_art_join, cnn_tw_art])
full_join.reset_index(drop=True, inplace=True)

# full join is essentially reconstructing the original tweets dataframe, adding the articles. 
# we did this by linking rows where tweet was same as headline (cnn_tw_art) and by retrieving 
# articles where they weren't by opening the hyperlink in the tweet and scraping article (tweet_sc_art_join). 

# Make df of all articles, joining original scrape with twitter links

# we have the original scraped article df, but we may have found more when scraping from the tweet hyperlinks
# need to concat the two dataframes and drop duplicates 
cnn_scrape_articles.drop_duplicates(subset='headline', inplace=True)
cnn_scrape_articles.reset_index(drop=True, inplace=True)
cnn_scrape_articles.rename(columns={'text':'artText', 'URL':'expURL'}, inplace=True)
article_analysis = pd.concat([cnn_scrape_articles, full_join])
article_analysis.drop(['replies', 'retweets', 'likes', 'tweetText', 'shortURL'], axis=1, inplace=True)
article_analysis.drop_duplicates(subset=['headline', 'artText'], inplace=True)
article_analysis.reset_index(drop=True, inplace=True)
article_analysis=article_analysis.dropna(subset=['artText'])
index_names = article_analysis[article_analysis['artText'] == 'blank' ].index
article_analysis.drop(index_names, inplace=True)
index_names = article_analysis[article_analysis['artText'] == '' ].index
article_analysis.drop(index_names, inplace=True)
article_analysis.reset_index(drop=True, inplace=True)
article_analysis.drop_duplicates(subset='headline', inplace=True)
article_analysis=article_analysis.dropna(subset=['artText'])
article_analysis.reset_index(drop=True, inplace=True)

with open('../data/cnn_articles_analysis', 'wb') as f:
    pickle.dump(article_analysis, f)

# Make df of all tweets, linked to the article
twitter_article_analysis=full_join.copy()
twitter_article_analysis.drop('shortURL', axis=1, inplace=True)
twitter_article_analysis.drop_duplicates(subset='tweetText', inplace=True)
twitter_article_analysis.reset_index(drop=True, inplace=True)
twitter_article_analysis

for tw in ['replies', 'retweets', 'likes']:
    twitter_article_analysis[tw]=twitter_article_analysis[tw].astype(int)

with open('../data/cnn_twitter_articles_analysis', 'wb') as f:
    pickle.dump(twitter_article_analysis, f)
