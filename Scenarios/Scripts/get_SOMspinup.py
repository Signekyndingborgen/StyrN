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
from Create_rotations_spinup import split_unique_name

def getSOMspinup(path):
   
    #path=r'../RunSpinup5'  
    
    MotherFolder= path #r'..\RunSpinup5'
    items = os.walk(MotherFolder)
    index=1
    init = {}  
    for root, dirs, filenames in items:
        for d in dirs:
            C_inital=DaisyDlf(os.path.join(root, d, "SC100-M.dlf"))
            initialValues={}
            df=C_inital.Data
            diff_years = relativedelta(df.index[len(df)-1], df.index[0]).years+1
            #print(diff_years)
            inputC = int((df['Residuals_C_top'].sum(axis=0)+df['Residuals_C_root'].sum(axis = 0) + df['Fertilizer_C'].sum(axis = 0)-df['Bioinc_C-Soil'].sum(axis = 0))/diff_years)
            roots = int(df['Residuals_C_root'].sum(axis=0)/diff_years)
            fertilizerC = int(df['Fertilizer_C'].sum(axis=0)/diff_years)
            initialValues = [inputC, roots, fertilizerC] 
            init[d]= initialValues    
        
        return init
