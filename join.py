# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 09:47:51 2021

@author: lando

Simple script
Joining the state Excel sheets into one sheet
"""

import pandas as pd
import scrape_tools as st
import re

def retrieve_index(df,col):
    if col is list:
        names = col
    elif col is tuple:
        names = list(col)
    else:
        names = [col]
    df = df.reset_index(drop=False)
    df = df.rename({f"label_{i}":names[i] for i in range(len(names))})
    return df

def join_by_col(df1,df2,col1,col2,keep_index=True):
    df1 = df1.set_index(col1)
    df2 = df2.set_index(col2)
    new_df = pd.concat([df1,df2],axis=1)
    if not keep_index:
        new_df = retrieve_index(new_df,col1)
        
    return new_df

def join_counties():
    pwd = 'C:/Users/lando/Desktop/Python/City Data/'

    city_nums = pd.read_csv(pwd+'all-nums.csv').set_index(['state','city']).drop_duplicates()
    
    counties = pd.read_csv(pwd+'us_cities_counties.csv')
    counties = counties[['city','state_id','state_name','county_name','lat','lng']]
    counties = counties.set_index(['state_name','city'])
    
    joined = pd.concat([city_nums,counties],axis=1)
    joined = joined.dropna(axis=0,subset = ['county_name','total-population'])
    joined = joined.reset_index(drop=False)
    joined = joined.rename({'level_0':'state','level_1':'city'},axis=1)
    return joined

def join_states():
    links = st.get_states('http://www.city-data.com','Alabama')
    states = []
    for link in links:
        get_state = re.compile('/city/(?P<state>.*)\.html')
        state_match = get_state.search(link)
        states.append(state_match.group('state'))
    
    df = pd.DataFrame()
    for state in states:
        df = pd.concat([df,pd.read_excel(state+'-cities.xlsx')])
    df.to_excel('all-cities.xlsx',sheet_name = 'Unabridged')