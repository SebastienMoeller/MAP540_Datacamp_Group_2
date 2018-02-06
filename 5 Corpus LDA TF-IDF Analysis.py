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
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
#%%
# Encoding options: IBM437, ISO-8859-1, ibm1125
data = pd.read_csv('Reviews.csv', encoding = 'ISO-8859-1')
del data['Unnamed: 0']
#%%
commentsiX = data[data['product'] == 'iPhone X']
commentsi8 = data[data['product'] == 'iPhone 8']
commentsS8 = data[data['product'] == 'Samsung S8']

commentsiX = commentsiX['comments']
commentsi8 = commentsi8['comments']
commentsS8 = commentsS8['comments']

#maybe get ride of short comments (not very explicative...)?
count = data.comments.apply(lambda x: len(str(x).split(' ')))
short_reviews = data[count <6]
short_comments = short_reviews.comments
avg_star = short_reviews.stars.mean()

#%% KIM's DATA SET

#data = pd.read_csv('data_scraping_V2.csv', encoding = 'ISO-8859-1')
# Reddit comments contain mostly useless comments
#data = data[data['source'] != 'reddit']
# Youtube comments contain mostly useless comments
#data = data[data['source'] != 'youtube']
# Most twitter comments are broken
#data = data[data['source'] != 'twitter']

#comments = data['text'].tolist()

#%%
# For testing I reduce the data set
#comments = comments[100:1100]

#%%
# Given a list of tokens passed through nltk.pos_tag(tokens), this returns the
# pos argument needed for the lemmitization in a new list of pairs: (word, type)
def get_wordnet_pos(tokensTag):
    # tokensTag is a list of pairs of tuples and cannot be modified
    tokenNew = []  
    for i in range(len(tokensTag)):
        # Save the current word being identified
        tokenNew.append([tokensTag[i][0]])
        # Append the type
        if tokensTag[i][1][0] == 'J':
            tokenNew[i].append(wordnet.ADJ)
            
        elif tokensTag[i][1][0] == 'V':
            tokenNew[i].append(wordnet.VERB)
            
        elif tokensTag[i][1][0] == 'N':
            tokenNew[i].append(wordnet.NOUN)
            
        elif tokensTag[i][1][0] == 'R':
            tokenNew[i].append(wordnet.ADV)
        
        elif tokensTag[i][1][0] == '?':
            tokenNew[i].append(wordnet.ADJ_SAT)
        else:
            tokenNew[i].append(wordnet.ADJ)
            
    return tokenNew

# Smart lemmitization !
def lemmatize(words):
        
    wordType = get_wordnet_pos(pos_tag(words))
    wordnet_lemmatizer = WordNetLemmatizer()    
    for i in range(len(wordType)):
        words[i] = wordnet_lemmatizer.lemmatize(wordType[i][0], pos = wordType[i][1])
    
    return words 

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
            ' x ', ' ').replace('’', '').replace("'", '').replace('http', '').replace('https', '').replace('com', ' ').replace('co', ' ').replace(
                    '201', ' ').replace('0', ' ').replace('â\x80\x99', '').replace('í¢ä\x89åä\x8b¢', '').replace('phone', ' ') for item in comments]
    
    # nltk's tokenizer
    tkzer = TweetTokenizer(preserve_case = False, strip_handles = True, reduce_len = True)
    tokens = [tkzer.tokenize(item) for item in comments]
    
    tokens = []
    #wordnet_lemmatizer = WordNetLemmatizer()
    for idx in range(len(comments)):
        # Remove engish stopwords
        words = ([word for word in comments[idx].split() if word not in stopwords.words('english')])
        
        words = lemmatize(words)
        #for idy in range(len(words)):
            # Lemmatize each word
            
            #words[idy] = wordnet_lemmatizer.lemmatize(words[idy], pos = 'v')
        
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





#%%
#tokens = tokenList(comments)
tokensiX = tokenList(commentsiX)
tokensi8 = tokenList(commentsi8)
tokensS8 = tokenList(commentsS8)

#%% TF - IDF Matrix Construction
# All lemmitized tokens joined by comment
lemmiX = []
lemmi8 = []
lemmS8 = []

for idx in range(len(tokensiX)):
    lemmiX.append(' '.join(tokensiX[idx]))

for idx in range(len(tokensi8)):
    lemmi8.append(' '.join(tokensi8[idx]))

for idx in range(len(tokensS8)):
    lemmS8.append(' '.join(tokensS8[idx]))

#%%
#nmf for iphone X
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
termdoc = tfidf_vectorizer.fit_transform(lemmiX)
TFM = pd.DataFrame(termdoc.todense()).replace(0, '')
#%%
n_dimensions = 40 # This can also be interpreted as topics in this case. This is the "beauty" of NMF. 10 is arbitrary
model = NMF(n_components=40, init='random')
W = model.fit_transform(termdoc) 
H = model.components_ 
#%%
W = pd.DataFrame(W).replace(0, '')
H = pd.DataFrame(H).replace(0, '')
#%%
# Since NMF dimensions can be interpreted as topics, let's look at the dimensions
words = tfidf_vectorizer.get_feature_names()
n_top_words = 20 # print 10 words by dimension. You can change this number

