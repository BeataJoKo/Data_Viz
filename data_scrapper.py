# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 19:58:35 2024

@author: BeButton
"""

#%%
import re
import os
import urllib
import requests
import time
import itertools
from bs4 import BeautifulSoup
import pandas as pd

#%%
df_base = pd.read_csv('data/base_data_2018_2023.csv')

#%%
museums = list(df_base['Name'].unique())

#%%
data = []

#%%   
S_URL = 'https://danmarksmuseer.dk'
action = '/index.php?id=19'
url = urllib.parse.urljoin(S_URL, action)

#%%
for museum in museums:
    form = {
        'tx_nxmuseumsearch_search[museums][searchstring]': museum
        }
    response = requests.post(url, data=form)
    if response.status_code == 200:
        print("Form submitted successfully!")

        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='nx_resultrow')
        
        for result in results:
            museum_name = result.find('h3').text.strip()      
            website_url = result.find('a', class_='btn btn-default hjemmeside')['href']

            print("Museum Name:", museum_name)
            print("Website URL:", website_url)
            print("\n---\n")
            data.append((museum, website_url))

    else:
        print(f"Failed to submit form. Status code: {response.status_code}")
        
#%%
check_missing = [e[0] for e in data]
check_missing = list(set(check_missing))

count = 0
for museum in museums:
    if museum not in check_missing:
        data.append((museum, ''))
        count += 1
print(count)        

#%%
    
#%%   
df = pd.DataFrame(data, columns =['Name', 'Url'])

#%%
df.to_excel('museum_websites.xlsx', sheet_name='scrapped')

#%%

