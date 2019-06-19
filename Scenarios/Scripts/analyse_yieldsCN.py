# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:46:24 2019

@author: tqc268
"""
import matplotlib.pyplot as plt
import pandas as pd
from Yields import meanyields
from split_nameDir import split_unique_name
from Yields import meanyields
from Get_allyieldsN import get_allYieldsN
from Get_allyieldsC import get_allYields


path = r'../RunK1-9'

allresults = get_allYields(path)
meanperkey = meanyields(allresults)

#dictK = {key:value for key, value in meanperkey.items() if split_unique_name(key)['IsConventional']!= 'False'}

soil = ['JB1', 'JB4', 'JB6']
cmean = pd.DataFrame()
for s in soil:    
    dict2 = {k:value for k, value in meanperkey.items() if split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict2, orient='index') 
    df['clovergrass']=df['Ryegrass']+df['Wclover']
    means = df.mean(axis = 0)
    cmean[s] = means

norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['Daisynavn1']
norm['yield_JB1tDM']= norm['yieldfaktorDM']*norm['yield_JB1']
norm['yield_JB4tDM']= norm['yieldfaktorDM']*norm['yield_JB4']
norm['yield_JB6tDM']= norm['yieldfaktorDM']*norm['yield_JB6']
cmean= cmean.join(norm[norm.columns[-3:]])

cmean['JB1_%fejl'] = round((cmean['JB1']-cmean['yield_JB1tDM'])/cmean['yield_JB1tDM']*100, 1)
cmean['JB4_%fejl'] = round((cmean['JB4']-cmean['yield_JB4tDM'])/cmean['yield_JB4tDM']*100, 1)
cmean['JB6_%fejl'] = round((cmean['JB6']-cmean['yield_JB6tDM'])/cmean['yield_JB6tDM']*100, 1)
## Udbytte fej i %
cplot = cmean.iloc[:, -3:].dropna()
fig = plt.figure(figsize=(15, 8))
ax = plt.subplot(1, 2, 1)
cplot.plot(kind='bar', ax=ax, figsize=(10, 6)) 
ax.set(ylabel='DM yield error (%)')

allresults = get_allYieldsN(path)
meanperkey = meanyields(allresults)
cmean = pd.DataFrame()
for s in soil:    
    dict2 = {k:value for k, value in meanperkey.items() if split_unique_name(k)['Soiltype'][0:3]==s}
    df =pd.DataFrame.from_dict(dict2, orient='index') 
    df['clovergrass']=df['Ryegrass']+df['Wclover']
    means = df.mean(axis = 0)
    cmean[s] = means
    
norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['Daisynavn1']
norm['yield_JB1tN']= norm['yieldfaktorN']*norm['yield_JB1']
norm['yield_JB4tN']= norm['yieldfaktorN']*norm['yield_JB4']
norm['yield_JB6tN']= norm['yieldfaktorN']*norm['yield_JB6']
cmean= cmean.join(norm[norm.columns[-3:]])

cmean['JB1_%fejl'] = round((cmean['JB1']-cmean['yield_JB1tN'])/cmean['yield_JB1tN']*100, 1)
cmean['JB4_%fejl'] = round((cmean['JB4']-cmean['yield_JB4tN'])/cmean['yield_JB4tN']*100, 1)
cmean['JB6_%fejl'] = round((cmean['JB6']-cmean['yield_JB6tN'])/cmean['yield_JB6tN']*100, 1)

## Udbytte fej i %
cplot = cmean.iloc[:, -3:].dropna()

#ax2 = plt.subplot(222)
#cplot.plot.bar(x='B', y='counts', ax=ax2, figsize=(5, 4), title='Poisson Plot')

ax = plt.subplot(1, 2, 2)
cplot.plot(kind = 'bar', ax=ax, legend = True, title = 'RunK1-9')
ax.set(ylabel='N yield error (%)')
plt.tight_layout()

#fig.savefig("Yield error RunK2-8_few.pdf", bbox_inches='tight') 
#cmean.to_excel("../Plots/cmeanK.xlsx")
