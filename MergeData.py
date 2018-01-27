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

#%%
group2 = pd.concat([data0['comments'], data1['comments'], data2['comments'], data3['comments'], data4['comments'], data5['comments'], data6['CommentBox_Content']], ignore_index = True)

#%%
group2.to_csv('group2.csv')

#%%

#%%