# Loop for each dimension: what words are the most dominant in each dimension
for i_dimension, dimension in enumerate(model.components_):
    print("Topic #%d:" % i_dimension)
    print(" ".join([words[i] for i in dimension.argsort()[:-n_top_words - 1:-1]]))
print()

# Can you interpret these dimensions as humanly intelligible topics?

#%%
#nmf for iphone 8
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
termdoc = tfidf_vectorizer.fit_transform(lemmi8)
TFM = pd.DataFrame(termdoc.todense()).replace(0, '')
n_dimensions = 40 # This can also be interpreted as topics in this case. This is the "beauty" of NMF. 10 is arbitrary
model = NMF(n_components=40, init='random')
W = model.fit_transform(termdoc) 
H = model.components_ 
W = pd.DataFrame(W).replace(0, '')
H = pd.DataFrame(H).replace(0, '')
words = tfidf_vectorizer.get_feature_names()
n_top_words = 20 # print 10 words by dimension. You can change this number

# Loop for each dimension: what words are the most dominant in each dimension
for i_dimension, dimension in enumerate(model.components_):
    print("Topic #%d:" % i_dimension)
    print(" ".join([words[i] for i in dimension.argsort()[:-n_top_words - 1:-1]]))
print()
#%%
#nmf for Samsung S8
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
termdoc = tfidf_vectorizer.fit_transform(lemmS8)
TFM = pd.DataFrame(termdoc.todense()).replace(0, '')
n_dimensions = 40 # This can also be interpreted as topics in this case. This is the "beauty" of NMF. 10 is arbitrary
model = NMF(n_components=40, init='random')
W = model.fit_transform(termdoc) 
H = model.components_ 
W = pd.DataFrame(W).replace(0, '')
H = pd.DataFrame(H).replace(0, '')
words = tfidf_vectorizer.get_feature_names()
n_top_words = 20 # print 10 words by dimension. You can change this number

# Loop for each dimension: what words are the most dominant in each dimension
for i_dimension, dimension in enumerate(model.components_):
    print("Topic #%d:" % i_dimension)
    print(" ".join([words[i] for i in dimension.argsort()[:-n_top_words - 1:-1]]))
print()
#%% LDA ANALYSIS
from gensim import corpora, models

#dictionary = corpora.Dictionary(tokens)
dictionaryiX = corpora.Dictionary(tokensiX)
dictionaryi8 = corpora.Dictionary(tokensi8)
dictionaryS8 = corpora.Dictionary(tokensS8)
#print(dictionary)

#%%
#corpus = [dictionary.doc2bow(text) for text in tokens]
corpusiX = [dictionaryiX.doc2bow(text) for text in tokensiX]
corpusi8 = [dictionaryi8.doc2bow(text) for text in tokensi8]
corpusS8 = [dictionaryS8.doc2bow(text) for text in tokensS8]

#%%
# Long computation time!!!
#ldamodel = models.ldamodel.LdaModel(corpus, num_topics = 40, id2word = dictionary, passes = 10)
ldaiX = models.ldamodel.LdaModel(corpusiX, num_topics = 40, id2word = dictionaryiX, passes = 10)

#%%
ldai8 = models.ldamodel.LdaModel(corpusi8, num_topics = 40, id2word = dictionaryi8, passes = 10)

#%%
ldaS8 = models.ldamodel.LdaModel(corpusS8, num_topics = 40, id2word = dictionaryS8, passes = 10)

#%%
# Top 10 words associated with the 40 topics we clustered the data into
#print(ldamodel.print_topics(num_topics = 40, num_words = 10))
print(ldaiX.print_topics(num_topics = 40, num_words = 10))

#%%
print(ldai8.print_topics(num_topics = 40, num_words = 10))

#%%
print(ldaS8.print_topics(num_topics = 40, num_words = 10))

#%%





#%% TESTING ALTERNATE METHOD
tokenSorted = []
for i in range(len(tokens)):
    tokenSorted = tokenSorted + tokens[i]

tokenSorted = ' '.join(tokenSorted)



#%%
print(ldamodel.get_document_topics(tokens))

#%%
ldamodel.get


#%%
#GRAPH THEORY
import networkx as nx
import string
from sys import maxint
#%%
def bigrams(line):
    tokens = line.split(" ")
    return [(tokens[i], tokens[i+1]) for i in range(0, len(tokens)-1)]
#%%
flat_tokensS8 = [item for sublist in tokensS8 for item in sublist]
G=nx.Graph()
#VERTICES
for num in range(92638):
    G.add_node(flat_tokensS8[num])
G.nodes()

#%%
#iterate over all elements of bigrams
    #G.add_edge(first element bigram, second element bigram)

bigrams = listGrams(tokensS8,2)

for pair in range(89180):
    G.add_edge(bigrams[pair][0],bigrams[pair][1])

#%%
print(len(G.edges()))
#%%
nx.draw(G)
plt.savefig("simple_path.png") # save as png
plt.show() # display
