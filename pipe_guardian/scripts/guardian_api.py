import json
import requests
import os
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta
import time
from pathlib import Path

path = Path(os.getcwd())

levels_up = 4
root=path.parents[levels_up+0]
kpath=f'{root}\gk.txt'
MY_API_KEY = open(kpath).read()

API_ENDPOINT = 'http://content.guardianapis.com/search'
my_params = {
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'api-key': MY_API_KEY
}

all_res=[]
start_date = date(2022, 2, 27)
count=0
# there is a daily download limit, so split the date into batches. The stories up until present day were 
# donwloaded previous day
end_date = date(2022, 3, 1)
dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    fname = f'../data/tempdata/articles/{datestr}.json'
    if not exists(fname):
        all_results = []
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        while current_page <= total_pages:
            my_params['page'] = current_page
            count+=1
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            all_results.extend(data['response']['results'])
            # if there is more than one page
            current_page += 1
            time.sleep(0.08)
            total_pages = data['response']['pages']
        with open(fname, 'w') as f:
            f.write(json.dumps(all_results, indent=2))

directory = '../data/tempdata/articles'
 
# iterate over files in
# that directory and create dic from json file. Only include features stipulated
article_responses = []
for filename in os.listdir(directory):
    json_file_path = os.path.join(directory, filename)
    with open(json_file_path, 'r') as j:
        contents = json.loads(j.read())
        contents = [item for item in contents if item['type']=='article']
        for con in contents:
            new_dic={}
            for k in ['id', 'sectionId', 'webPublicationDate']:
                new_dic[k] = con[k]
                for f in ['headline', 'byline', 'wordcount', 'bodyText']:
                    try:
                        new_dic[f] = con['fields'][f]
                    except:
                        new_dic[f] = f'no {f}'
            article_responses.append(new_dic)
                    
with open("../data/guardian_articles.json", 'w') as fl:
    json.dump(article_responses, fl, indent=2) 

