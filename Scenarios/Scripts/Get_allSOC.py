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

# Calculates the pool changes by summing all daisy pools SOM+AOM+SMB as: end - start / yrs


path = r'../Run3'
def get_allSOM(path):
    items = os.walk(path)
    allSOMresults={}
    
    for root, dirs, filenames in items:
        for d in dirs:
            cropyield={}            
            if os.path.isfile(os.path.join(root, d, "Annual-OM.dlf")):
                anOM = DaisyDlf(os.path.join(root, d, "Annual-OM.dlf"))
                df=anOM.Data
                filter_colC = [col for col in df if col.endswith('-C')]
                SOC_col = df[filter_colC].sum(axis = 1)
                dSOC = round( (SOC_col[len(SOC_col)-1]-SOC_col[1]) / (len(SOC_col)-1), 2)
                filter_colN = [col for col in df if col.endswith('-N')]
                SON_col = df[filter_colN].sum(axis = 1)
                dSON = round((SON_col[len(SON_col)-1]-SON_col[1]) / (len(SON_col)-1), 2)
                allSOMresults[d] = [dSON] 
          
        return(allSOMresults)
    