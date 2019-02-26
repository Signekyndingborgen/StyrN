import pandas as pd

norm = pd.read_excel('../common/Nnorm_2019.xlsx', sheet_name = "Ark1")
norm.index = norm['afgkode']

def CalcFertil(crop_ID, LastYearCropID, soil, AllCropIDs, ManureType, ManureMass, IsConventional):
    norm_crop = norm[soil][crop_ID]
    forfrugt=0
    if norm['Ja/Nej'][crop_ID]==1:
        forfrugt = norm['Forfrugt'][LastYearCropID]
    SumNorm=0
    for i in range(0,len(AllCropIDs)):
        SumNorm+=norm[soil][AllCropIDs[i]]
        if norm['Ja/Nej'][AllCropIDs[i]]==1:
            lastyear=i-1
            if i==0:
                lastyear=len(AllCropIDs)-1
            SumNorm-=norm['Forfrugt'][AllCropIDs[lastyear]] 
    weight =len(AllCropIDs)* (norm_crop - forfrugt)/SumNorm
    
    #Mass of nitrogen depends on type of manure. We just apply it on the the already calculated weight
        if ManureType =='Cattleslurry':
            weight = 0.7 * weight
        elif ManureType == 'Pigslurry':
            weight = 0.75 * weight
        elif ManureType == 'Cattlemanure':
            weight = 0.45 * weight
            
        GylleN = weight*ManureMass
        MineralN=0
    #In conventional we apply Mineral N to fulfill the norm
    if IsConventional:
        MineralN = norm_crop - GylleN
    return [GylleN, MineralN]
    
        
#print(CalcFertil(216, 216, 'JB 1+3', [216, 216, 216], 'Cattleslurry', 85, True))
#print(CalcFertil(216, 216, 'JB 1+3', [216, 216, 216], 'Cattleslurry', 85, False))