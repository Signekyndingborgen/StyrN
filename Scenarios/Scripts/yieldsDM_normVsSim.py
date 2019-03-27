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
from Create_rotations_spinup import split_unique_name

import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime

rota = pd.DataFrame(pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Rotations'))
rota.index = rota['ID']
crops = pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Crops')
crops.index = crops['Crop']
norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['afgkode']

grain = ['SB', 'Winter Wheat JG','Vinterbyg','Rug','Winter Rape PA','Spring Wheat',
         'Rug', 'Froegraes', 'Potato; Sava_Figaro','Sugar Beet','Pea']
silo = ['Ryegrass', 'Wclover', 'Silomajs', 'SB-green'] 

MotherFolder='..\Run1'
items = os.walk(MotherFolder)
index=1
soil ='JB4'
    
allresults={}

for root, dirs, filenames in items:
    for d in dirs:
        cropyield={}            
        if os.path.isfile(os.path.join(root, d, "harvest.dlf")):
            harvest=DaisyDlf(os.path.join(root, d, "harvest.dlf"))
            df=harvest.Data
            DMharv= df[['crop', 'leaf_DM', 'stem_DM','sorg_DM']]
            DMS =DMharv.groupby('crop')
            for cropname in silo:
                if cropname in DMS.groups.keys():
                    rg = DMS.get_group(cropname).sum(axis=1)
                    cropyield[cropname]= rg.resample('Y').sum()
                    
            DMharvG= df[['crop', 'sorg_DM']]
            DMG =DMharvG.groupby('crop')
            for cropname in grain:
                if cropname in DMG.groups.keys():
                    rg = DMG.get_group(cropname).sum(axis=1)
                    cropyield[cropname]= rg.resample('Y').sum()
            allresults[d]=cropyield
        #print(d)

for key, value in allresults.items():
    name_entries = split_unique_name(key)    
    if name_entries['IsConventional'] and name_entries['ManureMass']!=230 and name_entries['Soiltype'][0:3]=='JB6':
        evalu={}
        maxnumberyear = 6
        while pd.isna(rota[name_entries['rotation']][maxnumberyear]):
            maxnumberyear-=1
        print(key)
        #print([name_entries['rotation'], name_entries['ManureMass'], name_entries['Soiltype']])
        sim_yields =[]
        for year in range(1, maxnumberyear+1):
            actualyear=1990+year
            cropname = rota[name_entries['rotation']][year].strip()
            crop_ID = int(crops['afgkode1'][cropname])
            yield_norm = norm['norm_' + soil][crop_ID]*norm['yieldfaktorDM'][crop_ID]
            daisynames = crops['Daisynavn1'][cropname].split(',')
            if not pd.isna(crops['Harvest2'][cropname]):
                crop_ID2 = int(crops['afgkode2'][cropname])
                yield_norm2 = norm['norm_' + soil][crop_ID2]*norm['yieldfaktorDM'][crop_ID2]
                daisynames2 = crops['Daisynavn2'][cropname].split(',')
                
                #if crops['Daisynavn2'][cropname]=='Ryegrass, Wclover':
                #    sim_yields.append(value['Ryegrass'][str(actualyear)][0] + value['Wclover'][str(actualyear)][0])
                #    print([daisyname, np.mean(sim_yields)*10])
            for daisyname in daisynames:
                if crops['Daisynavn1'][cropname]=='Wclover,Ryegrass':
                   # print('virker')
                    sim_yields.append(['clovergrass', value['Wclover'][str(actualyear)][0] + value['Ryegrass'][str(actualyear)][0]])
#                    sim_yields.append('clovergrass, c)
                    print(sim_yields)
                    #print([daisyname, np.mean(sim_yields)*10])
                    #evalu[daisyname] = [int(sim_yield), int(yield_norm)]
                else:
                    #if str(1990+year) in value[daisyname.strip()]:
                    sim_yields.append([daisyname, value[daisyname.strip()][str(1990+year)][0]])
                print(sim_yields)
                        #rint([daisyname, np.mean(sim_yields)*10])
 #Clovergrass = value['RyeGrass'][str(1993+year)][0] + value['WClover''][str(1993+year)][0]
      #                  evalu[daisyname] = [int(sim_yield), int(yield_norm)]
                            #print(str(value[daisyname.strip()][str(1993+year)][0]-yield_norm))