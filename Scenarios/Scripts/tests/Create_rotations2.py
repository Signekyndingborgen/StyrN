# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:36:40 2019

@author: tqc268

Vinterbyg PE fikset!
Og slætter alle filer i Run mappen inden kørsel - og laver en ny Run mappe.
Skriver sædskifter og datoer for 1 jord-klima-init-C kombination.
"""
import sys
import pandas as pd
import os

sys.path.insert(0, r'../../../pydaisy/')
from datetime import datetime
import shutil
from pydaisy.Daisy import DaisyModel, DaisyEntry
from fertil import CalcFertil
from DaisyWaitBlock import DaisyWaitBlock
from pydaisy.Daisy import *

path=r'../Run'

def get_unique_name(NameDictionary):
    return NameDictionary['rotation'] + '_' + str(NameDictionary['ManureMass']) +'_' + str(NameDictionary['IsConventional'])

def split_unique_name(unique_name):
    splitted = unique_name.split('_')
    NameDictionary={}
    NameDictionary['rotation']=splitted[0]
    NameDictionary['ManureMass']=int(splitted[1])
    NameDictionary['IsConventional']=bool(splitted[2])
    
    return NameDictionary


def write_columns(path):

    rota = pd.DataFrame(pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Rotations'))
    rota.index = rota['ID']
    crops = pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Crops')
    crops.index = crops['Crop']
    manure = pd.read_excel('../common/masterinput_v4.xlsx',sheet_name= 'Manure1')
    manure.index = manure['ID']
    template = DaisyModel(os.path.join(path, '../Common/Scenarier_v3.dai'))   
       
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)
        except:
            pass
    if not os.path.isdir(path):
        os.makedirs(path)
    
    
    soil ='JB1'
    
    for i in range(1, 24):
        rotation=rota.columns[i]
            #find rotation length
        maxnumberyear = 6
        while pd.isna(rota[rotation][maxnumberyear]):
            maxnumberyear-=1
    
    
        #Make a list with all cropIDs. We need this in the fertilize calc
        AllCropIDs = []
        for year in range(1, maxnumberyear+1):
            cropname = rota[rotation][year].strip()
            crop_ID = int(crops['afgkode1'][cropname])
            AllCropIDs.append(crop_ID)
    
    
        #Find the different manure realisations
        ManureSims = []
        OrgKonv=['Konv', 'Øko' ]
        for t in OrgKonv:
            if not pd.isna(rota[rotation][t]):
                IsConventional=True
                ManureID = rota[rotation][t]
                ManureType = manure['Manuretype'][ManureID]
                for ManureMass in manure.loc[ManureID][2:6]:
                    if not pd.isna(ManureMass):
                        if t =='Konv':
                            ManureSims.append([ManureType, ManureMass, True])
                        else:
                            ManureSims.append([ManureType, ManureMass, False])
    
        print(rotation)
    
        #Loop the manure realisations
        for ManureSim in ManureSims:
            newfile= template.copy()
            block = newfile.Input['defaction'][0]
            LastYearCropID = int(crops['afgkode1'][rota[rotation][maxnumberyear].strip()])
    
            #Loop the years
            for year in range(1, maxnumberyear+1):
                cropname = rota[rotation][year].strip()
                crop_ID = int(crops['afgkode1'][cropname])
    
                ThisYearsEntries=[]
    
                #Plowing
                if not pd.isna(crops['Plowing'][cropname]):
                    ThisYearsEntries.append(DaisyWaitBlock(crops['Plowing'][cropname]))
                    ThisYearsEntries[-1].EntriesAfterWait.append(DaisyEntry('plowing',[]))
    
                #Sowing
                if not pd.isna(crops['Sowing1'][cropname]):
                    ThisYearsEntries.append(DaisyWaitBlock(crops['Sowing1'][cropname]))
                    for c in crops['Daisynavn1'][cropname].split(','):
                        ThisYearsEntries[-1].EntriesAfterWait.append(DaisyEntry('sow', ['"' + str(c.strip()) +'"']))
                if not pd.isna(crops['Sowing2'][cropname]):
                    if str(crops['Sowing2'][cropname]) < str(crops['Harvest1'][cropname]):
                        ThisYearsEntries.append(DaisyWaitBlock(crops['Sowing2'][cropname]))
                        for c in crops['Daisynavn2'][cropname].split(','):
                            ThisYearsEntries[-1].EntriesAfterWait.append(DaisyEntry('sow', ['"' + str(c.strip()) +'"']))
    
                #Fertilize
                man=CalcFertil(crop_ID, LastYearCropID, soil, AllCropIDs, ManureSim[0], ManureSim[1], ManureSim[2])
                LastYearCropID=crop_ID
                print(man)
                # Hvis der er gylle:
                if ManureSim[1]!=0.0:
                    ThisYearsEntries.append(DaisyWaitBlock(crops['FDate1'][cropname]))
                    fert = DaisyEntry('fertilize',[])
                    fert.Children.append(DaisyEntry('"' + ManureSim[0] +'"',[]))
                    fert.Children.append(DaisyEntry('equivalent_weight',[ str(man[0]) , '[kg N/ha]']))
                    ThisYearsEntries[-1].EntriesAfterWait.append(fert)
                if ManureSim[2]:
                    #if man
                    Fertilizerdates= []
                    for fdc in range(1,5):
                        if not pd.isna(crops['FDate' + str(fdc)][cropname]):
                            Fertilizerdates.append(crops['FDate' + str(fdc)][cropname])
    
                    for fdate in Fertilizerdates:
                        ThisYearsEntries.append(DaisyWaitBlock(fdate))
                        fert = DaisyEntry('fertilize',[])
                        fert.Children.append(DaisyEntry('"'+'NPK01'+'"',[]))
                        fert.Children.append(DaisyEntry('equivalent_weight',[ str(man[1]/len(Fertilizerdates)), '[kg N/ha]']))
                        ThisYearsEntries[-1].EntriesAfterWait.append(fert)
    
                HarvestNumbers=[]
                if not pd.isna(crops['Harvest1'][cropname]):
                    HarvestNumbers.append('1');
                if not pd.isna(crops['Sowing2'][cropname]) and not pd.isna(crops['Harvest2'][cropname]):
                    HarvestNumbers.append('2');
    
    
                #Harvest
                for hn in HarvestNumbers:
                    harvestdates=[]
                    if isinstance(crops['Harvest'+hn][cropname], datetime):
                        harvestdates.append(crops['Harvest'+hn][cropname])
                    else:
                        for s in crops['Harvest'+hn][cropname].split(','):
                            harvestdates.append(datetime(2019, int(s.split('/')[1]), int(s.split('/')[0])))
                    for date in harvestdates:
                        ThisYearsEntries.append(DaisyWaitBlock(date))
                        for c in crops['Daisynavn'+hn][cropname].split(','):
                            harvest = DaisyEntry('harvest', ['"' + str(c.strip()) +'"'])
                            harvest.Children.append(DaisyEntry(crops['HarvestHow'+hn][cropname], []))
                            ThisYearsEntries[-1].EntriesAfterWait.append(harvest)
    
                #Catch crops
                if not pd.isna(crops['Sowing2'][cropname]):
                    if str(crops['Harvest1'][cropname]) < str(crops['Sowing2'][cropname]):
                        ThisYearsEntries.append(DaisyWaitBlock(crops['Sowing2'][cropname]))
                        ThisYearsEntries[-1].EntriesAfterWait.append(DaisyEntry('plowing', []))
                        for c in crops['Daisynavn2'][cropname].split(','):
                            ThisYearsEntries[-1].EntriesAfterWait.append(DaisyEntry('sow', ['"' + str(c.strip()) +'"']))
    
    
                ThisYearsEntries.sort(key = lambda t:t.waitdate)
                for tye in ThisYearsEntries:
                    tye.append_entries(block);
    
            #Now print the daisy file
            #create unique name
            name_entries={}
            name_entries['rotation']=rotation
            name_entries['ManureMass']=int(ManureSim[1])
            name_entries['IsConventional']=ManureSim[2]
            newfile.save_as(os.path.join(path, get_unique_name(name_entries), 'model.dai'))
# write_columns(path)