# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 16:53:50 2021

@author: sxiao
"""
import pandas as pd
#import numpy as np
df=pd.read_csv(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\cps_00033.csv")
cw70=pd.read_stata(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ1970_occ1990dd.dta")
cw80=pd.read_stata(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ1980_occ1990dd.dta")
cw90=pd.read_stata(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ1990_occ1990dd.dta")
#cw00=pd.read_stata(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\occ2000_occ1990dd.dta")
#rpc_occ=pd.read_csv(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\02_project3_occ_data_occ\cencus2000_1pct_5pct.csv")
#%%
#devide the dataset into two
df=df[df['YEAR']<2003]
#%%
#restrict only to working age population 
#GK uses ages 16 and above; ZBZ uses ages 15-64
df=df[df['AGE']>=16]
# drop military OCC1990=905, NIU occ1990=999
df=df.drop(df[df['OCC1990']==905].index)
df=df.drop(df[df['OCC1990']==999].index)
#print(df['EMPSTAT'].value_counts())# the results show it will also include people who are unemployed and not in the labor force
# need to decide whether to keep only the people who are employed or not
#%%
#GK uses employment level\share, ZBZ uses both employed and unemployed.
# we will work with employment level
df=df[(df['EMPSTAT']==10)|(df['EMPSTAT']==12)]
#print(df['EMPSTAT'].value_counts())
#10    548472
#12     25691
#Name: EMPSTAT, dtype: int64
#%%
#Missing values
# missing_data=df.isnull()
# for column in missing_data.columns:
#     print(column)
#     print(missing_data[column].value_counts())
#     print("")  
#%%
#for year 1972-1982,use cw70.for year 1983-1991,use cw80. for year 1992-2002,use cw90 #for year 2003-2010,use cw00
#see https://cps.ipums.org/cps-action/variables/OCC#comparability_section
#creat a column as merging key
# write a function returns cencus code based on previous lines
def get_ces(df):
    if 1976<=df['YEAR']<=1982:
        return 70
    elif 1983<=df['YEAR']<=1991:
        return 80
    elif 1992<=df['YEAR']<=2002:
        return 90
    #elif 2003<=df['YEAR']:
    #elif 2003<=df['YEAR']<=2010:
       # return 2000    
df['CES']=df.apply(get_ces, axis = 1)
#%% for year >= 2003
#df.replace(rpc_occ['1pct'],rpc_occ['5pct'])
#%%
#adjust the occ for cw00
#cw00['occ']=cw00['occ']*10
cw70['CES']=70
cw80['CES']=80
cw90['CES']=90
#cw00['CES']=2000
cw=pd.concat([cw70,cw80,cw90], ignore_index=True)
cw=cw.sort_values(by=['CES','occ'])
#cw00=cw00.sort_values(by=['occ'])
#%%
# merge occ1990 with the crosswalk
# firt sort by occ1990
df=df.sort_values(by=['YEAR','OCC'])
df=pd.merge(df,cw,left_on=['CES','OCC'],right_on=['CES','occ'],how= 'left')# use left join to make sure all occ1990 are recoded
#df=pd.merge(df,cw90,left_on=['OCC1990'],right_on=['occ'],how= 'left')# use left join to make sure all occ1990 are recoded
# check no. of occ for CPS 'OCC1990' and cw 'occ'. here we have not dropped farm occupations yet
# df OCC1990 returns 383 ,cw. occ returns 502, cw. occ1990dd returns 331
# use left join will produce missing values 

#%%
# print(len(df['OCC1990'].unique()))
# print(len(cw['occ'].unique()))
# print(len(cw['occ1990dd'].unique()))
# item=df['OCC1990'].unique()
# z=cw['occ'].unique()
# for element in item:
#     if element not in z:
#         print(element)
# #return 349
df_na=df[df['occ'].isnull()]# it turns out all of them has OCC1990=349
print(df_na['OCC'].unique())
#df_ck=df_na[df['YEAR']==2003]
#%%
# drop the occupations in farming
#  Autor and Dorn(2013) produces figure 1 by using 318 nonfarm occupations, so we need to drop farming occ
#based on the disserataion Appendix of Dorn , occ1990dd 473-498 is farming 
df=df[(df['occ1990dd']<473)|(df['occ1990dd']>498)]
#%%
#Missing values, make sure OCC OCC1990DD does not have any missing values
missing_data=df.isnull()
for column in missing_data.columns:
    print(column)
    print(missing_data[column].value_counts())
    print("") 
#%%
# double check if the occ1990 is matched to occ1990dd
#print(df['OCC1990'].unique())
#print(cw['occ'].unique())
df_check=df[df['OCC1990']==17]
#%% keep only the variables we need
df=df[['YEAR','MONTH','occ1990dd','WTFINL']]
#%% 
#save raw data
df.to_csv('.\occ1990dd_raw.csv',index=False)
#%%
#compute employment share with cps weights
# calculate the total weight by occ1990dd, year, month
df=df.sort_values(by=['YEAR','MONTH','occ1990dd'])
df_temp= df.groupby(['YEAR', 'MONTH','occ1990dd'], as_index=False)
df['occwt']=df_temp['WTFINL'].transform(lambda x:x.sum() )
#%%
# calculate the total weight by occ1990dd, year, month
df_temp= df.groupby(['YEAR', 'MONTH'], as_index=False)
df['totalwt']=df_temp['WTFINL'].transform(lambda x:x.sum() )
df['share']=df['occwt']/df['totalwt'] #employment share for each occ,month, year
#%% keep only the variables we need
df=df[['YEAR','MONTH','occ1990dd','share']]
#%% remove duplicates
df= df.drop_duplicates()
#%% aggareagte to quarterly data by taking quarterly averages, do not use monthly
df['DATE']=pd.to_datetime(df['YEAR'].astype(str)+df['MONTH'].astype(str), format='%Y%m')
df['quarter'] = df['DATE'].dt.quarter
dff=df.groupby(['YEAR','quarter','occ1990dd'], as_index=False)['share'].mean()
dff['share']=dff['share']*100
#%%
dff.to_csv('.\occ1990dd_share.csv',index=False)
#%%rank occ1990dd by median wage of cencus 1990
# see occ_01.py
#%% deseasonalize in R 