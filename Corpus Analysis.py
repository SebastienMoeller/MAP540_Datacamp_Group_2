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
from collections import Counter as count
#%% 
# Importing all comments
amazonSamsungS8 = pd.read_csv('AmazonSamsungS8.csv', index_col = 0)
googleSamsungS8 = pd.read_csv('GoogleSamsungS8.csv', index_col = 0)
# Convert to list for later steps
amazonComments = amazonSamsungS8['comments'].tolist()
googleComments = googleSamsungS8['comments'].tolist()
#%% 
# sample comment to test outputs
#comments = ['I LOVE this phone, my Wife has one..... @wife #waddup. I\'ll be going in-to univErsiTY in 4 days. I won\'t give up until I\'ve won this phone phone phone please ~']
#%% 
# Lets only look at reviews with a rating of 3 and below
#amazonComments = amazonSamsungS8[amazonSamsungS8['stars']<=3]['comments'].tolist()
#googleComments = googleSamsungS8[googleSamsungS8['stars']<=3]['comments'].tolist()
comments = amazonComments + googleComments
#%%





#%%
#from nltk.corpus import stopwords
#from nltk.tokenize import TweetTokenizer

# given a list of comments, the function will return a list of tokens with -
# special characters and english stopwords removed. This format is useful -
# for further text analysis.
def tokenize(my_list):
    # Lowercase all characters 
    # (like this the same word will contribute to the same token count)
    comments = [item.lower() for item in my_list]
    # Combine all comments into a single string
    comments = ' '.join(comments)
    # We establish a dictionary of the transformation: characters to replace with a space
    transformation = {a:' ' for a in ['@','/','#','.','\\','!',',','(',')','{','}','[',']','-',"'",'~','’','"']}                                
    comments = comments.translate(str.maketrans(transformation))
    
    # nltk's tokenizer
    tkzer = TweetTokenizer(preserve_case = False, strip_handles = True, reduce_len = True)
    tokens = tkzer.tokenize(comments)
    # set of english stopwords
    english_stopwords = set(stopwords.words('english'))
    # Remove english stopwords
    tokens = [i for i in tokens if i not in english_stopwords]
    
    return tokens

# given a list of ordered tokens from a document, the function will return-
# a list of neighbouring groups of size n.
def nGrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))
#%%
    




#%%
tokens = tokenize(comments)
#%%
countMonogram = count(nGrams(tokens, 1))
countBigram = count(nGrams(tokens, 2))
countTrigram = count(nGrams(tokens, 3))
#%%
countMonogram.most_common(30)
#%%
countBigram.most_common(30)
#%%
countTrigram.most_common(30)
#%%





#%%
import matplotlib.pyplot as plt

def gramGraph(tokens, n, name, top = 30):
    countGram = count(nGrams(tokens, n))
    test = countGram.most_common(top)
    
    labels = []
    values = []
    indexes = range(len(test))
    for i in indexes:
        labels.append(', '.join(test[i][0]))
        values.append(test[i][1])
    
    fig = plt.gcf()
    fig.set_size_inches(.7*top, 10)
    
    plt.bar(indexes, values, 1)
    plt.xticks(indexes, labels, rotation = 70, ha='right')
    plt.title(name, fontsize = 20)
    
    return fig
#%%





#%%
fig = gramGraph(tokens, 1, 'Samsung S8 Top 20 Monograms', 20)
fig.savefig('Plot Monogram S8 Top 20', bbox_inches = 'tight')
#%%
fig = gramGraph(tokens, 2, 'Samsung S8 Top 20 Bigrams', 20)
fig.savefig('Plot Bigram S8 Top 20', bbox_inches = 'tight')
#%%
fig = gramGraph(tokens, 3, 'Samsung S8 Top 20 Trigrams', 20)
fig.savefig('Plot Trigram S8 Top 20', bbox_inches = 'tight')
#%%

#%%

#%%























