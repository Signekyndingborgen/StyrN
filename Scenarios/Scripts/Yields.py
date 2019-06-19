# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:44:20 2019

@author: tqc268
"""
# Script take allresults (yields) from Daisy files and takes the mean yield per crop for each key

import sys
import pandas as pd
sys.path.append(r'../../../pydaisy')
from split_nameDir import split_unique_name
#from Get_allyields import get_allYields
import numpy as np 
import operator 
from functools import reduce


#path = r'../Run3'
#allresults = get_allYields(path)

def meanyields(allresults):
    
    for key, value in allresults.items():   
        for kl, vl in value.items():
            vl =np.asarray(vl)
            allresults[key][kl] = np.mean(vl [vl !=0])
    return(allresults)
    
    