# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:10:22 2019

@author: tqc268
"""

norm170 = [v for k, v in allresults.items() if split_unique_name(k)['ManureMass']==170 and split_unique_name(k)['Soiltype'][0:3]==soil]

#result = []
#for item in norm170:
#    for k,v in item.items():
#        average = round(v[v!=0].mean(), 2)
#        result.append({k:average})

all_keys = reduce(operator.or_, (allresults.keys() for d in allresults))

np.mean(allresults.get(key).get('Silomajs'))

cropmean = []
for k in all_keys:
    mean= round(np.mean([d[k] for d in result if k in d]), 2)
    cropmean.append([k, mean])
cmean=pd.DataFrame(cropmean)
cmean.columns = ['daisynavn', 'yield_tDM'] 
cmean.index=cmean['daisynavn']
cmean.loc[0]=['Clovergrass', cmean['yield_tDM']['Wclover']+cmean['yield_tDM']['Ryegrass']]
cmean.index=cmean['daisynavn']

cmean['cropname'] = crops['Crop'][cmean['daisynavn']]

crop_ID = int(crops['afgkode1'][cropname])
yield_norm = round(norm['yield_' + soil][crop_ID]*norm['yieldfaktorDM'][crop_ID], 2)

print({k:np.mean(v) for k,v in allresults.items()})
print({k:sum(map(int, v)) for k, v in allresults.items()})
###########################################################################