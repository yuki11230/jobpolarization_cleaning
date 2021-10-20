# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 17:58:02 2021

@author: sxiao
This code ranked the employament share ranked by 1980 cencus wage and occ1990 (occ1990dd_share_pivot_ranked.csv)
/ or just occ1990 (occ1990dd_share_pivot.csv)

"""

import pandas as pd
#import numpy as np
df1=pd.read_csv(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ1990dd_share.csv")
df2=pd.read_csv(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ1990dd_share_200310.csv")
occ_wg=pd.read_stata(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ-means-by-decade-1980-2005-czall.dta")
occ_wg=occ_wg[['year','occ1990dd','occ_mn_wg']]
#%%
df=pd.concat([df1,df2], ignore_index=True)#2003-10 used a different occ1990 merging codes
#%% try to decide which census year to use to rank occ by wage
# we have four cencus year: 1980, 1990, 2000, 2005
# print(len(occ_wg[occ_wg['year']==1980]['occ1990dd'].unique()))
# print(len(occ_wg[occ_wg['year']==1990]['occ1990dd'].unique()))
# print(len(occ_wg[occ_wg['year']==2000]['occ1990dd'].unique()))
# print(len(occ_wg[occ_wg['year']==2005]['occ1990dd'].unique()))
# all of the above return 323 
#print(len(cw['occ1990dd'].unique())) # returns 331
#%%
#a=np.array_equal(occ_wage[occ_wage['year']==1980]['occ1990dd'].unique(),occ_wage[occ_wage['year']==1990]['occ1990dd'].unique()) # False
#a=np.array_equal(occ_wage[occ_wage['year']==1990]['occ1990dd'].unique(),occ_wage[occ_wage['year']==2000]['occ1990dd'].unique()) # False
print(len(df['occ1990dd'].unique())) #returns 323 occupations
#%% first add mean wage of census 1980 to all occupations, then sort the data by year quarter meanwage
occ_wg_80=occ_wg[occ_wg['year']==1980]
dff=pd.merge(df,occ_wg_80,left_on='occ1990dd',right_on='occ1990dd',how='left')# use left join to make sure all occ1990 are recoded
#%% check missing values
dff['occ_mn_wg'].isnull().sum()
df1 = dff[dff.isna().any(axis=1)]# return 24 nan values with the following occ1990dd code
# 473 479 488 489 496 498  all come from farming occupations 
#%% keep only needed variables and create DATE column
dff=dff[['YEAR','quarter','occ1990dd','occ_mn_wg','share']]
dff=dff.sort_values(by=['YEAR','quarter','occ_mn_wg'])
dff['DATE']=df['YEAR'].astype(str)+"q"+df['quarter'].astype(str)
#%% time series data of emp share by occupation with mean hourly wage 
dff.to_csv('.\occ1990dd_share_mnwg_ts.csv',index=False)
#%% only keep year>1982 due to missing values
#we did not use data from year1976-1982 because out of 320 occ 61 occupations 
#are not coded in the cencus 1970.
dff=dff[dff['YEAR']>1982]
#%% create cross-sectional data 
df_re=dff[['DATE','occ1990dd','share','occ_mn_wg']]
# rank by 1980 cencus wage and occ1990
df_reshape=df_re.pivot(index='DATE',columns=['occ_mn_wg','occ1990dd'],values='share')
# rank by occ1990 only
# df_reshape=df_re.pivot(index='DATE',columns=['occ1990dd'],values='share')
#%%
#df.to_csv('.\occ1990dd_share_mnwg_pivot_raw.csv',index=False)
#%%
#Missing values, make sure OCC OCC1990DD does not have any missing values
missing_data=df_reshape.isnull()
for column in missing_data.columns:
    print(column)
    print(missing_data[column].value_counts())
    print("") 
    #(occ, missing values true): 533,1; 583,35;594,4;655,6; 645,34;649,1;653,34;684,34;707,4
    #88, 30; 235,35;713,34
#%% 
# check how many columns(occupations) of occ1990dd are missing from 1976 to 1982
print(df_reshape.iloc[0,:].isnull().sum())# returns 64
#%%
df_reshape.to_csv('.\occ1990dd_share_pivot_ranked_wg.csv')# rank by 1980 cencus wage and occ1990
#df_reshape.to_csv('.\occ1990dd_share_pivot.csv')# rank by occ1990 only