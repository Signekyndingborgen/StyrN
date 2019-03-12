# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:22:26 2019

@author: tqc268

Script that reads C roots and C input values from the spin-up simulations and puts it into soil tiles

"""
import sys
import os
import pandas as pd
from dateutil.relativedelta import relativedelta

path=r'../RunSpinUp'  
MotherFolder=r'..\RunSpinUp'
items = os.walk(MotherFolder)
index=1
init = {}  
for root, dirs, filenames in items:
    for d in dirs:
        C_inital=DaisyDlf(os.path.join(root, d, "DailyP-SC80-M.dlf"))
        initialValues={}
        df=C_inital.Data
        diff_years = relativedelta( df.index[len(df)-1], df.index[0]).years

        inputC = int(df['CLeaf'].sum(axis = 0)/diff_years)
        roots = int(df['Residuals_C_root'].sum(axis = 0)/diff_years)
        initialValues = [inputC, roots] 
        init[d]= initialValues


#pathin = r'../Run3'
#template = DaisyModel(os.path.join(path, '../Common/Soils_3test.dai'))   
        
#newfile= template.copy()    
#block = newfile.Input['defcolumn']['OrganicMatter'][0]

#OrgMatter = DaisyEntry('OrganicMatter',[])
#OrgMatter.Children.append(DaisyEntry('init + str(init['t'][i] +','[kg N/ha/y]'])
#OrgMatter.Children.append(DaisyEntry('equivalent_weight',[ str(df['amount'][i]) , '[kg N/ha]']))
#block.Children.append(OrgMatter)