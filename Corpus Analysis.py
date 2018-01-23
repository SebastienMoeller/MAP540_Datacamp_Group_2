#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:15:31 2018

@author: Sebastien
"""

#%%
import pandas as pd
from textblob import TextBlob
from nltk.tokenize import TweetTokenizer
#%%
data = pd.read_csv('GoogleiPhoneX.csv', index_col = 0)
comments = data['comments'].tolist()
#%%





#%%
l = [item.lower() for item in comments]
#%% We establish a dictionary of the transformation
transformation = {a:" " for a in ['@','/','#','.','\\','!']}
text = ' '.join(l)                                  
text = text.translate(str.maketrans(transformation))
#print(text)
#%%





#%%
blob = TextBlob(text)
listOfWords = blob.words
#%%
tkzer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
token = tkzer.tokenize(text)
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
