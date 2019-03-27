# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:58:09 2019

@author: tqc268
"""
import pandas as pd
import fertil

soil = 'JB 1+3'
i = 0

rota = pd.DataFrame(pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Rotations'))
rota.index = rota['ID']
crops = pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Crops')
crops.index = crops['Crop']
manure = pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Manure1')
manure.index = manure['ID']

res=[]

for i in range(1, 23): ## SÆDSKIFTE
    rotation = rota.columns[i]
    #find rotation length
    maxnumberyear = 6
    while pd.isna(rota[rotation][maxnumberyear]):
        maxnumberyear-=1

    LastYearCropName = rota[rotation][maxnumberyear].strip()

    AllCropIDs = []
        
    for year in range(0, maxnumberyear): 
        cropname = rota[rotation][year].strip()
        crop_ID = int(crops['afgkode1'][cropname])
        AllCropIDs.append(crop_ID)
#    print(AllCropIDs)

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
                        
        

    for ManureSim in ManureSims:
        for year in range(0, maxnumberyear): 
            cropname = rota[rotation][year].strip()
            crop_ID = int(crops['afgkode1'][cropname])
            LastYearCropID = int(crops['afgkode1'][LastYearCropName])
            AllCropIDs.append(crop_ID)
    
            res.append(CalcFertil(crop_ID, LastYearCropID, soil, AllCropIDs, ManureSim[0], ManureSim[1], ManureSim[2]))
            LastYearCropName = cropname