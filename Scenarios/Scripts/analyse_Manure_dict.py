# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:56:08 2019

@author: tqc268
"""
# Analyse results based on manure input
import numpy as np
import pandas as pd
from Get_allSOC import get_allSOM
from split_nameDir import split_unique_name
import matplotlib.pyplot as plt

path = r'../Run4'
#dSOMperkey = get_allSOM(path)

dictKonv = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "True"}
#dictOrg = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "False"}

rota= [split_unique_name(k)['Rotation'] for k,v in dSOMperkey.items() ]
rotaK= [split_unique_name(k)['Rotation'] for k,v in dictKonv.items() ]
rk = np.unique(np.array(rotaK))
rotations= rk.tolist()

manure = [split_unique_name(k)['ManureMass'] for k,v in dSOMperkey.items() ]
manureK = [split_unique_name(k)['ManureMass'] for k,v in dictKonv.items() ]
man = np.unique(np.array(manureK))
ManureAmount =man.tolist()


d= pd.DataFrame(index=rotations, columns=ManureAmount)
for ma in ManureAmount:
    dict1 = {k:value for k, value in dictKonv.items() if split_unique_name(k)['ManureMass']== ma}
    for ro in rotations:    
        dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
        if len(dict2)>0:
            df = pd.DataFrame.from_dict(dict2, orient='index') 
            means = df.mean(axis = 0)
            d[ma][ro] = means[0]

d.plot(kind = 'bar', legend = True, title = 'Puljeændring fordelt på husdyrgødningsniveau per sædskifte')


dt=d.transpose()

dt.plot.line(style = '.-', legend = True) 
plt.legend(bbox_to_anchor=(1.04,0.5), loc="center left")