# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:14:10 2018

@author: sdf945
"""

import sys
sys.path.insert(0,r'../../pydaisy/')
from pydaisy.Daisy import *
# from Daisy import DaisyDlf, DaisyModel
import matplotlib.pyplot as plt
import numpy as np 
import datetime as datetime
import matplotlib.dates as mdates

# dlf = DaisyDlf(r'h:\Documents\StyrN\Clovergrass\Foulum\CG_1970-2000\DailyP-harvest.dlf')

#dm= DaisyModel (r'H:\Documents\StyrN\Clovergrass\Foulum\CG_1970-2000\DailyP-Ryegrass.dlf')

folder = r'C:\Users\tqc268\Desktop\Github\StyrN\Scenarios\RunKK1E\KK1E_170_True_JB4med_East.dwf_Medium'

#Diflufenican leaching
#result_cropN_day = DaisyDlf(folder+'\DailyP-Daily-CropProduction.dlf')
result_cropN_day = DaisyDlf(folder+'\Silomajs.dlf')
# sum daily values of plant N in leaf, stem and sorg
N_majs = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]
DM_majs =result_cropN_day.Data.values[:,4]+result_cropN_day.Data.values[:,6]+result_cropN_day.Data.values[:,7]

result_cropN_day = DaisyDlf(folder+'\Graes CC.dlf')
N_gras = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]
DM_gras = result_cropN_day.Data.values[:,4]+result_cropN_day.Data.values[:,6]+result_cropN_day.Data.values[:,7]

#result_cropN_day = DaisyDlf(folder+'\DailyP-SB.dlf')
#N_sb = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]

#result_cropN_day = DaisyDlf(folder+'\DailyP-SB.dlf')
#N_sb = result_cropN_day.Data.values[:,10]+result_cropN_day.Data.values[:,12]+result_cropN_day.Data.values[:,13]


lines=[]
plt.figure(figsize=(20,5))
line1, =plt.plot(result_cropN_day.Data.index, N_majs, color='purple', label='Silomajs')
line2, =plt.plot(result_cropN_day.Data.index, N_gras, color='green', label='Græs')
#line3, =plt.plot(result_cropN_day.Data.index, N_sb, color='crimson', label='Spring Barley')

lines.append(line1)
lines.append(line2)
#lines.append(line3)
   
#plt.axhline(0.01, color="red", linewidth=2, linestyle="--")
plt.legend(handles=lines, fontsize='x-large', loc=2)
plt.title('Aboveground N uptake', fontsize=20,color='black')
plt.ylabel('kg N /ha', fontsize=20)
plt.legend(handles=lines, fontsize=20)

plt.tick_params(labelsize=20, axis='both', which='major')
plt.axvline(result_dif.Data.index[174], color="red", linewidth=2)
plt.axvline(result_dif.Data.index[204], color="red", linewidth=2)
plt.xlim(left=result_dif.Data.index[173], right=result_dif.Data.index[311]) 
plt.ylim(0, 0.2)
