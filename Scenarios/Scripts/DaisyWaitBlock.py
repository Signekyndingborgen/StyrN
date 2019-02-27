# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:09:03 2019

@author: jpq949
"""

from pydaisy.Daisy import DaisyEntry

class DaisyWaitBlock(object):
    def __init__(self, date):
        self.EntriesAfterWait=[]
        self.waitdate = date
        
    def append_entries(self, daisy_entry):
        daisy_entry.Children.append(DaisyEntry('wait_mm_dd', [self.waitdate.strftime('%m %d')]))
        daisy_entry.Children.extend(self.EntriesAfterWait)
        