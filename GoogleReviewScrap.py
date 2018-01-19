#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:25:20 2018

@author: Sebastien
"""

#%%
import urllib.request as urll
from bs4 import BeautifulSoup
import re
import pandas as pd

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

def googleMaxPage(url):
    page = urll.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    maxPage = soup.find('span', attrs={'class':'pag-n-to-n-txt'})
    maxPage = re.sub('[^0-9]','', maxPage.text[-5:])
    # This returns the total number of reviews
    maxPage = int(maxPage)
    # There are 10 reviews per page
    maxPage = int(maxPage/10)-1
    
    return maxPage

def googleScrap(url):
    
    maxPage = googleMaxPage(url)
    output = googlePageScrap(url)
    
    for i in range(maxPage):
        urlPage = str(url + ',rstart:'+ str(i+1) +'0')
        new = googlePageScrap(urlPage)
        output = output + new
    
    output_df = pd.DataFrame(output)
    output_df.columns = ['stars', 'comments']

    return output_df    
#%%





#%% Scrap the data
url = 'https://www.google.com/shopping/product/5933462846166885821/reviews?output=search&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraX_rF40LQy2-BzkgE8wgr55aIFvSNoLYTvzWp6ulZKN4SpoI7JqPpChbztn5oHhXayw0IKumMhPjVOPJAvphyMoDnPXS1BcAGxwJNxOu6YHRwRxy_hxIZAFPVH71vJWF51zJw3MuI7eIHMGOCaLxvHA,rsort:1'
iPhoneX = googleScrap(url)
#%%
url = 'https://www.google.com/shopping/product/15759308961534611032/reviews?newwindow=1&q=iphone+8&oq=iphone+8&prds=paur:ClkAsKraX1KyZbb72-_nOauyJ6tLxfYSpRr11Qd82QzPDzWCGdDhySawrVvlfUwE361hwlKO6m2_UM3ZtvT0PZX01Rnh2VSOukPheljUtLai0H60NM31aPbTpxIZAFPVH71cIy-DnJuBCRz3iNUXJsDhFf4Veg,rsort:1'
iPhone8Plus = googleScrap(url)
#%%
url = 'https://www.google.com/shopping/product/5683373131666675199/reviews?newwindow=1&q=samsung+galaxy+s8&oq=samsung+g&prds=paur:ClkAsKraX-qS4Yu6pMv3Uu2hhUR8yvGlxoy8OKgyMpEZY5CwQIjsU21Q7fX_RoPUB1CRK-u6sfMWemxcnbrnjQciLpfPBklvcIbWCNi-nOgQQaz6DWxL09jV5hIZAFPVH71iXF5HAM4_3oWDT_y1BYhBqRWlCg,rsort:1'
samsungS8 = googleScrap(url)
#%%





#%% Export data to csv
iPhoneX.to_csv('GoogleiPhoneX.csv')
iPhone8Plus.to_csv('GoogleiPhone8Plus.csv')
samsungS8.to_csv('GoogleSamsungS8.csv')
#%%





#%%
