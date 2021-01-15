# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:28:38 2020

@author: lando
"""

url = 'http://www.city-data.com/'
start_state = 'Colorado'

import scrape_tools as st
from datetime import datetime
from datetime import timedelta
from time import sleep
import pandas as pd
import re

request_log = []
make_soup = st.log_request(st.make_soup,request_log)
ping = st.log_request(st.ping,request_log)
get_cities = st.log_request(st.get_cities,request_log)
scrape_city = st.log_request(st.scrape_city,request_log)
# You cannot reassign request_log after this point
# If you do, run these four lines again

print("Gathering state links")
#####################################################################
html_soup = make_soup(url)
html_soup = html_soup.findAll('div',{'id': 'home1'})[0]

links = []
switch = False
for state in html_soup.findAll('a'):
    if state.text == start_state:
        switch = True
    if switch:
        links.append(state['href'])

links.remove('http://www.city-data.com/city/District-of-Columbia.html')
links.remove('http://www.city-data.com/smallTowns.html')
#####################################################################

print('Collecting city names by state')
#####################################################################
all_cities = {}
for link in links:
    get_state = re.compile('/city/(?P<state>.*)\.html')
    state_match = get_state.search(link)
    all_cities.update({state_match.group('state'): get_cities(link)})
#####################################################################

print('Scraping and storing city data')
#####################################################################
li = open('var_settings.txt','r').readlines()[0].split(', ')
min_forget = float(li[0])
forget_margin = float(li[1])
max_forget = min_forget + forget_margin
min_forgive = float(li[2])
max_forgive = float(li[3])
forgive_guess = float(li[4])
# f = open('var_settings.txt','w')
# s = [min_forget,max_forget,min_forgive,max_forgive,forgive_guess]
# f.write(str(s)[1:-1])
n = 1
for state in all_cities.keys():
    state_df = pd.DataFrame()
    print(f"Scraping {state.replace('-',' ')} cities:")
    for city in all_cities[state]:
        if len(request_log) >= 950:
            time_since = datetime.now()-request_log[-950]
            if time_since < timedelta(hours=min_forget):
                wait_time = (timedelta(hours=max_forget)-time_since).total_seconds()+60.
                a = datetime.now()
                print(f"Will resume scraping at {(a+timedelta(seconds=wait_time)).hour}:{(a+timedelta(seconds=wait_time)).minute}")
                sleep(wait_time)
        if (city == 'Santa Margarita') & (state == 'California'):
            continue
        print(n, f"{city}, {state.replace('-',' ')}")
        city_url = url + f"city/{city.replace(' ','-')}-{state}.html"
        city_data = {'state':state.replace('-',' '),'city':[city]}
        while True:
            addition = scrape_city(city_url)
            if addition is bool: # If the server ignored me
                min_forget = max(min_forget,(datetime.now()-request_log[-998]).total_seconds()/3600.)
                max_forget = min_forget+forget_margin
                print(f"Setting minimum forget time to {min_forget:.01f} hours")
                min_forgive, max_forgive, pings = st.repent(min_forgive,max_forgive,forgive_guess,url)
                forgive_guess = (min_forgive+max_forgive)/2
                request_log.extend(pings)
            else:
                break
        city_data.update(addition)
        city_df = pd.DataFrame.from_dict(city_data)
        state_df = pd.concat([state_df,city_df])
        n += 1
    
    filename = 'C:/Users/lando/Desktop/Python/City Data/'+state+'-cities.xlsx'
    state_df.to_excel(filename,sheet_name='Unabridged')
    print(state.replace('-',' ') + ' cities written to Excel file')
#####################################################################

print('All done. Time to party!')