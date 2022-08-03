#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pickle
import json


# In[ ]:


date_list=[]
for y in range(13,23):
    year = "20" + str(y)
    for m in range(1,13):
        if len(str(m)) ==1:
            month = "0" + str(m)
        else:
            month = str(m)     
        year_month = year + month
        if m in [4,6,9,11]:
            no_days=31
        elif m == 2:
            no_days =29
        else:
            no_days=32
        for d in range(1,no_days):
            if len(str(d)) ==1:
                day = "0" + str(d)
            else:
                day = str(d)
            year_month_day = year_month + day
            date_list.append(year_month_day)
            if year_month_day == "20220413":
                break
        else:
            continue
        break
    else:
        continue
    break


# In[ ]:


with open('../global_data/date_list', 'wb') as f:
    pickle.dump(date_list, f)


# In[13]:


countries_zone =  {'Andorra': 'europe',
                   'Afghanistan': 'mideast',
                   'Antigua': 'americas',
                   'Albania': 'europe',
                   'Armenia': 'asia/pac',
                   'Angola': 'africa',
                   'Argentina': 'americas',
                   'Austria': 'europe',
                   'Australia': 'asia/pac',
                   'Azerbaijan': 'asia/pac',
                   'Barbados': 'americas',
                   'Bangladesh': 'asia/pac',
                   'Belgium': 'europe',
                   'Burkina': 'africa',
                   'Bulgaria': 'europe',
                   'Bahrain': 'mideast',
                   'Burundi': 'africa',
                   'Benin': 'africa',
                   'Brunei': 'mideast',
                   'Bolivia': 'americas',
                   'Bahamas': 'americas',
                   'Bhutan': 'asia/pac',
                   'Botswana': 'africa',
                   'Belarus': 'europe',
                   'Belize': 'americas',
                   'America': 'us',
                   'US': 'us',
                   'United States': 'us',
                   'DRC': 'africa',
                   'Congo': 'africa',
                   "Ivoire": 'africa',
                   'Ivory': 'africa',
                   'Chile': 'americas',
                   'Cameroon': 'africa',
                   'Colombia': 'americas',
                   'China': 'asia/pac',
                   'Rica':'americas',
                   'Cuba':'americas',
                   'Verde':'americas',
                   'Cyprus':'europe',
                   'Czech':'europe',
                   'Germany':'europe',
                   'Djibouti':'africa',
                   'Denmark':'europe',
                   'Dominica':'americas',
                   'Dominican':'americas',
                   'Ecuador':'americas',
                   'Estonia':'europe',
                   'Egypt':'mideast',
                   'Eritrea':'africa',
                   'Ethiopia':'africa',
                   'Finland':'europe',
                   'Fiji':'asia/pac',
                   'France':'europe',
                   'Gabon':'africa',
                   'Georgia': 'europe',
                   'Ghana':'africa',
                   'Gambia':'africa',
                   'Guinea':'africa',
                   'Greece':'europe',
                   'Guatemala':'americas',
                   'Haiti':'americas',
                   'Bissau':'africa',
                   'Guyana':'americas',
                   'Honduras':'americas',
                   'Hungary':'europe',
                   'Indonesia':'asia/pac',
                   'Ireland':'europe',
                   'Israel':'mideast',
                   'India':'asia/pac',
                   'Iraq':'mideast',
                   'Iran':'mideast',
                   'Iceland':'europe',
                   'Italy':'europe',
                   'Jamaica':'americas',
                   'Jordan':'mideast',
                   'Japan':'asia/pac',
                   'Kenya':'africa',
                   'Kyrgyzstan':'asia/pac',
                   'Kiribati':'asia/pac',
                   'Korea':'asia/pac',
                   'Kuwait':'mideast',
                   'Lebanon':'mideast',
                   'Liechtenstein':'europe',
                   'Liberia':'africa',
                   'Lesotho':'africa',
                   'Lithuania':'europe',
                   'Luxembourg':'europe',
                   'Latvia':'europe',
                   'Libya':'mideast',
                   'Madagascar':'africa',
                   'Marshall':'asia/pac',
                   'Macedonia':'europe',
                   'Mali':'africa',
                   'Myanmar':'asia/pac',
                   'Mongolia':'asia/pac',
                   'Mauritania':'asia/pac',
                   'Malta':'europe',
                   'Mauritius':'asia/pac',
                   'Maldives':'asia/pac',
                   'Malawi':'africa',
                   'Mexico':'americas',
                   'Mozambique':'africa',
                   'Namibia':'africa',
                   'Niger':'africa',
                   'Nicaragua':'americas',
                   'Netherlands':'europe',
                   'Holland':'europe',
                   'Norway':'europe',
                   'Nepal':'asia/pac',
                   'Nauru':'asia/pac',
                   'Zealand':'asia/pac',
                   'Oman':'mideast',
                   'Panama':'americas',
                   'Peru':'americas',
                   'Papua':'asia/pac',
                   'PNG':'asia/pac',
                   'Philippines':'asia/pac',
                   'Pakistan':'asia/pac',
                   'Poland':'europe',
                   'Portugal':'europe',
                   'Palau':'asia/pac',
                   'Paraguay':'americas',
                   'Qatar':'mideast',
                   'Romania':'europe',
                   'Russia':'europe',
                   'Rwanda':'africa',
                   'Saudi':'mideast',
                   'Solomon':'asia/pac',
                   'Seychelles':'asia/pac',
                   'Sudan':'africa',
                   'Sweden':'europe',
                   'Singapore':'asia/pac',
                   'Slovenia':'europe',
                   'Slovakia':'europe',
                   'Sierra':'africa',
                   'Marino':'europe',
                   'Senegal':'africa',
                   'Somalia':'africa',
                   'Suriname':'americas',
                   'Sao_Tome':'africa',
                   'Syria':'mideast',
                   'Togo':'africa',
                   'Thailand':'asia/pac',
                   'Tajikistan':'asia/pac',
                   'Turkmenistan':'asia/pac',
                   'Tunisia':'mideast',
                   'Tonga':'asia/pac',
                   'Turkey':'europe',
                   'Trinidad':'americas',
                   'Tuvalu':'asia/pac',
                   'Tanzania':'africa',
                   'Ukraine':'europe',
                   'Uganda':'africa',
                   'Uruguay':'americas',
                   'Uzbekistan':'asia/pac',
                   'Vatican':'europe',
                   'Venezuela':'americas',
                   'Vietnam':'asia/pac',
                   'Vanuatu':'asia/pac',
                   'Yemen':'mideast',
                   'Zambia':'africa',
                   'Zimbabwe':'africa',
                   'Algeria':'mideast',
                   'Bosnia':'europe',
                   'Cambodia':'asia/pac',
                   'Chad':'africa',
                   'Comoros':'asia/pac',
                   'Croatia':'europe',
                   'Timor':'asia/pac',
                   'Salvador':'americas',
                   'Equatorial':'africa',
                   'Grenada':'americas',
                   'Kazakhstan':'asia/pac',
                   'Laos':'asia/pac',
                   'Micronesia':'asia/pac',
                   'Moldova':'europe',
                   'Monaco':'europe',
                   'Montenegro':'europe',
                   'Morocco':'mideast',
                   'Kitts':'americas',
                   'Lucia':'americas',
                   'Vincent':'americas',
                   'Samoa':'asia/pac',
                   'Serbia':'europe',
                   'Lanka':'asia/pac',
                   'Swaziland':'africa',
                   'Switzerland':'europe',
                   'Emirates':'mideast',
                   'UAE':'mideast',
                   'United Kingdom':'uk',
                   'UK':'uk',
                   'Britain':'uk',
                   'England':'uk',
                   'Scotland':'uk',
                   'Wales':'uk',
                   'Europe':'europe',
                   'European':'europe',
                   'Africa':'africa',
                   'African':'africa',
                   'American':'americas',
                   'Asia':'asia/pac',
                   'Asian':'asia/pac',
                   'Caribbean':'americas'}


# In[14]:


with open('../global_data/country_zone_dict', 'w') as f:
    json.dump(countries_zone, f)


# In[ ]:




