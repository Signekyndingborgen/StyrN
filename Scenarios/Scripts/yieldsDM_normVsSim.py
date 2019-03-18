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
from Create_rotations2 import split_unique_name

import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime

norm = pd.read_excel('../common/Nnorm_2019_yields.xlsx', sheet_name = "Ark1")
norm.index = norm['afgkode']
rota = pd.DataFrame(pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Rotations'))
rota.index = rota['ID']
crops = pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Crops')
crops.index = crops['Crop']
norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['afgkode']

grain = ['SB', 'Winter Wheat JG','Vinterbyg','Rug','Winter Rape PA','Spring Wheat',
         'Rug', 'Froegraes', 'Potato; Sava_Figaro','Fodder Beet','Pea']
silo = ['Ryegrass', 'Wclover', 'Silomajs', 'SB-green'] 

MotherFolder='..\Run'
items = os.walk(MotherFolder)
index=1
soil ='JB1'
    
allresults={}

for root, dirs, filenames in items:
    for d in dirs:
        cropyield={}            
        harvest=DaisyDlf(os.path.join(root, d, "DailyP-harvest.dlf"))
        df=harvest.Data
        DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
        DMG =DMharv.groupby('crop')
        for cropname in silo:
            if cropname in DMG.groups.keys():
                rg = DMG.get_group(cropname).sum(axis=1)
                cropyield[cropname]= rg.resample('Y').sum()
 
        DMharv= df[['crop', 'sorg_DM']]
        DMG =DMharv.groupby('crop')
        for cropname in grain:
            if cropname in DMG.groups.keys():
                rg = DMG.get_group(cropname).sum(axis=1)
                cropyield[cropname]= rg.resample('Y').sum()
        allresults[d]=cropyield    
 
for key, value in allresults.items():
    name_entries = split_unique_name(key)    
    if name_entries['IsConventional'] and name_entries['ManureMass']!=230:
        print(d)
        
        maxnumberyear = 6
        while pd.isna(rota[name_entries['rotation']][maxnumberyear]):
            maxnumberyear-=1
        for year in range(1, maxnumberyear+1):
            cropname = rota[name_entries['rotation']][year].strip()
            crop_ID = int(crops['afgkode1'][cropname])
            yield_norm = norm['norm_' + soil][crop_ID]*norm['yieldfaktorDM'][crop_ID]
            daisynames = crops['Daisynavn1'][cropname].split(',')
            if not pd.isna(crops['Harvest2'][cropname]):
                crop_ID2 = int(crops['afgkode2'][cropname])
                yield_norm2 = norm['norm_' + soil][crop_ID2]*norm['yieldfaktorDM'][crop_ID2]
                daisynames2 = crops['Daisynavn2'][cropname].split(',')
                for daisyname in daisynames2:
                    if crops['Daisynavn2']=='Wclover, Ryegrass':
                        value['RyeGrass'][str(1993+year)][0] + value['WClover'][str(1993+year)][0]    
                        if str(1993+year) in value[daisyname.strip()]:
                            print(daisyname + ' ' + str(value[daisyname.strip()][str(1993+year)][0]-yield_norm))
            
            for daisyname in daisynames:
                if crops['Daisynavn2']=='Wclover, Ryegrass':
                    value['RyeGrass'][str(1993+year)][0] + value['WClover'][str(1993+year)][0]   #              
                else:
                    if str(1993+year) in value[daisyname.strip()]:
                        
 #Clovergrass = value['RyeGrass'][str(1993+year)][0] + value['WClover''][str(1993+year)][0]
                        print(daisyname + ' ' + str(value[daisyname.strip()][str(1993+year)][0]-yield_norm))

#if crops[['Daisynavn1']=='Wclover, Ryegrass':
#                sum values for wclover and rygrass :-) 