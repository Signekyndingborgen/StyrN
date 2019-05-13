# -*- coding: utf-8 -*-
"""
Created on Wed May  1 12:42:50 2019

@author: tqc268
"""

from Yields import meanyields
from Get_allyields import get_allYields
from split_nameDir import split_unique_name
from Yields import meanyields
path = r'../RunTest'
allresults = get_allYields(path)
meanperkey = meanyields(allresults)

dictK = {key:value for key, value in meanperkey.items() if split_unique_name(key)['IsConventional']!= 'False'}
dictO = {key:value for key, value in meanperkey.items() if split_unique_name(key)['IsConventional']== 'False'}

soil = ['JB1', 'JB4', 'JB6']
cmean = pd.DataFrame()
for s in soil:    
    dict2 = {k:value for k, value in dictK.items() if split_unique_name(k)['ManureMass']==170 and split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict2, orient='index') 
    df['clovergrass']=df['Ryegrass']+df['Wclover']
    means = df.mean(axis = 0)
    cmean[s] = means

# Ryegrass 10 t D
# Graes 6.6 ny 4.0