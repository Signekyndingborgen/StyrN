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

# Plot tørstofsudbytte for kløver, græs og samlet i søjlediagram

MotherFolder='..\RunDaisy2.1'
items = os.walk(MotherFolder)

#harvestR=DaisyDlf(r'H:\Documents\StyrN\KG_kalib\RunDaisy1\T5_S3_IND\DailyP-Ryegrass.dlf')
#harvestW=DaisyDlf(r'H:\Documents\StyrN\KG_kalib\RunDaisy1\T5_S3_IND\DailyP-Wclover.dlf')

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
        
        ax=plt.subplot(4,3,index)
        index+=1
        plt.scatter(rg.index, (rg['day_length']),  marker='o', c='black', s=5, label= 'grass')
        plt.scatter(wc.index, (wc['day_length']),  marker='x', c='red', s=5, label = 'clover')
        plt.legend()
#        plt.legend(('time', 'LAI/N_leaf'))
        plt.title(d, position = (0.6, 0.8), fontweight="bold", fontsize=10)
        ax.set(ylabel=('Day length'))
        plt.show()
        plt.tight_layout()

fig.savefig("Daylength_v2.1.pdf", bbox_inches='tight')      
