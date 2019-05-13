# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:24:43 2019

@author: tqc268
"""
import sys
import pandas as pd
import os
sys.path.insert(0,r'../../pydaisy/')
from datetime import datetime
from pydaisy.Daisy import DaisyDlf
import numpy as np
grain = ['SB', 'Winter Wheat JG','Vinterbyg','Rug','Winter Rape PA','Spring Wheat', 'Rug', 'Froegraes', 'Potato SavaFigaro','Sugar Beet','Pea', 'Potato; FertOrgaNic']
silo = ['Ryegrass', 'Wclover', 'Silomajs', 'SB-green', 'Graes'] 

def get_allYields(path):
    items = os.walk(path)
    allresults={}
    
    for root, dirs, filenames in items:
        for d in dirs:
            cropyield={}            
            if os.path.isfile(os.path.join(root, d, "harvest.dlf")):
                harvest=DaisyDlf(os.path.join(root, d, "harvest.dlf"))
                df=harvest.Data
                DNarv= df[['crop', 'leaf_N', 'stem_N','sorg_N']]
                DMS =DMharv.groupby('crop')
                for cropname in silo:
                    if cropname in DMS.groups.keys():
                        rg = DMS.get_group(cropname).sum(axis=1)
                        cropyield[cropname]= list(rg.resample('Y').sum())
                        
                DMharvG= df[['crop', 'sorg_DM']]
                DMG =DMharvG.groupby('crop')
                
                for cropname in grain:
                    if cropname in DMG.groups.keys():
                        gr = DMG.get_group(cropname).sum(axis=1)
                        cropyield[cropname]= list(gr.resample('Y').sum())
                allresults[d]=cropyield
        #average = round(v[v!=0].mean(), 2)
        #result.append({k:average})                     
        return(allresults)