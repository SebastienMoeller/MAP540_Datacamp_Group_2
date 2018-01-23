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
    maxPage = re.sub('[^0-9]','', maxPage.text[7:])
    # This returns the total number of reviews
    maxPage = int(maxPage)
    # There are 10 reviews per page
    maxPage = int(maxPage/10)-1
    
    if maxPage > 100:
        maxPage = 100
    
    return maxPage

# Scraps all reviews starting from page 1 as the input url
def googleScrap(url, maxPage = -1):
    
    # check if maxPage has been specified
    if maxPage <= 0:
        maxPage = googleMaxPage(url)

    output = googlePageScrap(url)
    
    # Go to each page of reviews and add them to the output list
    for i in range(maxPage):
        urlPage = str(url + ',rstart:'+ str(i+1) +'0')
        new = googlePageScrap(urlPage)
        output = output + new
        print(i+2,' / ',maxPage+1)
    
    # Convert the list into a pandas dataframe
    output_df = pd.DataFrame(output)
    output_df.columns = ['stars', 'comments']
    
    # Need to remove duplicates from shifted comments due to the computation time
    output_df = output_df.drop_duplicates('comments')
    
    return output_df 
#%%





#%% Scrap iPhoneX
url = 'https://www.google.com/shopping/product/5196767965601398683/reviews?biw=1440&bih=780&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraXws3xeqTK3deHJMV_BI6rHFLD1-0-FLCSIFjMFmaCLo2em084jq4mwxmOrTF7J6tYIUmyeVLi-DhUVQ0Fjy8o4PX0h-_9JRFgVPmFvO1FWV0-VPotxIZAFPVH70NFTJcwTbVgp4iH_8rHEcWzD4iaA,pub:Best+Buy,rsort:1'
iPhoneXBestBuy = googleScrap(url)

url = 'https://www.google.com/shopping/product/5196767965601398683/reviews?biw=1440&bih=780&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraXws3xeqTK3deHJMV_BI6rHFLD1-0-FLCSIFjMFmaCLo2em084jq4mwxmOrTF7J6tYIUmyeVLi-DhUVQ0Fjy8o4PX0h-_9JRFgVPmFvO1FWV0-VPotxIZAFPVH70NFTJcwTbVgp4iH_8rHEcWzD4iaA,pub:att.com,rsort:1'
iPhoneXATT = googleScrap(url, 47)

url = 'https://www.google.com/shopping/product/5196767965601398683/reviews?biw=1440&bih=780&q=iphone+x&oq=iphone+x&prds=paur:ClkAsKraXws3xeqTK3deHJMV_BI6rHFLD1-0-FLCSIFjMFmaCLo2em084jq4mwxmOrTF7J6tYIUmyeVLi-DhUVQ0Fjy8o4PX0h-_9JRFgVPmFvO1FWV0-VPotxIZAFPVH70NFTJcwTbVgp4iH_8rHEcWzD4iaA,pub:ProductReview.com.au,rsort:1'
iPhoneXPReview = googleScrap(url, 4)
#%%
iPhoneX = iPhoneXBestBuy.append(iPhoneXATT, ignore_index = True).append(iPhoneXPReview, ignore_index = True)
#%%





#%% Scrap iPhone8
url = 'https://www.google.com/shopping/product/2527512113670095639/reviews?biw=1440&bih=780&q=iphone+8&oq=iphone+8&prds=paur:ClkAsKraX1iYqFA45a1I8Lb2CHYpqvq-lseC5EVu1r36XMzGMc90uym5AnxzZ5-T7kEqBQiUsKNbFH2uQCvFKVj5hzCiSGPbHoNuDSMjeNsnjxQPsSGuAhn6WRIZAFPVH72zDOte2qPzas3yMWbOvnhzn3RUHg,pub:Best+Buy,rsort:1'
iPhone8BestBuy = googleScrap(url)

url = 'https://www.google.com/shopping/product/2527512113670095639/reviews?biw=1440&bih=780&q=iphone+8&oq=iphone+8&prds=paur:ClkAsKraX1iYqFA45a1I8Lb2CHYpqvq-lseC5EVu1r36XMzGMc90uym5AnxzZ5-T7kEqBQiUsKNbFH2uQCvFKVj5hzCiSGPbHoNuDSMjeNsnjxQPsSGuAhn6WRIZAFPVH72zDOte2qPzas3yMWbOvnhzn3RUHg,pub:att.com,rsort:1'
iPhone8ATT = googleScrap(url)

url = 'https://www.google.com/shopping/product/2527512113670095639/reviews?biw=1440&bih=780&q=iphone+8&oq=iphone+8&prds=paur:ClkAsKraX1iYqFA45a1I8Lb2CHYpqvq-lseC5EVu1r36XMzGMc90uym5AnxzZ5-T7kEqBQiUsKNbFH2uQCvFKVj5hzCiSGPbHoNuDSMjeNsnjxQPsSGuAhn6WRIZAFPVH72zDOte2qPzas3yMWbOvnhzn3RUHg,pub:vzw.com,rsort:1'
iPhone8VZW = googleScrap(url, 3)
#%%
iPhone8 = iPhone8BestBuy.append(iPhone8ATT, ignore_index = True).append(iPhone8VZW, ignore_index = True)
#%%





#%% Scrap Samsung S8
url= 'https://www.google.com/shopping/product/2874873357294577697/reviews?biw=1440&bih=780&output=search&q=galaxy+s8&oq=gal&prds=paur:ClkAsKraX-TlauU-GPtWQsD9gn21hudqQJu6LVfM3EroSWdCymyGQm80RnDEPkMqWFA_T7-FgYzaEPAa2-I88sQcJyE37ScXkhFuixfexe1H_y3QH11VYBgH_BIZAFPVH70HS8o9gj8YcYZIdk8G_GTZoBBn_A,pub:Best+Buy,rsort:1'
samsungS8BestBuy = googleScrap(url)

url = 'https://www.google.com/shopping/product/2874873357294577697/reviews?biw=1440&bih=780&output=search&q=galaxy+s8&oq=gal&prds=paur:ClkAsKraX-TlauU-GPtWQsD9gn21hudqQJu6LVfM3EroSWdCymyGQm80RnDEPkMqWFA_T7-FgYzaEPAa2-I88sQcJyE37ScXkhFuixfexe1H_y3QH11VYBgH_BIZAFPVH70HS8o9gj8YcYZIdk8G_GTZoBBn_A,pub:att.com,rsort:1'
samsungS8ATT = googleScrap(url)

url = 'https://www.google.com/shopping/product/2874873357294577697/reviews?biw=1440&bih=780&output=search&q=galaxy+s8&oq=gal&prds=paur:ClkAsKraX-TlauU-GPtWQsD9gn21hudqQJu6LVfM3EroSWdCymyGQm80RnDEPkMqWFA_T7-FgYzaEPAa2-I88sQcJyE37ScXkhFuixfexe1H_y3QH11VYBgH_BIZAFPVH70HS8o9gj8YcYZIdk8G_GTZoBBn_A,pub:Samsung,rsort:1'
samsungS8Samsung = googleScrap(url)
#%%
samsungS8 = samsungS8BestBuy.append(samsungS8ATT, ignore_index = True).append(samsungS8Samsung, ignore_index = True)
#%%



#%% Export data to csv
iPhone8.to_csv('GoogleiPhone8.csv')
#%%
iPhoneX.to_csv('GoogleiPhoneX.csv')
#%%
samsungS8.to_csv('GoogleSamsungS8.csv')
#%%





#%%
