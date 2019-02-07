# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:31:39 2018

@author: tqc268
"""

import sys
import pandas as pd
import os
sys.path.append(r'../../../pydaisy')

from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
sys.path.append(r'..\..\..\.')

from pydaisy.Daisy import *

# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram

MotherFolder='..\RunDaisy16opt'
items = os.walk(MotherFolder)

index=1
fig = plt.figure(figsize=(15, 8))
#fig, axes = plt.subplots(nrows=2, ncols=3)
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
# summere og plot af udbytte i tørstof DM       
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        rg = DMG.get_group('Ryegrass').sum(axis=1)
        wc = DMG.get_group('Wclover').sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        ax=plt.subplot(3,4,index)
        index+=1
        df22= pd.DataFrame([rg, wc]).T
        df22.columns =['Ryegrass', 'Wclover']
        df2 = df22.loc['2006-1-1':'2011-1-1',:]   
        df2.index = df2.index.strftime("%Y-%m")
        p1=plt.bar(df2.index, df2['Ryegrass'])
        p2=plt.bar(df2.index, df2['Wclover'])
        #Laver et subplot, som derefter bliver det aktive som de næste plt virker på
        #ax.set(ylabel=('simulated (t DM/ha)')) 
        plt.legend((p1[0], p2[0]), ('Ryegrass', 'Clover'))
        plt.title(d+'-DM', position = (0.2, 0.9), fontweight="bold", fontsize=8)
        #ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
        #ax.figure.autofmt_xdate()
        #ax.xaxis.set_major_locator()
        #ax.xaxis.set_major_formatter()
        plt.show()
        plt.tight_layout()
fig.savefig("KG_DM_stackedbar.pdf", bbox_inches='tight')      
