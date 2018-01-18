#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:25:20 2018

@author: Sebastien
"""

#%%
import urllib.request as urll
from bs4 import BeautifulSoup
#%%
url = 'https://www.google.com/shopping/product/5933462846166885821/reviews?output=search&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraX_rF40LQy2-BzkgE8wgr55aIFvSNoLYTvzWp6ulZKN4SpoI7JqPpChbztn5oHhXayw0IKumMhPjVOPJAvphyMoDnPXS1BcAGxwJNxOu6YHRwRxy_hxIZAFPVH71vJWF51zJw3MuI7eIHMGOCaLxvHA&sa=X&ved=0ahUKEwia_pa7zuHYAhUDbFAKHeWAAdEQqSQIqwE'
page2 = urll.urlopen(url)
soup2 = BeautifulSoup(page2, 'html.parser')
#%%
# scrap reviews
scrap = soup2.find_all('div', attrs={'class':'review-content'})
#%%
# Save reviews in a list
reviews = []
loop = 1
for i in scrap:
    meta = []
    meta.append(i.text)
    reviews.append(meta)
#%%
# Scrap the star rating
    
#%%
# Scrap star rating and add to data structure
for i in reviews:
    i.append('rating')
#%%
# Retrieve rating
reviews[0][1]
#%%

#%%

#%%

#%%

#%%

#%%

#%%
