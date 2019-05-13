# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:34:14 2019

@author: tqc268
"""

import pandas as pd
import pickle
import numpy as np
# if potato has a funny name
for key, value in allresults.items():   
    for kl, vl in value.items():
        if kl == 'Potato; Sava_Figaro':
            value['Potato'] = value.pop(kl)
            
#data = pickle.load(open("dict.pkl","rb"))

data = allresults
# Assuming some precedence of attributes for your data here!
index = ['Rotation','ManureMass', 'IsConventional', 'SoilType','Weather','InitLevel','Crop','Yield']

# Creating an empty Pandas Dataframe with the columns from above
mDf = pd.DataFrame(columns=index) 
mDf.head()        

# Loading your dictionary to Pandas

df = pd.DataFrame.from_dict(data)
df
# Column names will be split and entered as new entries per row
colNames = list(df.columns)

# Crops are stored as row names in pandas
crops = list(df.index)

# Lot of things are going on here! 
# You can check out what's going on. 
# There are two list comprehensions: Inner one makes one row entry with your file name now appended with crop name and yield
# Outer one loops through each of the 162 entries

hierEntries = [np.asarray([(colNames[i]+'_'+crops[b]+'_'+repr(df.iloc[b,i])).split('_') for b in range(len(crops))]) for i in range(len(df.columns))]

# The previous step results in a 3D array; changing it to 2d arrays
hierEntries = (np.asarray(hierEntries)).reshape(-1,len(index))

# Make a Pandas dataframe out of these entries
hierEntries = pd.DataFrame(hierEntries,columns=index)

# Load it into the empty frame we made
mDf = mDf.append(hierEntries)        

# The coolest step is this one which just takes your frame from above and 
# makes a hierarchical array as shown below. 
# The keys to sort are all but the yield.
# This resembles the table you had printed!
hierDf = mDf.set_index(index[:-1])
dfH = hierDf.swaplevel('ManureMass', 'InitLevel')
# dfH = hierDf.reorder_levels(order =['Rotation','InitLevel', 'IsConventional', 'SoilType','Weather','ManureMass', 'Crop'] )
