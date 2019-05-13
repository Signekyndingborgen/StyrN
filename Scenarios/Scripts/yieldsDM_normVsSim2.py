# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:17:20 2019

@author: tqc268
"""

import sys
import pandas as pd
sys.path.append(r'../../../pydaisy')
from split_nameDir import split_unique_name
from Get_allyields import get_allYields
import numpy as np 
import operator 
from functools import reduce

rota = pd.DataFrame(pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Rotations'))
rota.index = rota['ID']
crops = pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Crops')
crops.index = crops['Crop']
norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['afgkode']

path = r'../Run'


allresults = get_allYields(path)
soil = 'JB6'
name_entries = split_unique_name(key)
for key, value in allresults.items():     
    sim_yieldmean ={}  
    if name_entries['Soiltype'][0:3]!=soil:
        allresult = allresults
        
for key, value in allresults.items():   
    for kl, vl in value.items():
        allresults[key][kl] = np.mean(vl) ## mean value includes zero and it should not
df =pd.DataFrame.from_dict(d,orient='index')  
df['clovergrass']=df['Ryegrass']+df['Wclover']

norm170 = [v for k, v in allresults.items() if split_unique_name(k)['ManureMass']==170 and split_unique_name(k)['Soiltype'][0:3]==soil]


cropkeys=[]
for key, value in allresults.items():   
    for kl, vl in value.items():
        cropkeys[key][value] = kl

for key, value in allresults.items():   
    for kl, vl in value.items():
        if kl == 'Potato; Sava_Figaro':
            value['Potato'] = value.pop(kl)


evalu = {}

        
        evalu[key][]= np.mean(vl)
cmean = [x for x in d if x != 0]


ean= round(np.mean([d[k] for d in result if k in d]), 2)
    cropmean.append([k, mean])
name_entries = split_unique_name(key) 
norm170 = [v for k, v in allresults.items() if split_unique_name(k)['ManureMass']==170 and split_unique_name(k)['Soiltype'][0:3]==soil]

crop = 'Ryegrass'

np.mean([v[crop] for v in norm170])


for key, value in allresults.items():    

    
    sim_yieldmean ={}
    
    if name_entries['ManureMass']==170 and name_entries['Soiltype'][0:3]==soil:
        cropnames = allresults.get(key).keys()
        for cropname in cropnames:
            mean= np.mean(allresults.get(key).get(cropname))
            sim_yieldmean.append(key: [cropname, mean])
     
    yield_norm = round(norm['yield_' + soil][crop_ID]*norm['yieldfaktorDM'][crop_ID], 2)
    daisyname = crops['Daisynavn1'][cropname].split(',')
    print(key)
    for daisyname in daisynames:
        simyieldmean = np.mean(value[daisyname.strip()][str(actualyear)][0])
        sim_yields.append([cropname, simyieldmean, yield_norm])
    print(cropname)
evalu[key]=sim_yields 
dict2 = {}
for key in allresults:
    dict2[key] = sum(allresults[key])

"""
        for daisyname in daisynames:
            if crops['Daisynavn1'][cropname]=='Wclover, Ryegrass':
                simyieldmean = np.mean(value['Wclover'][str(actualyear)][0] + value['Ryegrass'][str(actualyear)][0])
                sim_yields.append([cropname, simyieldmean, yield_norm])
            else:
                simyieldmean = np.mean(value[daisyname.strip()][str(actualyear)][0])
                sim_yields.append([cropname, simyieldmean, yield_norm])

                    
                    #if str(1990+year) in value[daisyname.strip()]:
                #evalu[daisyname] = sim_yields
                    #print(sim_yields)
                    #print([daisyname, np.mean(sim_yields[:1])*10])
                    #evalu[daisyname] = [int(sim_yield), int(yield_norm)]
                
 """                   