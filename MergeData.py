# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 13:05:43 2018

@author: Sebastien
"""

#%%
import pandas as pd

#%%
data0 = pd.read_csv('AmazonSamsungS8.csv', index_col = 0)
data1 = pd.read_csv('AmazoniPhone8.csv', index_col = 0)
data2 = pd.read_csv('AmazoniPhoneX.csv', index_col = 0)
data3 = pd.read_csv('GoogleSamsungS8.csv', index_col = 0)
data4 = pd.read_csv('GoogleiPhone8.csv', index_col = 0)
data5 = pd.read_csv('GoogleiPhoneX.csv', index_col = 0)
data6 = pd.read_csv('influenster_iphoneX.csv')

#%%
# Unifying format to merge meta data
data0 = pd.DataFrame(data0[['comments', 'stars']])
data0['source'] = 'Amazon'
data0['product'] = 'Samsung S8'
data0 = data0[['source', 'product', 'comments', 'stars']]

data1 = pd.DataFrame(data1[['comments', 'stars']])
data1['source'] = 'Amazon'
data1['product'] = 'iPhone 8'
data1 = data1[['source', 'product', 'comments', 'stars']]

data2 = pd.DataFrame(data2[['comments', 'stars']])
data2['source'] = 'Amazon'
data2['product'] = 'iPhone X'
data2 = data1[['source', 'product', 'comments', 'stars']]

data3 = pd.DataFrame(data3[['comments', 'stars']])
data3['source'] = 'Google Shopping'
data3['product'] = 'Samsung S8'
data3 = data3[['source', 'product', 'comments', 'stars']]

data4 = pd.DataFrame(data4[['comments', 'stars']])
data4['source'] = 'Google Shopping'
data4['product'] = 'iPhone 8'
data4 = data4[['source', 'product', 'comments', 'stars']]

data5 = pd.DataFrame(data5[['comments', 'stars']])
data5['source'] = 'Google Shopping'
data5['product'] = 'iPhone X'
data5 = data5[['source', 'product', 'comments', 'stars']]

data6 = pd.DataFrame(data6[['CommentBox_Content', 'CommentBox_Rating']])
data6.columns = ['comments', 'stars']
data6['source'] = 'Influenster'
data6['product'] = 'iPhone X'
data6 = data6[['source', 'product', 'comments', 'stars']]

#%%
group2 = pd.concat([data0['comments'], data1['comments'], data2['comments'], data3['comments'], data4['comments'], data5['comments'], data6['comments']], ignore_index = True)
group2Meta = pd.concat([data0, data1, data2, data3, data4, data5, data6])

#%%
group2.to_csv('group2.csv')
group2Meta.to_csv('group2Meta.csv')

#%%

