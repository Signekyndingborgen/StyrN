# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:30:49 2019

@author: tqc268
"""

def split_unique_name(unique_name):
    splitted = unique_name.split('_')
    NameDictionary={}
    NameDictionary['Rotation']=splitted[0]
    NameDictionary['ManureMass']=int(splitted[1])
    NameDictionary['IsConventional']=splitted[2]
    NameDictionary['Soiltype']=splitted[3]
    NameDictionary['Weather']=splitted[4]
    NameDictionary['Initlevel']=splitted[5]

    return NameDictionary

def split_unique_nameSpin(unique_name):
    splitted = unique_name.split('_')
    NameDictionary={}
    NameDictionary['Spinup']=splitted[0]
    NameDictionary['Soiltype']=splitted[1]
    NameDictionary['Weather']=splitted[2]
    return NameDictionary