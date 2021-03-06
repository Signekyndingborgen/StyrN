# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:34:37 2018

@author: tqc268
"""
import sys
import pandas as pd
import os
sys.path.append(r'../../../pydaisy')
from pydaisy.Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
sys.path.append(r'..\..\..\.')

from pydaisy.Daisy import *

# læser målt data og giver id som matcher d
xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

#converts tuple into dataframes - HER GÅR DET galt...
#pf3=pd.DataFrame(meas, columns=['grassN'])
def rmse(pred, obs):
    return np.sqrt(((pred - obs) ** 2).mean())
# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram
MotherFolder='..\RunDaisy2.2'
items = os.walk(MotherFolder)
index=1
fig = plt.figure(figsize=(10, 10))
# fig, axes = plt.subplots(nrows=2, ncols=3)
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
# summere og plot af udbytte i tørstof DM       
        DMharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
        DMG =DMharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        #wc = DMG.get_group('Wclover').sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        ax=plt.subplot(5,5,index)
        index+=1
        df22= pd.DataFrame([rg]).T
        df22.columns =['Ryegrass']
        #df22['sim-totalN']=df22['Ryegrass']
        df2 = df22.loc['2006-1-1':'2011-1-1',:]                 
        s1=xl.loc[xl['id']==d]
        meas =(s1.groupby(s1.index)['grassDM'].mean(), s1.groupby(s1.index)['grassN'].mean())
        # Samler en dataframe med målt og simulert
        ms=df2.join(meas[0]) 
        ms=ms.join(meas[1])
        #ms['total-N']=ms['cloverN']+ms['grassN']

        #plt.scatter(ms['cloverN'], ms['Wclover'], marker='x', c='black', s=15)
        #plt.title(d+'-Clover', position = (0.35, 0.85), fontweight="bold", fontsize=8)
        #ax.set(ylabel=('simulated (kg N/ha)'), xlabel= 'measured')
        #ax.set(xlim=(0,150), ylim=(0,150))
        #ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')
        #rmse_val = rmse(ms['cloverN'],ms['Wclover'])
        #rs=str(round(rmse_val, 2))
        #eva= ('RMSE='+'\n'+(rs))
        #plt.text(100,1, eva)
        
        ax=plt.subplot(5,5,index)
        index+=1
        plt.scatter(ms['grassN'], ms['Ryegrass'], marker='x', c='black', s=15)
        plt.title(d+'-Grass', position = (0.35, 0.85), fontweight="bold", fontsize=8)
        ax.set(ylabel=('simulated (kg N/ha)'), xlabel= 'measured')
        ax.set(xlim=(0,150), ylim=(0,150))
        ax.plot([0, 1], [0, 1], transform=ax.transAxes, c='black', linestyle ='--')
        rmse_val = rmse(ms['grassN'],ms['Ryegrass'])
        rs=str(round(rmse_val, 2))
        eva= ('RMSE='+'\n'+(rs))
        plt.text(100,1, eva)
        plt.tight_layout()
#fig.savefig("MeasVSmod_N_C_V.2.2.pdf", bbox_inches='tight')
