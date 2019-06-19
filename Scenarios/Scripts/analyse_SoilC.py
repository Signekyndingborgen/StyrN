# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:02:36 2019

@author: tqc268
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:42:11 2019

@author: tqc268
"""

## Effekt of initalization level within rotations   

import numpy as np
import pandas as pd
from Get_allSOC import get_allSOM
from split_nameDir import split_unique_name
import matplotlib.pyplot as plt

#path = r'../RunKonv'
#dSOMperkey = get_allSOM(path)

rota= [split_unique_name(k)['Rotation'] for k,v in dSOMperkey.items() ]
rk = np.unique(np.array(rota))
rotations= rk.tolist()
manure = [split_unique_name(k)['ManureMass'] for k,v in dSOMperkey.items() ]
man = np.unique(np.array(manure))
ManureAmount =man.tolist()

dict170 = {k:value for k, value in dSOMperkey.items()  if split_unique_name(k)['ManureMass'] ==170}
    

soilC = ['low', 'med', 'high']
SOMmeandf = pd.DataFrame(index = rotations, columns = soilC)
for sc in soilC:
    dict1 = {k:value for k, value in dSOMperkey.items()  if split_unique_name(k)['Soiltype'][3:]== sc}
    meanRO = pd.DataFrame()
    for ro in rotations:    
        dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
        df = pd.DataFrame.from_dict(dict2, orient='index') 
        means = df.mean(axis = 0)
        meanRO[ro] = means
        SOMmeandf[sc][ro]= meanRO[ro][0]

ax = SOMmeandf.plot(kind = 'bar', legend = True, title='Annual N pool change')
ax.set(ylabel= 'kg N / ha / yr')
plt.tight_layout()

