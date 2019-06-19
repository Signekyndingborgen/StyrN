# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:46:24 2019

@author: tqc268
"""
import pandas as pd
from Yields import meanyields
from Get_allyieldsCN import get_allYieldsCN
from split_nameDir import split_unique_name
from Yields import meanyields

path = r'../RunK2-7'
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
    dict2 = {k:value for k, value in dictK.items() if split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict2, orient='index') 
    df['clovergrass']=df['Ryegrass']+df['Wclover']
    means = df.mean(axis = 0)
    cmean[s] = means

"""
# Calculate the mean yield of Rygrass in rotations KK8 and KK9 (only ones with only grass - no clover)
cmeanG_V = pd.DataFrame()
for s in soil:    
    dict3 = {k:value for k, value in dictK.items() if split_unique_name(k)['Rotation']=='KK9' and split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict3, orient='index') 
    means = df.mean(axis = 0)
    cmeanG_V[s] = means
cmeanG_V.index = ['Graes']

cmeanCG_P = pd.DataFrame()
for s in soil:    
    dict3 = {k:value for k, value in dictK.items() if split_unique_name(k)['Rotation']=='K8' and split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict3, orient='index') 
    df['clovergrass_P']=df['Ryegrass']+df['Wclover']
    means = df.mean(axis = 0)
    cmeanCG_P[s] = means
cmeanCG_P.index = ['clovergrass_P']
# add the Ryegrass mean of rotations KK8 and KK9 to the rest of the crops

cmean = cmean.append(cmeanCG_P['clovergrass_P'])

cmean = cmean.append(cmeanG_V) 
"""

norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['Daisynavn1']
norm['yield_JB1tN']= norm['yieldfaktorN']*norm['yield_JB1']
norm['yield_JB4tN']= norm['yieldfaktorN']*norm['yield_JB4']
norm['yield_JB6tN']= norm['yieldfaktorN']*norm['yield_JB6']
cmean= cmean.join(norm[norm.columns[-3:]])

cmean['JB1_%fejl'] = round((cmean['JB1']-cmean['yield_JB1tN'])/cmean['yield_JB1tN']*100, 1)
cmean['JB4_%fejl'] = round((cmean['JB4']-cmean['yield_JB4tN'])/cmean['yield_JB4tN']*100, 1)
cmean['JB6_%fejl'] = round((cmean['JB6']-cmean['yield_JB6tN'])/cmean['yield_JB6tN']*100, 1)

#cmean.to_excel("../Plots/cmeanKK9.xlsx")

import matplotlib.pyplot as plt
## Udbytte fej i %
cplot = cmean.iloc[:, -3:].dropna()
ax = cplot.plot(kind = 'bar', legend = True)
ax.set(ylabel='Udbytttefejl på kvælstof ( %)')
plt.tight_layout()




"""
#plt.bar(cplot.index, cplot)

#plt.title(d+'-DM', position = (0.6, 0.9), fontweight="bold", fontsize=8)
#ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
#ax.figure.autofmt_xdate()
#ax.xaxis.set_major_locator()
#ax.xaxis.set_major_formatter()
fig.savefig("KG_DM_v.2.1.pdf", bbox_inches='tight')      



plt.scatter(cmean['yield_JB4tDM'], cmean['JB4'], marker='x', c='black', s=15)
plt.scatter(cmean['yield_JB6tDM'], cmean['JB6'], marker='x', c='black', s=15)
plt.title('Yields t DM/ha' , position = (0.6, 0.9), fontweight="bold", fontsize=8)
ax.set(xlim=(0,6), ylim=(0,6))
ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')


import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(cmean, marker = 'o')
plt.xlabel(cmean.index[:], rotation =  'vertical')   



## Add afgkode to cmean dataframe
## extract norm dataframe yields with matching index/afgkode

"""