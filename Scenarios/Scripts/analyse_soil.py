# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:14:29 2019

@author: tqc268
"""

import numpy as np
import pandas as pd
from Get_allSOC import get_allSOM
from split_nameDir import split_unique_name
import matplotlib.pyplot as plt

path = r'../Run4'
#dSOMperkey = get_allSOM(path)

#dictKonv = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "True"}
#dictOrg = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "False"}

rota= [split_unique_name(k)['Rotation'] for k,v in dSOMperkey.items() ]
rk = np.unique(np.array(rota))
rotations= rk.tolist()


## Effekt of soil texture within rotations   
soiltype = ['JB1', 'JB4', 'JB6']

meanJBRO= pd.DataFrame(index=rotations, columns=soiltype)
for st in soiltype:
    dict1 = {k:value for k, value in dSOMperkey.items() if split_unique_name(k)['Soiltype'][0:3]== st}
    for ro in rotations:    
        dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
        if len(dict2)>0:
            df = pd.DataFrame.from_dict(dict2, orient='index') 
            means = df.mean(axis = 0)
            meanJBRO[st][ro] = means[0]

meanJBRO.plot(kind = 'bar', legend = True)


## Effekt of topsoil SOC within rotations   
soilC = ['high', 'med', 'low']

meanCRO= pd.DataFrame(index=rotations, columns=soilC)
for sc in soilC:
    dict1 = {k:value for k, value in dSOMperkey.items() if split_unique_name(k)['Soiltype'][3:]== sc}
    for ro in rotations:    
        dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
        if len(dict2)>0:
            df = pd.DataFrame.from_dict(dict2, orient='index') 
            means = df.mean(axis = 0)
            meanCRO[sc][ro] = means[0]

meanCRO.plot(kind = 'bar', legend = True, title= 'Mean dSON per topsoil C content level', ylabel = 'kg N / ha yr')