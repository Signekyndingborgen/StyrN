# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:00:33 2019

@author: tqc268
"""
import numpy as np
import pandas as pd
from Get_allSOC import get_allSOM
from split_nameDir import split_unique_name
import matplotlib.pyplot as plt

path = r'../Run4'
dSOMperkey = get_allSOM(path)

#dictKonv = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "True"}
#dictOrg = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "False"}

rota= [split_unique_name(k)['Rotation'] for k,v in dSOMperkey.items() ]
rk = np.unique(np.array(rota))
rotations= rk.tolist()

manure = [split_unique_name(k)['ManureMass'] for k,v in dSOMperkey.items() ]
man = np.unique(np.array(manure))
ManureAmount =man.tolist()


# Effekt of weather within rotations
weather = ['East', 'West']
SOMmeanperRotWe = []
for we in weather:
    dict1 = {k:value for k, value in dSOMperkey.items() if split_unique_name(k)['Weather'][0:4]== we}
    meanRO = pd.DataFrame()
    for ro in rotations:    
        dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
        df = pd.DataFrame.from_dict(dict2, orient='index') 
        means = df.mean(axis = 0)
        meanRO[ro] = means
    SOMmean =meanRO.transpose()
    SOMmean.columns = ['N'+'_'+we]
    SOMmeanperRotWe.append(SOMmean)
dfSOM = SOMmeanperRotWe[0].join(SOMmeanperRotWe[1])



dfSOM.plot(kind = 'bar', legend = True)

# (ylabel ='kg N/ha/yr')
