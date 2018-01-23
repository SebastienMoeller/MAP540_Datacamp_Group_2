#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:15:31 2018

@author: Sebastien
"""

#%%
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import collections
#%%
data = pd.read_csv('GoogleiPhoneX.csv', index_col = 0)
comments = data['comments'].tolist()
#comments = ['I LOVE this phone, my Wife has one..... @wifey #waddup. I\'ll be going in-to univErsiTY in 4 days. I won\'t give up until I\'ve won this phone phone phone please ~']
#%%





#%%
l = [item.lower() for item in comments]
#%% We establish a dictionary of the transformation
transformation = {a:" " for a in ['@','/','#','.','\\','!',',']}
text = ' '.join(l)                                  
text = text.translate(str.maketrans(transformation))

print(text)
#%%





#%%
english_stopwords = set(stopwords.words('english'))
#%%
tkzer = TweetTokenizer(preserve_case = False, strip_handles = True, reduce_len = True)
token = tkzer.tokenize(text)
#%%
tokens = [i for i in token if i not in english_stopwords]
#%%

#%%
def nGrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))
#%%
bigram = nGrams(tokens, 2)
trigram = nGrams(tokens, 3)

#%%
counter=collections.Counter(tokens)
print(counter)
#%%
countBigram = collections.Counter(bigram)
countTrigram = collections.Counter(trigram)
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
