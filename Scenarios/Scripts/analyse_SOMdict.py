# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:46:24 2019

@author: tqc268
"""
import numpy as np
import pandas as pd
from Get_allSOC import get_allSOM
from split_nameDir import split_unique_name
import matplotlib.pyplot as plt

path = r'../RunK1-9'
dSOMperkey = get_allSOM(path)

dictKonv = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['ManureMass'] == 170}
dictOrg = {key:value for key, value in dSOMperkey.items() if split_unique_name(key)['IsConventional'] == "False"}

dict1=dictKonv
rota= [split_unique_name(k)['Rotation'] for k,v in dict1.items() ]
rk = np.unique(np.array(rota))
rotations= rk.tolist()
manure = [split_unique_name(k)['ManureMass'] for k,v in dict1.items() ]
man = np.unique(np.array(manure))
ManureAmount =man.tolist()

# Effekt of rotations
SOMmeanperRot = pd.DataFrame()
for ro in rotations:    
    dict2 = {k:value for k, value in dict1.items() if split_unique_name(k)['Rotation']== ro}
    df =pd.DataFrame.from_dict(dict2, orient='index') 
    means = df.mean(axis = 0)
    SOMmeanperRot[ro] = means   
SOMmean =SOMmeanperRot.transpose()
SOMmean.columns = ['dSON']
dat = SOMmean.sort_values('dSON')

fig = plt.figure(figsize=(10, 5))
plt.bar(dat.index, dat['dSON'])
plt.ylabel('kg N/ha/yr')
plt.show()
plt.tight_layout()
#plt.title('Mean N pool change per crop rotation', position = (0.4, 0.9), fontweight = "bold", fontsize = 10)
#fig.savefig("Mean dSON K1-8_few.pdf", bbox_inches='tight')    


## Add afgkode to cmean dataframe
## extract norm dataframe yields with matching index/afgkode