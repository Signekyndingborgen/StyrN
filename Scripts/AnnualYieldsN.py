# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 11:53:20 2018

@author: tqc268
"""
from sklearn.metrics import r2_score
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
fig = plt.figure(figsize=(5, 5))
ax=plt.subplot()
index=1
yearlydata =[]
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        wc = DMG.get_group('Wclover').sum(axis=1)
        df2= pd.DataFrame([rg, wc]).T
        df2.columns =['Ryegrass', 'Wclover']
        df2['sim-totDM'] = df2['Ryegrass']+df2['Wclover']
        df2 = df2.loc['2006-1-1':'2011-1-1',:]
        df3 = df2['sim-totDM'].resample('Y').sum()     
        for y in range(2006, 2010):
            parc_sum={}
            
            sum=0
            for index, row in xl.iterrows():
                if row['id']==d and row['date'].year==y:
                    if row['Parc nr'] not in parc_sum:
                        parc_sum[row['Parc nr']]=0
                    parc_sum[row['Parc nr']]+= row['DMtot_kg']                 
                    sum=sum +row['DMtot_kg']
                    rep=list(parc_sum.values())
             
            if(len(parc_sum)==2):
                rep=list(parc_sum.values())
                yearlydata.append([d, y, rep[0], rep[1], df3[datetime(y,12,31)]])
                
final = pd.DataFrame(yearlydata, columns=('d','year', 'rep1', 'rep2', 'simDM'))
final['measDM'] = (final[['rep1', 'rep2']].mean(axis=1))/1000
plt.scatter(final['measDM'], final['simDM'], marker='x', c='black', s=15)
plt.title('Clovergrass', position = (0.35, 0.85), fontweight="bold", fontsize=8)
#plt.ylabel('simulated (t DM/ha)') 
#plt.xlabel('measured')
plt.axis([0,20, 0,20])
plt.plot([0,20], [0,20], c='black', linestyle ='--')
rmse_val = rmse(final['measDM'],final['simDM'])
rs=str(round(rmse_val, 2))
r2=str(round(r2_score(final['measDM'], final['simDM'])), 2)
eva= ('RMSE='+(rs)+'\n' 'r2='+ (r2))
plt.text(10,1, eva)

index=1
yearlydata =[]
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
        Nharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
        N =Nharv.groupby('crop')
        Nrg = N.get_group('Ryegrass').sum(axis=1)
        Nwc = N.get_group('Wclover').sum(axis=1) 
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        df2= pd.DataFrame([Nrg, Nwc]).T
        df2.columns =['RyegrassN', 'WcloverN']
        df2['sim-totN'] = df2['RyegrassN']+df2['WcloverN']
        df2 = df2.loc['2006-1-1':'2011-1-1',:]
        df4 = df2['sim-totN'].resample('Y').sum()
        
        for y in range(2006, 2010):
            parc_sum={}
            sum=0
            for index, row in xl.iterrows():
                if row['id']==d and row['date'].year==y:
                    if row['Parc nr'] not in parc_sum:
                        parc_sum[row['Parc nr']]=0
                    parc_sum[row['Parc nr']]+= row['Ntot_kg']                    
                    sum=sum +row['Ntot_kg']                    
                    rep=list(parc_sum.values())
             
            if(len(parc_sum)==2):
                rep=list(parc_sum.values())
                yearlydata.append([d, y, rep[0], rep[1], df4[datetime(y,12,31)]])
                
finalN = pd.DataFrame(yearlydata, columns=('d','year','rep1N', 'rep2N', 'simN'))

finalN['measN'] = finalN[['rep1N', 'rep2N']].mean(axis=1)    
plt.scatter(finalN['measN'], finalN['simN'], marker='x', c='black', s=15)
plt.title('Clovergrass', position = (0.35, 0.85), fontweight="bold", fontsize=8)
plt.ylabel('simulated (t DM/ha)') 
plt.xlabel('measured')
plt.axis([0,150, 0,150])
plt.plot([0,150], [0,150], c='black', linestyle ='--')
rmse_val = rmse(finalN['measN'],finalN['simN'])
rs=str(round(rmse_val, 2))
eva= ('RMSE='+'\n'+(rs))
plt.text(10,1, eva)

#plt.scatter(final['sim'], final['measDM'])
#plt.scatter(final['rep1'], final['rep2'])