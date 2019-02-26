# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:36:40 2019

@author: tqc268

Vinterbyg PE fikset! 
Og slætter alle filer i Run mappen inden kørsel - og laver en ny Run mappe.
Skriver sædskifter og datoer for 1 jord-klima-init-C kombination.
"""
import sys
import pandas as pd
import os
sys.path.insert(0,r'../../pydaisy/')
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
import shutil
from pydaisy.Daisy import *

# Import excel w scenario information
# the crop rotations
rota = pd.DataFrame(pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Rotations'))
rota.index = rota['ID']
crops = pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Crops')
crops.index = crops['Crop']
manure = pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Manure1')
manure.index = manure['ID']

# import table with file names for weather data, soil data, initialization file, initial SOC content
conditions = pd.read_excel('../common/masterinput_v1.xlsx', sheet_name = 'soil_climate_more')
    
path=r'../Run'

shutil.rmtree(path)
#os.makedirs(path)

template = DaisyModel(os.path.join(path, '../Common/Scenarier_v1.dai'))
i=0  
for i in range(1, 13):
    rotation=rota.columns[i]
        #find rotation length
    maxnumberyear = 6
    while pd.isna(rota[rotation][maxnumberyear]):
        maxnumberyear-=1

    LastYearCropName = rota[rotation][maxnumberyear].strip()

    AllCropIDs = []
        
    for year in range(1, maxnumberyear+1): 
        cropname = rota[rotation][year].strip()
        crop_ID = int(crops['afgkode1'][cropname])
        AllCropIDs.append(crop_ID)


    #Find the different manure realisations
    ManureSims = []
    OrgKonv=['Konv', 'Øko' ]
    for t in OrgKonv:
        if not pd.isna(rota[rotation][t]):
            IsConventional=True
            ManureID = rota[rotation][t]
            ManureType = manure['Manuretype'][ManureID]
            for ManureMass in manure.loc[ManureID][2:6]:
                if not pd.isna(ManureMass):
                    if t =='Konv':
                        ManureSims.append([ManureType, ManureMass, True])
                    else:
                        ManureSims.append([ManureType, ManureMass, False])

       
    newfile= template.copy()    
    block = newfile.Input['defaction'][1]
    #Loop the manure realisations
    for ManureSim in ManureSims:
        
        #Loop the years
        for year in range(0,6):
            if not pd.isna(rota[rotation][year]):
                cropname = rota[rotation][year].strip()
                
                #Plowing
                if not pd.isna(crops['Plowing'][cropname]):
                    block.Children.append(DaisyEntry('wait_mm_dd', [crops['Plowing'][cropname].strftime('%m %d')]))  
                    block.Children.append(DaisyEntry('plowing',[]))
                
                #Sowing
                if not pd.isna(crops['Sowing1'][cropname]):
                    block.Children.append(DaisyEntry('wait_mm_dd', [crops['Sowing1'][cropname].strftime('%m %d')]))  
                    for c in crops['Daisynavn1'][cropname].split(','):
                        block.Children.append(DaisyEntry('sow', ['"' + str(c.strip()) +'"']))
                if not pd.isna(crops['Sowing2'][cropname]):
                    if str(crops['Sowing2'][cropname]) < str(crops['Harvest1'][cropname]):                
                        block.Children.append(DaisyEntry('wait_mm_dd', [crops['Sowing2'][cropname].strftime('%m %d')]))  
                        for c in crops['Daisynavn2'][cropname].split(','):
                            block.Children.append(DaisyEntry('sow', ['"' + str(c.strip()) +'"']))
                print(rotation)
                print(AllCropIDs)
                #Fertilize
                man=CalcFertil(crop_ID, LastYearCropID, soil, AllCropIDs, ManureSim[0], ManureSim[1], ManureSim[2])
                block.Children.append(DaisyEntry('wait_mm_dd', [crops['FDate1'][cropname].strftime('%m %d')]))
                fert = DaisyEntry('fertilize',[])
                fert.Children.append(DaisyEntry('"' + ManureSim[0] +'"',[]))
                fert.Children.append(DaisyEntry('equivalent_weight',[ str(man[0]) , '[kg N/ha]']))                
                block.Children.append(fert)
                ## Fertil2.... mangler
                
                #Harvest
                if not pd.isna(crops['Harvest1'][cropname]):
                    harvestdates=[]
                    if isinstance(crops['Harvest1'][cropname],datetime): 
                        harvestdates.append(crops['Harvest1'][cropname])
                    else:
                        for s in crops['Harvest1'][cropname].split(','):
                            harvestdates.append(datetime(2010, int(s.split('/')[1]), int(s.split('/')[0])))
                    for date in harvestdates:
                        block.Children.append(DaisyEntry('wait_mm_dd', [date.strftime('%m %d')]))
                        for c in crops['Daisynavn1'][cropname].split(','):
                            block.Children.append(DaisyEntry('harvest', ['"' + str(c.strip()) +'"'] ))
                
                #Catch crops
                if not pd.isna(crops['Sowing2'][cropname]):
                    if str(crops['Harvest1'][cropname]) < str(crops['Sowing2'][cropname]):
                        block.Children.append(DaisyEntry('wait_mm_dd', [crops['Sowing2'][cropname].strftime('%m %d')]))
                        block.Children.append(DaisyEntry('plowing', []))
                        for c in crops['Daisynavn2'][cropname].split(','):
                            block.Children.append(DaisyEntry('sow', ['"' + str(c.strip()) +'"']))
                    else:
                        if not pd.isna(crops['Harvest2'][cropname]):
                            harvestdates=[]
                            if isinstance(crops['Harvest2'][cropname],datetime): 
                                harvestdates.append(crops['Harvest2'][cropname])
                            else:
                                for s in crops['Harvest2'][cropname].split(','):
                                    harvestdates.append(datetime(2010, int(s.split('/')[1]), int(s.split('/')[0])))
                            for date in harvestdates:
                                block.Children.append(DaisyEntry('wait_mm_dd', [date.strftime('%m %d')]))
                                for c in crops['Daisynavn2'][cropname].split(','):
                                    block.Children.append(DaisyEntry('harvest', ['"' + str(c.strip()) +'"']))
        #Now print the daisy file                            
        newfile.save_as(os.path.join(path, rotation + '_' + str(int(ManureSim[1])) +'_' + str(ManureSim[2]), 'model.dai'))
