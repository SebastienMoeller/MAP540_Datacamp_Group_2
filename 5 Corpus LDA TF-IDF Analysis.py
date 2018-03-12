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
commentsiX = commentsiX['comments']

#%%
commentsi8 = data[data['product'] == 'iPhone 8']
commentsi8 = commentsi8['comments']

#%%
commentsS8 = data[data['product'] == 'Samsung S8']
commentsS8 = commentsS8['comments']

#%%
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

#%%
tokensi8 = tokenList(commentsi8)

#%%
tokensS8 = tokenList(commentsS8)

#%%





#%% TF - IDF Matrix Construction
# All lemmitized tokens joined by comment
lemmiX = []
for idx in range(len(tokensiX)):
    lemmiX.append(' '.join(tokensiX[idx]))
#%%
lemmi8 = []
for idx in range(len(tokensi8)):
    lemmi8.append(' '.join(tokensi8[idx]))

#%%
lemmS8 = []
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

#%%
#dictionary = corpora.Dictionary(tokens)

#%%
dictionaryiX = corpora.Dictionary(tokensiX)

#%%
dictionaryi8 = corpora.Dictionary(tokensi8)

#%%
dictionaryS8 = corpora.Dictionary(tokensS8)
#print(dictionary)

#%%
#corpus = [dictionary.doc2bow(text) for text in tokens]
corpusiX = [dictionaryiX.doc2bow(text) for text in tokensiX]

#%%
corpusi8 = [dictionaryi8.doc2bow(text) for text in tokensi8]

#%%
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





#%% KATIE
import pyLDAvis.gensim
pyLDAvis.enable_notebook()

#%%
pyLDAvis.gensim.prepare(ldaiX, corpusiX, dictionaryiX)

#%%
pyLDAvis.display(ldaViz)
#%%
#GRAPH THEORY
import networkx as nx

#%%

#%%

#%%
    




#%%
# FILTER TOKENS TO ONLY CONTAIN NOUNS
def nounsOnly(tokenList):
    newTokens = []
    for i in range(len(tokenList)):
        tags = pos_tag(tokenList[i])
        nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        newTokens.append(nouns)
    print(newTokens)
    return newTokens 
#%%
newTokensS8 = nounsOnly(tokensS8)

#%%
newTokensiX = nounsOnly(tokensiX)
newTokensi8 = nounsOnly(tokensi8)

#%%





#%% Replace synonyms of problem with problem
def problemSync(tokenList):
    newTokens = []
    for i in range(len(tokenList)):
        words = [w.replace('issue', 'problem').replace('default', 'problem').replace('fault', 'problem').replace(
                'trouble', 'problem').replace('broken', 'problem').replace('defect', 'problem').replace(
                        'fault', 'problem').replace('malfunction', 'problem').replace('flaw', 'problem').replace(
                                'setback', 'problem') for w in tokenList[i]]
        newTokens.append(words)
    print(newTokens)
    return newTokens
#%%
problemTokensS8 = problemSync(newTokensS8)




#%% BIGRAMS
from collections import Counter
import matplotlib
from community import community_louvain
#%%
#iterate over all elements of bigrams
#G.add_edge(first element bigram, second element bigram)

bigrams = listGrams(problemTokensS8 ,2)
#%%
countb = Counter(bigrams)
#%%
mostb = countb.most_common(len(countb))
mostb
#%% DEFINING GRAPH USING BIGRAMS
baseGraph = nx.Graph()
for pair in range(len(mostb)):
    baseGraph.add_edge(mostb[pair][0][0],mostb[pair][0][1], weight =mostb[pair][1])  #add weight argument: weight = 

#%%












    
    
#%%
def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos

def _position_communities(g, partition, **kwargs):

    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos

def _find_between_community_edges(g, partition):

    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges
#%%
def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos
#%%
    




#%%




#%% MAKING GRAPHS: EGO GRAPH OF 'PROBLEM'
matplotlib.rcParams['figure.figsize'] = (40, 20)
G = nx.ego_graph(baseGraph, radius = 1, center = True, n = 'problem')
partition = community_louvain.best_partition(G)
pos = community_layout(g=G, partition=partition)
nx.draw(G, pos, node_color=list(partition.values()), 
        labels=dict((n,n) for n,d in G.nodes(data=True)), font_color='black', font_size=8, font_family='monospace', weight = 'bold',
       edge_color='lightgrey')

#%%





#%% ALTERNATE GRAPH METHOD
import matplotlib.pyplot as plt
#%%
nx.draw(G)
plt.show() # display
#%%
#trying with Girvan-Newman
import itertools
comp = nx.algorithms.community.centrality.girvan_newman(G)
k = 5
for i in itertools.islice(comp, k):
    cluster = tuple(sorted(c) for c in communities)

#%% 









































