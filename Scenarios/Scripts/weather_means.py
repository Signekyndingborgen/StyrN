# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:19:26 2019

@author: tqc268
"""
import pandas as pd
import numpy as np
vejen = pd.read_table(r'../common/West.txt')
tåstrup = pd.read_table(r'../common/East.txt')
an_prec_West =np.mean(vejen.groupby('Year').sum())
an_prec_East =np.mean(tåstrup.groupby('Year').sum())
meanT_west = np.mean(vejen)
meanT_east = np.mean(tåstrup)
