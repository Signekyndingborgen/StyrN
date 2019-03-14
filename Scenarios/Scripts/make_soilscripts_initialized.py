# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:22:26 2019

@author: tqc268

Script that reads C roots and C input values from the spin-up simulations and puts it into soil tiles

"""
import sys
import os
import pandas as pd
sys.path.insert(0,r'./../pydaisy/')
from pydaisy.Daisy import DaisyModel, DaisyEntry, DaisyDlf

from dateutil.relativedelta import relativedelta
from Create_rotations2 import split_unique_name




def getitem(name_entries, init):
    for k, v in init.items():
        names = split_unique_name(k)
#        if names['Weather']==name_entries['Weather']:
        #if names['SoilType']==name_entries['SoilType']:
        return v




path=r'../Run'  
MotherFolder=r'..\Run'
items = os.walk(MotherFolder)
index=1
init = {}  
for root, dirs, filenames in items:
    for d in dirs:
        C_inital=DaisyDlf(os.path.join(root, d, "DailyP-SC80-M.dlf"))
        initialValues={}
        df=C_inital.Data
        diff_years = relativedelta(df.index[len(df)-1], df.index[0]).years+1
        #print(diff_years)
        inputC = int((df['Residuals_C_top'].sum(axis = 0)+df['Residuals_C_root'].sum(axis = 0) + df['Fertilizer_C'].sum(axis = 0)-df['Bioinc_C-Soil'].sum(axis = 0))/diff_years)
        roots = int(df['Residuals_C_root'].sum(axis = 0)/diff_years)
        fertilizerC = int(df['Fertilizer_C'].sum(axis =0)/diff_years)
        initialValues = [inputC, roots, fertilizerC] 
        init[d]= initialValues    
for key, value in init.items:
    name_entries = split_unique_name(key)    
    if name_entries['IsConventional'] and name_entries['ManureMass']!=230:
        init2 = init.values()
        
#for key, value in init.items():
#    name_entries = split_unique_name(key)    
#    if name_entries['IsConventional'] and name_entries['ManureMass']!=230:
#        init2 = [key, [value]
        
#items = os.walk(r'../RunSpinUp3')
#for root, dirs, filenames in items:
#    for d in dirs:    
#        template = DaisyModel(os.path.join(root, d, 'model.dai'))   
#        name_entries = split_unique_name(d)    
#        item = getitem(name_entries, init)
#        print(item)



#newfile= template.copy()    
#block = newfile.Input['defcolumn']['OrganicMatter'][0]

#OrgMatter = DaisyEntry('OrganicMatter',[])
#OrgMatter.Children.append(DaisyEntry('init + str(init['t'][i] +','[kg N/ha/y]'])
#OrgMatter.Children.append(DaisyEntry('equivalent_weight',[ str(df['amount'][i]) , '[kg N/ha]']))
#block.Children.append(OrgMatter)