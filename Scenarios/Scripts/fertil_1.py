import pandas as pd

norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Sheet1")
norm.index = norm['afgkode']

def CalcFertil(crop_ID, LastYearCropID, soil, AllCropIDs, ManureType, ManureMass, IsConventional):
    norm_crop = norm['norm_'+soil[0:3]][crop_ID]
    forfrugt=0
    if norm['Ja/Nej'][crop_ID]==1:
        forfrugt = norm['Forfrugt'][LastYearCropID]
    SumNorm=0
    for i in range(0,len(AllCropIDs)):
        SumNorm+=norm['norm_'+soil[0:3]][AllCropIDs[i]]
        if norm['Ja/Nej'][AllCropIDs[i]]==1:
            lastyear=i-1
            if i==0:
                lastyear=len(AllCropIDs)-1
            SumNorm-=norm['Forfrugt'][AllCropIDs[lastyear]] 
    weight =len(AllCropIDs)*(norm_crop - forfrugt)/SumNorm
    
    #Mass of nitrogen depends on type of manure. We just apply it on the the already calculated weight
    if ManureType =='kvaeg_gylle':
        weight = 0.7 * weight
    elif ManureType == 'slagtesvin_gylle':
        weight = 0.75 * weight
    elif ManureType == 'kvaeg_dybstroelse':
        weight = 0.45 * weight
        
    GylleN = round(weight*ManureMass)
    MineralN=0
    #In conventional we apply Mineral N to fulfill the norm
    if IsConventional:
        MineralN = norm_crop - GylleN
    return [GylleN, MineralN]
    
  