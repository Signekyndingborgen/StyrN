# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:46:24 2019

@author: tqc268
"""
import pandas as pd
from Yields import meanyields
from Get_allyields import get_allYields
from split_nameDir import split_unique_name
from Yields import meanyields

path = r'../RunK89'
allresults = get_allYields(path)
meanperkey = meanyields(allresults)

for key, value in meanperkey.items():   
    for kl, vl in value.items():
        if kl == 'Potato; Sava_Figaro':
            value['Potato SavaFigaro'] = value.pop(kl)

dictK = {key:value for key, value in meanperkey.items() if split_unique_name(key)['IsConventional']!= 'False'}
dictO = {key:value for key, value in meanperkey.items() if split_unique_name(key)['IsConventional']== 'False'}

soil = ['JB1', 'JB4', 'JB6']
cmean = pd.DataFrame()
for s in soil:    
    dict2 = {k:value for k, value in dictK.items() if split_unique_name(k)['ManureMass']==170 and split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict2, orient='index') 
    #df['clovergrass']=df['Ryegrass']+df['Wclover']
    means = df.mean(axis = 0)
    cmean[s] = means

# Calculate the mean yield of Rygrass in rotations KK8 and KK9 (only ones with only grass - no clover)
cmeanRG_V = pd.DataFrame()
for s in soil:    
    dict3 = {k:value for k, value in dictK.items() if split_unique_name(k)['Rotation']=='KK9' and split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict3, orient='index') 
    means = df.mean(axis = 0)
    cmeanRG_V[s] = means
cmeanRG_V.index = ['Ryegrass_V']

cmeanRG_P = pd.DataFrame()
for s in soil:    
    dict3 = {k:value for k, value in dictK.items() if split_unique_name(k)['Rotation']=='KK8' and split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict3, orient='index') 
    means = df.mean(axis = 0)
    cmeanRG_P[s] = means
cmeanRG_P.index = ['Ryegrass_P']
# add the Ryegrass mean of rotations KK8 and KK9 to the rest of the crops
cmean = cmean.append(cmeanRG_V) 
cmean = cmean.append(cmeanRG_P)

norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['Daisynavn1']
norm['yield_JB1tDM']= norm['yieldfaktorDM']*norm['yield_JB1']
norm['yield_JB4tDM']= norm['yieldfaktorDM']*norm['yield_JB4']
norm['yield_JB6tDM']= norm['yieldfaktorDM']*norm['yield_JB6']
cmean= cmean.join(norm[norm.columns[-3:]])

cmean['JB1_%fejl'] = round((cmean['JB1']-cmean['yield_JB1tDM'])/cmean['yield_JB1tDM']*100, 1)
cmean['JB4_%fejl'] = round((cmean['JB4']-cmean['yield_JB4tDM'])/cmean['yield_JB4tDM']*100, 1)
cmean['JB6_%fejl'] = round((cmean['JB6']-cmean['yield_JB6tDM'])/cmean['yield_JB6tDM']*100, 1)

cmean.to_excel("../Plots/cmeanK_P4.xlsx")

import matplotlib.pyplot as plt

fig = plt.figure()
#ax=plt.subplot(3,1, 1)
plt.scatter(cmean['yield_JB1tDM'], cmean['JB1'], marker='x', c='black', s=15)
plt.scatter(cmean['yield_JB4tDM'], cmean['JB4'], marker='x', c='black', s=15)
plt.scatter(cmean['yield_JB6tDM'], cmean['JB6'], marker='x', c='black', s=15)
plt.title('Yields t DM/ha' , position = (0.6, 0.9), fontweight="bold", fontsize=8)
plt.legend(cmean.index)
ax.set(ylabel=('simulated (t DM/ha)'), xlabel= 'yieldnorm')
ax.set(xlim=(0,6), ylim=(0,6))
ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')


"""
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(cmean, marker = 'o')
plt.xlabel(cmean.index[:], rotation =  'vertical')   



## Add afgkode to cmean dataframe
## extract norm dataframe yields with matching index/afgkode

"""