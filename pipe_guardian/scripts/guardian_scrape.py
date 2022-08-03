#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import pickle


# In[3]:


f = open('../data/tempdata/articles/guardian_articles.json')
guardian_articles = json.load(f)


# In[4]:


guardian_articles_df = pd.DataFrame(guardian_articles)


# In[5]:


guardian_articles_df = guardian_articles_df[['headline', 'bodyText', 'sectionId', 'webPublicationDate']]


# In[6]:


guardian_articles_df.rename(columns = {'bodyText':'text', 'sectionId':'category', 'webPublicationDate':'date'}, inplace = True)


# In[21]:


with open('articles/guardian_articles_df', 'wb') as f:
    pickle.dump(guardian_articles_df, f)


# In[7]:


guardian_articles_df.category.value_counts()


# In[8]:


guardian_articles_df


# In[ ]:




