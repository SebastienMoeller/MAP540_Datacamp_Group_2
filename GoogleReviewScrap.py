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
scrap = soup2.find_all('div', attrs={'class':'review-content'})

reviews = []

loop = 1
for i in scrap:
    reviews.append(i.text)
#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%
