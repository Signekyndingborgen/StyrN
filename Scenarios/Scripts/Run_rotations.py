# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:36:40 2019

@author: tqc268
"""

import sys
import os
sys.path.insert(0,r'../../pydaisy/')

from Create_rotations_spinup import write_columns, get_unique_name

from pydaisy.Daisy import DaisyModel, DaisyEntry, run_sub_folders

    
if __name__ =='__main__':
    path=r'../Run1'
    write_columns(path)
    DaisyModel.path_to_daisy_executable = r'C:\Program Files\Daisy 5.64\bin\Daisy.exe'
    run_sub_folders(os.path.abspath(path),'model.dai', NumberOfProcesses=6)