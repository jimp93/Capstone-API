import json
import pandas as pd
import pickle

f = open('../data/tempdata/articles/guardian_articles.json')
guardian_articles = json.load(f)

guardian_articles_df = pd.DataFrame(guardian_articles)
guardian_articles_df = guardian_articles_df[['headline', 'bodyText', 'sectionId', 'webPublicationDate']]
guardian_articles_df.rename(columns = {'bodyText':'text', 'sectionId':'category', 'webPublicationDate':'date'}, inplace = True)

with open('articles/guardian_articles_df', 'wb') as f:
    pickle.dump(guardian_articles_df, f)
    
guardian_articles_df.category.value_counts()
guardian_articles_df
