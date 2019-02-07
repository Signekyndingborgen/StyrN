# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:31:39 2018

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

xl = pd.read_excel(r'..\Meas_yields.xlsx', 'data')
xl.set_index('date', inplace=True)
xl['id'] = 'T'+xl['treatment'].map(str)+'_S'+xl['block'].map(str)+'_'+xl['field']

MotherFolder='..\RunDaisy2.1'
items = os.walk(MotherFolder)
index=1
fig = plt.figure(figsize=(15, 8))
#fig, axes = plt.subplots(nrows=2, ncols=3)
for root, dirs, filenames in items:
    for d in dirs:
        print(d)
        harvestR=DaisyDlf(os.path.join(root, d, "DailyP-Ryegrass.dlf"))
        harvestW=DaisyDlf(os.path.join(root, d, "DailyP-Wclover.dlf"))
        rg=harvestR.Data.loc['2006-1-1':'2011-1-1',:]
        wc=harvestW.Data.loc['2006-1-1':'2011-1-1',:]
        rg['Ntot'] = ['NLeaf']+rg['NDead']+rg['NStem']+rg['NSOrg']
        wc['Ntot'] = wc['NLeaf']+wc['NStem']+wc['NSOrg']
        wc['Nfix'] = wc['Fixated']
        ax=plt.subplot(4,3,index)
        index+=1
        plt.plot(rg.index, (rg['Ntot']),  c='black', label= 'grass')
        plt.plot(wc.index, (wc['Ntot']), c='red', label = 'clover_Ntot')
        plt.plot(wc.index, (wc['Nfix']), c='green', label = 'clover_Nfix')
        plt.legend()
        plt.title(d, position = (0.6, 0.8), fontweight="bold", fontsize=10)
        ax.set(ylabel=('kg N /ha'))
        plt.show()
        plt.tight_layout()

fig.savefig("N_total_fix_v.2.1-2.pdf", bbox_inches='tight')      
