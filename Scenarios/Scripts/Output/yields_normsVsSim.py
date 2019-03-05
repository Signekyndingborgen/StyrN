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
MotherFolder='..\..\RunK'
items = os.walk(MotherFolder)
index=1

harvest=DaisyDlf(os.path.join(root, "DailyP-harvest.dlf"))
df=harvest.Data
DMharv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
DMG =DMharv.groupby('crop')
rg = DMG.get_group('Ryegrass').sum(axis=1)
wc = DMG.get_group('Wclover').sum(axis=1)
# Laver et subplot, som derefter bliver det aktive som de næste plt virker på
df2= pd.DataFrame([rg, wc]).T
df2.columns =['Ryegrass', 'Wclover']
df2['sim-totalDM']=df2['Ryegrass']+df2['Wclover']
#df2 = df2.loc['2006-1-1':'2011-1-1',:]
# df3 = df2['sim-totalDM'].resample('Y', how='sum')

p1=plt.bar(df2.index, df2['Ryegrass'])
p2=plt.bar(df2.index, df2['Wclover'])

plt.legend((p1[0], p2[0]), ('Ryegrass', 'Clover'))
plt.title(d, position = (0.9, 0.9), fontweight="bold", fontsize=8)
plt.show()
plt.tight_layout()