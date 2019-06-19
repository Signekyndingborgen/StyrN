# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:05:31 2019

@author: tqc268
"""
import numpy as np
import pandas as pd
from Get_allSOC import get_allSOM
from split_nameDir import split_unique_name
import matplotlib.pyplot as plt

path = r'../RunK_170'
dSOMperkey = get_allSOM(path)

#dictKonv = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "True"}
#dictOrg = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "False"}

rota= [split_unique_name(k)['Rotation'] for k,v in dSOMperkey.items() ]
rk = np.unique(np.array(rota))
rotations= rk.tolist()


## Effekt of initalization level within rotations   
initlevel = ['High', 'Medium', 'Low']

meanILRO= pd.DataFrame(index=rotations, columns=initlevel)
for il in initlevel:
    dict1 = {k:value for k, value in dSOMperkey.items() if split_unique_name(k)['Initlevel']== il}
    for ro in rotations:    
        dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
        if len(dict2)>0:
            df = pd.DataFrame.from_dict(dict2, orient='index') 
            means = df.mean(axis = 0)
            meanILRO[il][ro] = means[0]

ax = meanILRO.plot(kind = 'bar', legend = True, title = 'Annual change in SON')
ax.set(ylabel = 'kg N/ha/yr')
plt.tight_layout()