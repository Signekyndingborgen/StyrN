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

from split_nameDir import split_unique_nameSpin
from get_SOMspinup import getSOMspinup
import numpy as np
init = getSOMspinup(r'../RunSpinUp5')


High = [v for k,v in init.items() if split_unique_nameSpin(k)['Spinup'] =='High']
Med = [v for k,v in init.items() if split_unique_nameSpin(k)['Spinup'] =='Medium']
Low = [v for k,v in init.items() if split_unique_nameSpin(k)['Spinup'] =='Low']

print(np.mean([item[1] for item in High]))
print(np.mean([item[1] for item in Med]))
print(np.mean([item[1] for item in Low]))
