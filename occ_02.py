# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:45:37 2021

@author: sxiao
"""
"""
This program compare the employment share I computed with the employment share in Autor and Dorn(2013)
"""
import pandas as pd
df=pd.read_csv(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\01_project3_occ_data\occ1990dd_share.csv")
ad_share=pd.read_stata(r"C:\Users\sxiao\OneDrive - Indiana University\FromBox\0CurrentResearch\01_project3_occ_data\occ1990dd_data2012.dta")
ad_share=ad_share[['occ1990dd','sh_empl1950','sh_empl1970','sh_empl1980','sh_empl1990','sh_empl2000','sh_empl2005']]
#%%
ad_share['sh_empl1980']=ad_share['sh_empl1980']*100
#%%
# firt sort by occ1990
df=df.sort_values(by=['occ1990dd'])
df=pd.merge(df,ad_share,left_on='occ1990dd',right_on='occ1990dd',how= 'outer')
#%%
df801=df[(df['YEAR']==1980)&(df['quarter']==1)]
df802=df[(df['YEAR']==1980)&(df['quarter']==2)]
#df803=df[(df['YEAR']==1980)&(df['quarter']==3)]
#df804=df[(df['YEAR']==1980)&(df['quarter']==4)]
#%%
import matplotlib.pyplot as plt
plt.figure();
df801['share'].plot()
df802['share'].plot()
#df803['share'].plot()
#df804['share'].plot()
df801['sh_empl1980'].plot()
