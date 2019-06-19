# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:36:40 2019

@author: tqc268

"""
import sys
import pandas as pd
import os
sys.path.insert(0,r'../../pydaisy/')
from datetime import datetime
import shutil
from pydaisy.Daisy import DaisyModel, DaisyEntry
from fertil import CalcFertil
from DaisyWaitBlock import DaisyWaitBlock
from pydaisy.Daisy import *
from split_nameDir import split_unique_nameSpin
from split_nameDir import split_unique_name
from get_SOMspinup import getSOMspinup

def get_unique_name(NameDictionary):
    return NameDictionary['Rotation'] + '_' + str(NameDictionary['ManureMass']) +'_' + str(NameDictionary['IsConventional']) +'_'+ str(NameDictionary['Soiltype'])+ '_'+ str(NameDictionary['Weather'])+ '_'+str(NameDictionary['Initlevel'])

xlfile = '../common/masterinput_v7.xlsx'

path=r'../RunK2-7'
def write_columns(path):
    init = getSOMspinup(r'../RunSpinup5')
    initlevels = ['High', 'Medium', 'Low']
    
    rota = pd.DataFrame(pd.read_excel(xlfile,sheet_name= 'RotationsK'))
    rota.index = rota['ID']
    crops = pd.read_excel(xlfile,sheet_name= 'Crops')
    crops.index = crops['Crop']
    cropsJB6 = pd.read_excel(xlfile,sheet_name= 'Crops_JB6')
    cropsJB6.index = crops['Crop']
    manure = pd.read_excel(xlfile, sheet_name= 'Manure')
    manure.index = manure['ID']
    SoilClimate = pd.read_excel(xlfile, sheet_name= 'soil_climate', header = 0)
    
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)
        except:
            pass
    if not os.path.isdir(path):
        os.makedirs(path)
    template = DaisyModel(os.path.join(path, '../Common/Scenarier_v7.dai'))
    template2 = DaisyModel(os.path.join(path, '../Common/Def_columns.dai'))   # SoilJB1_4_5_OM.dai
    weather = SoilClimate['Climate'][0:2].tolist()
    
    for il in initlevels:
        
        for w in weather:
    
            for s in range (0, 9):
                soil = SoilClimate['Soiltype'][s]
    
                for i in range(3, 9):
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
                        block = newfile.Input['defaction']
                        LastYearCropID = int(crops['afgkode1'][rota[rotation][maxnumberyear].strip()])
                        #Loop the years
                        for year in range(1, maxnumberyear+1):
                            cropname = rota[rotation][year].strip()
                            crop_ID = int(crops['afgkode1'][cropname])
    
                            ThisYearsEntries=[]
    #Plowing
                            if soil[0:3]=='JB6':
                                if not pd.isna(cropsJB6['Plowing'][cropname]):
                                    ThisYearsEntries.append(DaisyWaitBlock(cropsJB6['Plowing'][cropname]))
                                    ThisYearsEntries[-1].EntriesAfterWait.append(DaisyEntry('plowing',[]))
                                
                            else:
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
      #Harvest
                            HarvestNumbers=[]
                            if not pd.isna(crops['Harvest1'][cropname]):
                                HarvestNumbers.append('1');
                            if not pd.isna(crops['Sowing2'][cropname]) and not pd.isna(crops['Harvest2'][cropname]):
                                HarvestNumbers.append('2');
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
                                tye.append_entries(block)
                        
                        soilblock = [x for x in template2.Input['defcolumn'] if x.getvalue()=='"' + soil +'"'][0].copy()
                        newfile.Input.Children.insert(20, soilblock)
                        
                        for key, value in init.items():
                            name_entries_Spinup = split_unique_nameSpin(key)
                            if il == name_entries_Spinup['Spinup'] and name_entries_Spinup['Soiltype'] == soil and name_entries_Spinup['Weather']== w:
                               soilblock['OrganicMatter']['init']['input'].setvalue(str(init[key][0]))     
                               soilblock['OrganicMatter']['init']['root'].setvalue(str(init[key][1]))                            
                                #print(name_entries_Spinup['spinup'])
                                #newfile.Input['def]
                        newfile.Input['column'].setvalue('"'+ soil + '"')
        # Insert irrigation if soil == JB1
                        if soil[0:3] == 'JB1':
                            irrigationblock = template2.Input['defaction']
                            newfile.Input.Children.insert(22, irrigationblock)
                            newfile.Input['manager'].setvalue('(while (repeat A_F_R) (repeat irrigate_30))', 2)
                        else:
                            newfile.Input['manager'].setvalue('(repeat (A_F_R))', 2)
                        newfile.Input['weather'].setvalue('"'+ w +'"',1)
                    
                    #Now print the daisy file
                    #create unique name
                        name_entries={}
                        name_entries['Rotation']=rotation
                        name_entries['ManureMass']=int(ManureSim[1])
                        name_entries['IsConventional']=ManureSim[2]
                        name_entries['Soiltype']=soil
                        name_entries['Weather']= w
                        name_entries['Initlevel']= il
                        newfile.save_as(os.path.join(path, get_unique_name(name_entries), 'model.dai'))
if __name__ =='__main__':
    write_columns(path)
