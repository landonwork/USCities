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

def join_by_col(df1,df2,col1,col2):
    df1 = df1.set_index(col1)
    df2 = df2.set_index(col2)
    new_df = pd.concat([df1,df2],axis=1)
    return new_df

def join_counties():
    pwd = 'C:/Users/lando/Desktop/Python/City Data/'

    city_nums = pd.read_csv(pwd+'all_nums.csv').set_index(['state','city']).drop_duplicates()
    
    counties = pd.read_csv(pwd+'us_cities_counties.csv')
    counties = counties[['city','state_id','state_name','county_name','lat','lng']].drop_duplicates()
    counties = counties.set_index(['state_name','city'])
    
    joined = pd.concat([city_nums,counties],axis=1)
    joined = joined.dropna(axis=0,subset = ['county_name','total_population'])
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