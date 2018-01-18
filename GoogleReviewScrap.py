#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:25:20 2018

@author: Sebastien
"""

#%%
import urllib.request as urll
from bs4 import BeautifulSoup

def googlePageScrap(url):
    # Initializing BeautifulSoup
    page = urll.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    
    # Saving the nodes containing the reviews and ratings
    rev = soup.find_all('div', attrs={'class':'review-content'})
    rat = soup.find_all('div', attrs={'class':'_OBj'})
    
    # Ratings need to be extracted from the soup
    rating = []
    for i in range(len(rat)):
        # Convert to string otherwise .find() doesn't work
        rat[i] = str(rat[i])
        # Finding the index of the rating
        idx = rat[i].find('aria-label="')+len('aria-label="')
        # Save the rating in the rating list
        rating.append(int(rat[i][idx]))
    
    # The first entry is the average rating between all, therefore we delete it
    rating = rating[1:]
    
    # Building the output
    output = []
    for i in range(len(rev)):
        # Building meta data
        meta = []
        meta.append(rating[i])
        # Reviews can use the function .text to extract the actual reviews
        meta.append(rev[i].text)
        # Save meta data with the comment ( Rating + Review )
        output.append(meta)
    
    return output
#%%
def googleScrap(url):
    return None
#%%
# Scraping the number reviews to know the total number of pages to scrap
url = 'https://www.google.com/shopping/product/5933462846166885821/reviews?output=search&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraX_rF40LQy2-BzkgE8wgr55aIFvSNoLYTvzWp6ulZKN4SpoI7JqPpChbztn5oHhXayw0IKumMhPjVOPJAvphyMoDnPXS1BcAGxwJNxOu6YHRwRxy_hxIZAFPVH71vJWF51zJw3MuI7eIHMGOCaLxvHA,rsort:1'
page = urll.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
test = soup.find('span', attrs={'class':'pag-n-to-n-txt'})
test = test.text
test = test[-5:]
test = test.replace('\xa0','')
test = int(test)

#%%
url = 'https://www.google.com/shopping/product/5933462846166885821/reviews?output=search&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraX_rF40LQy2-BzkgE8wgr55aIFvSNoLYTvzWp6ulZKN4SpoI7JqPpChbztn5oHhXayw0IKumMhPjVOPJAvphyMoDnPXS1BcAGxwJNxOu6YHRwRxy_hxIZAFPVH71vJWF51zJw3MuI7eIHMGOCaLxvHA,rsort:1'
data = googlePageScrap(url)
#%%
url = 'https://www.google.com/shopping/product/5933462846166885821/reviews?output=search&q=iphone%20x&oq=iphone%20x&prds=paur:ClkAsKraX_rF40LQy2-BzkgE8wgr55aIFvSNoLYTvzWp6ulZKN4SpoI7JqPpChbztn5oHhXayw0IKumMhPjVOPJAvphyMoDnPXS1BcAGxwJNxOu6YHRwRxy_hxIZAFPVH71vJWF51zJw3MuI7eIHMGOCaLxvHA,rsort:1,rstart:10'
data2 = googlePageScrap(url)

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%

#%%
