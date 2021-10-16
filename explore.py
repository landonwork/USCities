# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 11:44:01 2021

@author: lando
"""

import pandas as pd

df = pd.read_csv('C:/Users/lando/Desktop/Python/City Data/all_nums.csv')

def search_city(s:str,df):
    return df[['city','state','total_population']].loc[df['city'].str.contains(s)]
    
def look_city(s:str,df):
    df = df.set_index(['state','city'])
    city, state = tuple(s.split(', '))
    return df.loc[state].loc[city]

a = df['total_population'] > 45000
midsize = df.loc[a]