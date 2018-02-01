#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:17:00 2018

@author: Sebastien
"""

#%%
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer

#%%
#corpus = pd.read_csv('tfidf_monogram.csv')

#%%
data = pd.read_csv('data_scraping_V2.csv', encoding = 'ISO-8859-1')
comments = data['text'].tolist()

#%%
def tokenList(my_list):
    # Lowercase all characters 
    # (like this the same word will contribute to the same token count)
    comments = [item.lower() for item in my_list]
    # We establish a dictionary of the transformation: characters to replace with a space
    # We also want to remove context words that don't have meaning
    transformation = {a:' ' for a in ['@','/','#','.','\\','!',',','(',')','{','}','[',']','-','~', '*','?','+', '8', '7', '6', ';', ':', '|']}
    transB = {b:'' for b in ['','’','"']}
    comments = [item.translate(str.maketrans(transformation)) for item in comments]
    comments = [item.translate(str.maketrans(transB)) for item in comments]
    comments = [item.replace('iphone', ' ').replace('samsung', ' ').replace('galaxy', ' ').replace('apple', ' ').replace('plus', ' ').replace(
            ' x ', ' ').replace('’', '').replace("'", '').replace('http', '').replace('https', '').replace('com', ' ') for item in comments]
    
    # nltk's tokenizer
    tkzer = TweetTokenizer(preserve_case = False, strip_handles = True, reduce_len = True)
    tokens = [tkzer.tokenize(item) for item in comments]
    
    tokens = []
    wordnet_lemmatizer = WordNetLemmatizer()
    for idx in range(len(comments)):
        # Remove engish stopwords
        words = ([word for word in comments[idx].split() if word not in stopwords.words('english')])
        for idy in range(len(words)):
            # Lemmatize each word
            words[idy] = wordnet_lemmatizer.lemmatize(words[idy], pos = 'v')
        
        tokens.append(words)
        # Progress report
        print('Tokenizing: ',idx+1, ' / ', len(comments))

    return tokens

# given a list of ordered tokens from a document, the function will return-
# a list of neighbouring groups of size n.
def nGrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))

# Returns nGrams from a corpus of tokens
def listGrams(input_list, n):
    output =[]
    for idx in range(len(input_list)):
        temp = nGrams(input_list[idx], n)
        output = output + temp
    return output

#%%
tokens = tokenList(comments)

#%%
from gensim import corpora, models

dictionary = corpora.Dictionary(tokens)

#%%
print(dictionary)

#%%
# CHECKING IF IT IS POSSIBLE TO SORT THE DICTIONARY BEFORE THE NEXT STEPS
test = []

for i in range(len(dictionary)):
    test.append(dictionary[i])

test.sort()
testDict = corpora.Dictionary(test)

#%%
# ALTERNATE APPROACH
import operator
sortedDictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
dictionary2 = dict(sortedDictionary)

#%%
corpus = [dictionary.doc2bow(text) for text in tokens]

#%%
# Long computation time!!!
ldamodel = models.ldamodel.LdaModel(corpus, num_topics = 5, id2word = dictionary, passes = 20)

#%%
#ldamodel1 = models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=1)


#%%
# Top 3 words associated with the 3 topics we clustered the data into
print(ldamodel.print_topics(num_topics=5, num_words=3))

#%%

















