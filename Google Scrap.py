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

# Scraps the reviews from one page, both the star ratings and comments
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
        meta.append(rev[i].text[1:-20])
        # Save meta data with the comment ( Rating + Review )
        output.append(meta)
    
    return output

# Returns the number of pages of reviews that need to be visited
def googleMaxPage(url):
    page = urll.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    maxPage = soup.find('span', attrs={'class':'pag-n-to-n-txt'})
    maxPage = re.sub('[^0-9]','', maxPage.text[-6:])
    # This returns the total number of reviews
    maxPage = int(maxPage)
    # There are 10 reviews per page
    maxPage = int(maxPage/10)-1
    
    return maxPage

# Scraps all reviews starting from page 1 as the input url
def googleScrap(url):
    
    maxPage = googleMaxPage(url)
    output = googlePageScrap(url)
    
    # Go to each page of reviews and add them to the output list
    for i in range(maxPage):
        urlPage = str(url + ',rstart:'+ str(i+1) +'0')
        new = googlePageScrap(urlPage)
        output = output + new
        print(i+1,' / ',maxPage)
    
    # Convert the list into a pandas dataframe
    output_df = pd.DataFrame(output)
    output_df.columns = ['stars', 'comments']

    return output_df    
#%%





#%% Scrap the data
url = 'https://www.google.com/shopping/product/8330308525491645368/reviews?output=search&q=apple+iphone+8&prds=paur:ClkAsKraX0HAK8DTxuQ7a_QLy1VVmmdGjqus04Pco-mYuwDAnhwY-2yRVwjDEGi_xEsNVx11gFrfhnTT-NU5F1Cv8xkFN2t2KRFYe2S0bJHgJvnYxGmE7Xr8KxIZAFPVH73QWHZfxejgLJJNz1emAuExXPnAxg,rsort:1'
iPhone8 = googleScrap(url)
#%%
url = 'https://www.google.com/shopping/product/5196767965601398683/reviews?output=search&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraX6xXlTCTDvTg5n66BfqjZtUzj5mRPstz9QYmLjncZZBAQRRtobM8Pe5XLEZX0CP8x5UxXIzT52WhOhO2moZSRoKU0aTE6QE0f-R3zq1xhh45Jvza8BIZAFPVH70FzB4_QX4D05ZaAMc8F9sjUFRwvg,rsort:1'
iPhoneX = googleScrap(url)
#%%
url = 'https://www.google.com/shopping/product/2874873357294577697/reviews?output=search&q=galaxy+s8&oq=galaxy+s8&prds=paur:ClkAsKraX4MdXEv-XobV-tsudUmMvrTaF0oUQFrnUCBf-gngBeSUnGe1TQzRN-qEvUxg11H4haqP6POwtI-P9rAtftKbUh-e4yFNzeeFNldak82GgWHBlGI__xIZAFPVH72dPmpO1V1eoP7Y9BbJQh6EoOBh5Q,rsort:1'
samsungS8 = googleScrap(url)
#%%





#%% Export data to csv
iPhoneX.to_csv('GoogleiPhoneX.csv')
#%%
iPhone8.to_csv('GoogleiPhone8.csv')
#%%
samsungS8.to_csv('GoogleSamsungS8.csv')
#%%





#%%

#%%




