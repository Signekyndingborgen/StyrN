import sys
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
import shutil

norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Ark1")
norm.index = norm['afgkode']

def CalcFertil(crop_ID, LastYearCropID, soil, AllCropIDs):
    norm_crop = norm[soil][crop_ID]
    forfrugt=0
    if norm['Ja/Nej'][crop_ID[i]]==1
        forfrugt = norm['Forfrugt'][LastYearCropID]
    
    SumNorm=0
    for i in range(0:len(AllCropIDs))
        SumNorm+=norm[soil][AllCropIDs[i]]
        if norm['Ja/Nej'][AllCropIDs[i]]==1:
            lastyear=i-1
            if i==0:
                lastyear=len(AllCropIDs)
            SumNorm-=norm['Forfrugt'][AllCropIDs[lastyear]]
    
    weight = (norm_crop - forfrugt)/SumNorm ## forfrugten fra forrige år skal trækkes fra
    
    return weight 




# Calc the weights of the crop rotation with the condition that forfrugt Ja/Nej skal være 1 ellers er vægt = 0  
     #   gen = (i for i in norm.loc[crop_ID]['Ja/Nej'] if i == 1)
    #for i in gen:
        print(i)
    #for i in range(1,7):
        if norm.loc[crop_ID]['Ja/Nej'][i] == 1:
            weight[i] =  1 # (norm_crop - forfrugt)/(norm_crop - forfrugt).sum() ## forfrugten fra forrige år skal trækkes fra
        else:
            weight[i] = 0
        #weight += weight
    print(ind) 
    print(weight)
    if not pd.isna(rota[rotation].loc['Konv']):
        manID = rota[rotation].loc['Konv']
        gylle = manure.loc[manID][1:]
        if gylle[0] == 'Cattleslurry':
            for fer in range(1,4):
                if not pd.isna(gylle[fer]):
                    gyl_tot= gylle[fer]*0.7*len(ind) # change to length of rotation
                    Fert_yr = pd.DataFrame(weight*gyl_tot, columns = ['gylleN'])
                    Fert_yr['MineralN'] = norm_crop - Fert_yr.gylleN
                    print (Fert_yr)
        if gylle[0] == 'Pigslurry':
            for fer in range(1,4):
                if not pd.isna(gylle[fer]):
                    gyl_tot = gylle[fer]*0.75*len(ind) # change to length of rotation
                    Fert_yr = pd.DataFrame(weight*gyl_tot, columns = ['gylleN'])
                    Fert_yr['MineralN'] = norm_crop - Fert_yr.gylleN
                    print(Fert_yr)    
    
    if not pd.isna(rota[rotation].loc['Øko']):
        manID = rota[rotation].loc['Øko']
        gylle = manure.loc[manID][1:]
        if gylle[0] == 'Cattleslurry':
            for fer in range(1,4):
                if not pd.isna(gylle[fer]):
                    gyl_tot= gylle[fer]*0.7*len(ind) # change to length of rotation
                    Fert_yr = pd.DataFrame(weight*gyl_tot, columns = ['gylleN'])
                    print(Fert_yr)
                    #fert[rotation].append(Fert_yr)
        if gylle[0] == 'Pigslurry':
            for fer in range(1,4):
                if not pd.isna(gylle[fer]):
                    gyl_tot = gylle[fer]*0.75*len(ind) # change to length of rotation
                    Fert_yr = pd.DataFrame(weight*gyl_tot, columns = ['gylleN'])
                    print(Fert_yr)
    return Fert_yr