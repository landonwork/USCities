# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 09:47:51 2021

@author: lando

Simple script
Joining the state Excel sheets into one sheet
"""

import pandas as pd
import scrape_tools as st

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