# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:10:58 2019

@author: tqc268
"""

df = hierDf.reset_index()
dfnp = np.asarray(df_crop)
mean = df.groupby(['SoilType', 'Crop']).mean()
df_crop['clovergrass'] = float(dfnp['Yield_Ryegrass']) + float(dfnp['Yield_Wclover'])
             
             
df2=df.groupby(['SoilType', 'Crop']).agg({'Yield': 'mean'})
df1 = df.loc[3, ]

df_soil = dfH.unstack('SoilType')
#df_crop = dfH2.unstack('Crop')

hierDf.apply(pd.to_numeric) 

df3 = df_crop.copy()


df2 = dfH.xs(('170', 'Medium'), level=['ManureMass', 'InitLevel'], drop_level=False).copy()  # .copy() is to avoid SettingwithCopyWarning
df2.columns = df2.columns.get_level_values(0)
df_crop.columns = ['_'.join(col) for col in df_crop.columns.values]

cg = df_crop.loc[( ['JB1med'], ['Yield_Ryegrass', 'Yield_Wclover'] ), : ]
cg = df_crop.loc[(slice(None), ['JB1med', 'JB1low']), :]
#df_crop.update(df_crop.apply(pd.to_numeric, errors='coerce'))
#df_crop.groupby(level=['SoilType']).mean().dropna()

mean = df_crop[np.asarray(df_crop)

crop2 = np.asarray(df_crop.reset_index())

mean = crop2.groupby(['SoilType']).mean()

#data_mean = hierDf.mean(level='SoilType')
df_soil
# matplot lib
df_soil.unstack(level=5).plot(kind='bar', subplots=True)
df_crop= dfH.unstack('Crop')
mean= np.asarray(df_crop).mean(axis = 1)

# Virker ikke
#idx = pd.IndexSlice
#hierDf_T170 = hierDf.loc[idx[:, ', :, 'True', :, :, 'Medium']]
#hierDF_mean = hierDf.mean(axis=1, level ='Crop')

df_crop.index