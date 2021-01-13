# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:28:38 2020

@author: lando
"""

url = 'http://www.city-data.com/'
start_state = 'California'

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
max_forget = float(li[1])
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
                sleep((timedelta(hours=max_forget)-time_since).total_seconds()+60.)
        if (city == 'Santa Margarita') & (state == 'California'):
            continue
        print(n, f"{city}, {state.replace('-',' ')}")
        city_url = url + f"city/{city.replace(' ','-')}-{state}.html"
        city_data = {'state':state.replace('-',' '),'city':[city]}
        addition = scrape_city(city_url)
        if addition is bool: # If the server ignored me
            min_forget = max(min_forget,(datetime.now()-request_log[-998]).total_seconds()/3600.)
            max_forget = min_forget+1
            print(f"Setting minimum forget time to {min_forget} hours")
            min_forgive, max_forgive, pings = repent(min_forgive,max_forgive,forgive_guess,url)
            forgive_guess = (min_forgive+max_forgive)/2
            request_log.extend(pings)
        city_data.update(addition)
        city_df = pd.DataFrame.from_dict(city_data)
        state_df = pd.concat([state_df,city_df])
        n += 1
    
    filename = 'C:/Users/lando/Desktop/Python/City Data/'+state+'-cities.xlsx'
    state_df.to_excel(filename,sheet_name='Unabridged')
    print(state.replace('-',' ') + ' cities written to Excel file')
#####################################################################

print('All done. Time to party!')

# There are two things to keep track of:
    # 1. How long it takes the server to forget past requests
    # 2. How long it takes the server to forgive me
# Forgetting:
    # 1. I will start by assuming it takes around 6 hours for the
    # server to forget who I am and that it blocks me after I have
    # reached 1000 requests that go unforgotten
    # 2. Therefore, if the server ever blocks me, I know it remembers at
    # least 1000 requests and the difference between the current time
    # and the last 1000th request is too short; in other words, the
    # forget time is longer than that time difference
    # 3. Using that time as a minimum forget time, I can keep track of
    # how many requests the server still remembers and stop the program
    # if it ever gets close to 1000 requests (say, 950)
    # 4. In addition, when I am certain the server has forgotten a request
    # there is no more reason to wait. This requires a max forget time.
    # Note: I will not be removing any values as I would like to look
    # at them myself later.
    # 5. There is no reason to predict an exact forget time, just a
    # safety margin. For simplicity, it will be one hour more than
    # the minimum forget time.
# Forgiving:
    # 1. I have reason to believe it could take as long as 24 hours for
    # the server to forgive me for exceeding the limit of requests in a
    # certain amount of time and that time blocked from the server
    # increases with additional requests while blocked
    # 2. Therefore, I must be careful when attempting to resume scraping.
    # I can being by assuming that it takes a minimum of, say, 8 hours
    # to be forgiven and a maximum of 48 and then use a binary method
    # to optimize the search method, starting with a guess of 24 hours
    # 4. It might also be useful to record the times at which my requests
    # are blocked