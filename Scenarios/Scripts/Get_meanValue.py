# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:24:43 2019

@author: tqc268
"""

""
import sys
import os
import pandas as pd
sys.path.insert(0,r'./../pydaisy/')
from pydaisy.Daisy import DaisyModel, DaisyEntry, DaisyDlf

from dateutil.relativedelta import relativedelta
from Create_rotations_spinup import split_unique_name

#def getitem(name_entries, init):
#    for k, v in init.items():
#        names = split_unique_name(k)
#        return v
path=r'../RunSpinup5'  
MotherFolder=r'..\RunSpinup5'
items = os.walk(MotherFolder)
index=1
init = {}  
for root, dirs, filenames in items:
    for d in dirs:
        C_inital=DaisyDlf(os.path.join(root, d, "SC100-M.dlf"))
        initialValues={}
        df=C_inital.Data
        diff_years = relativedelta(df.index[len(df)-1], df.index[0]).years+1
        inputC = int((df['Residuals_C_top'].sum(axis=0)+df['Residuals_C_root'].sum(axis = 0) + df['Fertilizer_C'].sum(axis = 0)-df['Bioinc_C-Soil'].sum(axis = 0))/diff_years)
        roots = int(df['Residuals_C_root'].sum(axis=0)/diff_years)
        fertilizerC = int(df['Fertilizer_C'].sum(axis=0)/diff_years)
        initialValues = [inputC, roots, fertilizerC] 
        init[d]= initialValues    

keys = []
for i in range(0, len(init)):
    new_keys = list(init.keys())[i][0:1]
    #print(new_keys)
    keys[i]=new_keys
init2 = dict(zip(new_keys, list(init.values())))

for key, value in init.items:
    name_entries = split_unique_name(key)    
    if name_entries['Rotation']=='High' and name_entries['ManureMass']!=230:
        init2 = init.get(key)