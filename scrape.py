# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:28:38 2020

@author: lando
"""

url = 'http://www.city-data.com/'
start_state = 'New York'

import scrape_tools as st
from datetime import datetime
from datetime import timedelta
from time import sleep
import pandas as pd
import re

request_log = []
get_states = st.log_request(st.get_states,request_log)
ping = st.log_request(st.ping,request_log)
get_cities = st.log_request(st.get_cities,request_log)
scrape_city = st.log_request(st.scrape_city,request_log)
# You cannot reassign request_log after this point
# If you do, you have to run these four lines again

print("Gathering state links")
#####################################################################
links = st.get_states('Alabama')
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
# Loading in best guess variables
li = open('var_settings.txt','r').readlines()[0].split(', ')
min_forget = float(li[0])
forget_guess = float(li[1])
min_forgive = float(li[2])
max_forgive = float(li[3])
forgive_guess = float(li[4])

# Still trying to decide where is best to keep this but I think it
# works best where it is
def update_var_settings(a,b,c,d,e):
    f = open('C:/Users/lando/Desktop/Python/City Data/var_settings.txt','w')
    s = [a,b,c,d,e]
    f.write(str(s)[1:-1])
    f.close()
    
# Start scraping
n = 1
for state in all_cities.keys():
    state_df = pd.DataFrame()
    print(f"Scraping {state.replace('-',' ')} cities:")
    for city in all_cities[state]:
        
        # When you start to get close to ticking off the server,
        # take a break:
            # 1. Wait until we can assume it is starting to forget the
            #    earlier requests
            # 2. Lower our assumption by a little bit, but not past
            #    what we already know is unsafe
            # 3. Update var_settings.txt
        if len(request_log) >= 950:
            time_since = datetime.now()-request_log[-950]
            if time_since < timedelta(hours=forget_guess):
                wait_time = (timedelta(hours=forget_guess)-time_since).total_seconds()+60.
                a = datetime.now()
                print(f"Will resume scraping at {(a+timedelta(seconds=wait_time)).hour}:{(a+timedelta(seconds=wait_time)).minute}")
                sleep(wait_time)
                forget_guess = max(forget_guess-0.1,min_forget)
        
        # This one city causes problems for some reason
        if (city == 'Santa Margarita') & (state == 'California'):
            continue
        
        print(n, f"{city}, {state.replace('-',' ')}")
        city_url = url + f"city/{city.replace(' ','-')}-{state}.html"
        city_data = {'state':state.replace('-',' '),'city':[city]}
        
        # Do-While loop
        # If we get blocked by the server:
            # 1. Reflect the time we spent unblocked in min_forget
            # 2. Raise forget_guess if needed
            # 3. Use st.repent to wait for forgiveness
            # 4. Update request_log and forgive_guess
            # 5. Update var_settings.txt
        while True:
            addition = scrape_city(city_url)
            if addition is False: # If the server ignores me
                min_forget = max(min_forget,(datetime.now()-request_log[max(-len(request_log),-998)]).total_seconds()/3600.)
                forget_guess = min_forget + .5
                print(f"Setting minimum forget time to {min_forget:.01f} hours")
                min_forgive, max_forgive, pings = st.repent(min_forgive,max_forgive,forgive_guess,'city-data.com')
                forgive_guess = (min_forgive+max_forgive)/2
                update_var_settings(min_forget,forget_guess,min_forgive,max_forgive,forgive_guess)
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