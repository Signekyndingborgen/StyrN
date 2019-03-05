# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:25:14 2019

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

rota = pd.DataFrame(pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Rotations'))
rota.index = rota['ID']

crops = pd.read_excel('../common/masterinput_v2.xlsx',sheet_name= 'Crops')
crops.index = crops['Crop']


for i in range(3, 6):
    rotation=rota.columns[i]
        #find rotation length
    maxnumberyear = 6
    while pd.isna(rota[rotation][maxnumberyear]):
        maxnumberyear-=1


    #Make a list with all cropIDs. We need this in the fertilize calc
    AllCropIDs = []
    for year in range(1, maxnumberyear+1): 
        cropname = rota[rotation][year].strip()
        crop_ID = int(crops['afgkode1'][cropname])
        AllCropIDs.append(crop_ID)
        


harvestname = crops['Daisynavn1'][cropname]


"""
def extract(crop_name, filnavn, output): # output altid være N?
    harvest=DaisyDlf(filnavn)
    df=harvest.Data
    # summere og plot af udbytte i tørstof DM       
    harv_grain = df[['crop', 'sorg_'+output]]
    harv_grass = df[['crop', 'leaf_'+output, 'stem_'+output,'sorg_'+output]]
    grain =harv_grain.groupby('crop')
    cereal = grain.get_group(crop_name).sum(axis=1)
    return(cereal)

outpu = 'DM'
rg=extract(Ryegrass, DailyP-harvest.dlf, output)

#rg=extract(crop_name='Ryegrass', os.path.join(root, d, "DailyP-harvest.dlf"), output)
"""