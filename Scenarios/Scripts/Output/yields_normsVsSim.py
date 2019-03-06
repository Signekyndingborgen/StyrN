# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:17:20 2019

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

norm = pd.read_excel('../../common/Nnorm_2019_yields.xlsx', sheet_name = "Ark1")
norm.index = norm['afgkode']
## Hente yield_soil, all feed crops must be converted to DM from FE
"""if afgkode == 216: *1.14
   if afgkode == 701: 1.26
   if afgkode == 252: *1.39
   if afgkode == 260 OR 963 OR 257 OR 256: 1.2
   if afgkode == : *
   
"""
grain = ['SB', 'Winter Wheat JG','Vinterbyg','Rug','Winter Rape PA','Spring Wheat',
         'Rug', 'Froegraes', 'Potato; Sava_Figaro','Fodder Beet','Pea']
silo = ['Ryegrass', 'Wclover', 'Silomajs']

MotherFolder='..\..\Run'
items = os.walk(MotherFolder)
index=1

allresults={}

for root, dirs, filenames in items:
    for d in dirs:
        if '170_True' in d:    
            print(d)
            cropyield={}
            harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
            df=harvest.Data
            DMharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
            DMG =DMharv.groupby('crop')
            for cropname in silo:
                if cropname in DMG.groups.keys():
                    rg = DMG.get_group(cropname).sum(axis=1)
                    cropyield[cropname]= rg.resample('Y').sum().mean()
     
            DMharv= df[['crop', 'sorg_N']]
            DMG =DMharv.groupby('crop')
            for cropname in grain:
                if cropname in DMG.groups.keys():
                    rg = DMG.get_group(cropname).sum(axis=1)
                    cropyield[cropname]= rg.resample('Y').sum().mean()
            allresults[d]=cropyield    

"""
Omregn udbyttenormerne 
"""
