# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 11:53:20 2018
## INCLUDE pct_clo from xl and plot it against simulated. Only for N. pct_clover is the same for DM and N.
@author: tqc268
"""
from sklearn.metrics import r2_score

import pandas as pd

from pydaisy.Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime

from pydaisy.Daisy import *

xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']
xl['yr'] = xl['date'].map(lambda x: x.year)

def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())

MotherFolder='..\RunDaisy17'
items = os.walk(MotherFolder)
index=1
yearlydata =[]
yearlydataN =[]
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        Nharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
        N =Nharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        wc = DMG.get_group('Wclover').sum(axis=1)
        Nrg = N.get_group('Ryegrass').sum(axis=1)
        Nwc = N.get_group('Wclover').sum(axis=1) 
        df2= pd.DataFrame([rg, wc, Nrg, Nwc]).T
        df2.columns =['Ryegrass', 'Wclover', 'RyegrassN', 'WcloverN']
        df2['sim-totDM'] = df2['Ryegrass']+df2['Wclover']
        df2['sim-totN'] = df2['RyegrassN']+df2['WcloverN']
        df2 = df2.loc['2006-1-1':'2011-1-1',:]
        df3 = df2['sim-totDM'].resample('Y').sum()     
        df4 = df2['sim-totN'].resample('Y').sum()
        
        for y in range(2006, 2010):
            parc_N = {}
            parc_sum = {} 
          #  parc_pct = {}
            sum=0
            for index, row in xl.iterrows():
                if row['id']==d and row['date'].year==y:
                    if row['Parc nr'] not in parc_sum:
                        parc_sum[row['Parc nr']]=0
                    parc_sum[row['Parc nr']]+= row['DMtot_kg']                 
                    sum=sum +row['DMtot_kg']
                   # rep=list(parc_sum.values())
            if(len(parc_sum)==2):
                rep=list(parc_sum.values())
                yearlydata.append([d, y, rep[0], rep[1], df3[datetime(y,12,31)]])

            for index, row in xl.iterrows():
                if row['id']==d and row['date'].year==y:
                    if row['Parc nr'] not in parc_N:
                        parc_N[row['Parc nr']]=0
                    parc_N[row['Parc nr']]+= row['Ntot_kg']                 
                    sum=sum +row['Ntot_kg']
                    repN=list(parc_N.values())
            if(len(parc_N)==2):
                repN=list(parc_N.values())
                yearlydataN.append([d, y, repN[0], repN[1], df4[datetime(y,12,31)]])               

          #  for index, row in xl.iterrows():
           #     if row['id']==d and row['date'].year==y:
            #        if row['Parc nr'] not in parc_pct:
             #           parc_N[row['Parc nr']]=0
              #      parc_N[row['Parc nr']]+= row['pct_clo']                 
               #     sum=sum +row['Ntot_kg']
                #    repN=list(parc_N.values())
            #if(len(parc_N)==2):
             #   repN=list(parc_N.values())
              #  yearlydataN.append([d, y, repN[0], repN[1], df4[datetime(y,12,31)]])        
                
final = pd.DataFrame(yearlydata, columns=('d','year', 'rep1', 'rep2', 'simDM'))
final['measDM'] = (final[['rep1', 'rep2']].mean(axis=1))/1000
final['treat'] = final['d'].str[:2]
finalN = pd.DataFrame(yearlydataN, columns=('d','year','rep1N', 'rep2N', 'simN'))
finalN['measN'] = finalN[['rep1N', 'rep2N']].mean(axis=1)    
finalN['treat'] = finalN['d'].str[:2]
treat = final.groupby('treat')
treatN= finalN.groupby('treat')

plt.subplot(1,3,3)
plt.scatter()

fig = plt.figure(figsize=(15, 10))

plt.subplot(1,3,1)
plt.scatter(treat.get_group('T4')['measDM'], treat.get_group('T4')['simDM'], marker='o', c='black', s=15, label = 'measVSsim,T4')
plt.scatter(treat.get_group('T5')['measDM'], treat.get_group('T5')['simDM'], marker='o', c='red', s=15, label = 'measVSsim,T5')
plt.scatter(final['rep1']/1000, final['rep2']/1000, marker='x', c='blue', s=15, label = 'reps')
plt.title('Clovergrass', position = (0.9, 0.9), fontweight="bold", fontsize=8)
plt.ylabel('simulated (t DM/ha)') 
plt.xlabel('measured')
plt.axis([0,20, 0,20])
plt.plot([0,20], [0,20], c='black', linestyle ='--')
plt.legend()
rmse_val = rmse(final['measDM'],final['simDM'])
rs=str(round(rmse_val, 2))
r2=str(round(r2_score(final['measDM'], final['simDM']), 2))
eva= ('RMSE='+(rs)+'\n' 'r2='+ (r2))
plt.text(15,1, eva)

plt.subplot(1,3,2)
#plt.scatter(finalN['measN'], finalN['simN'], marker='o', c='black', s=15, label = 'measVSsim')
plt.scatter(treatN.get_group('T4')['measN'], treatN.get_group('T4')['simN'], marker='o', c='black', s=15, label = 'measVSsim,T4')
plt.scatter(treatN.get_group('T5')['measN'], treatN.get_group('T5')['simN'], marker='o', c='red', s=15, label = 'measVSsim,T5')
plt.scatter(finalN['rep1N'], finalN['rep2N'], marker='x', c='blue', s=15, label = 'reps')
plt.title('Clovergrass', position = (0.9, 0.9), fontweight="bold", fontsize=8)
plt.ylabel('simulated (kg N/ha)') 
plt.xlabel('measured')
plt.axis([0,500, 0,500])
plt.plot([0,500], [0,500], c='black', linestyle ='--')
plt.legend()
rmse_val = rmse(finalN['measN'],finalN['simN'])
rs=str(round(rmse_val, 2))
r2=str(round(r2_score(finalN['measN'], finalN['simN']), 2))
eva= ('RMSE='+(rs)+'\n' 'r2='+ (r2))
plt.text(400,1, eva)

#plt.scatter(final['sim'], final['measDM'])
#plt.scatter(final['rep1'], final['rep2'])