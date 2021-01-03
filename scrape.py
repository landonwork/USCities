# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:28:38 2020

@author: lando
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import pandas as pd
import re
from time import sleep
from datetime import datetime

def make_soup(url):
    n = 3
    while True:
        try:
            site = urlopen(url, timeout = 20)
            break
        except URLError as error:
            if str(error).find('timed out') != -1:
                a = datetime.now()
                print(f"Taking a break...{a.hour}:{a.minute}")
                sleep(60*60*n)
                n += 1
            else:
                print("Site does not exist")
                return None
        
    html = site.read()
    site.close()
    html_soup = soup(html,'html.parser')
    return html_soup

url = 'http://www.city-data.com/'
stuff = make_soup(url)
start_state = 'California'

print('Collecting state links...')
html_soup = make_soup(url)
html_soup = html_soup.findAll('div',{'id': 'home1'})[0]

links = []
switch = False
for state in html_soup.findAll('a'):
    if state.text == start_state:
        switch = True
    if switch == True:
        links.append(state['href'])

links.remove('http://www.city-data.com/city/District-of-Columbia.html')
links.remove('http://www.city-data.com/smallTowns.html')
### Now our list links only includes the 50 states

print('...State links collected')

def get_cities(state_url):
    state_soup = make_soup(state_url)
    state_soup = state_soup.find('table',{'id':'cityTAB'})
    state_soup = state_soup.find('tbody')
    
    city_names = []
    for row in state_soup.findAll('tr'):
        city = row.findAll('td')[1].text
        just_city = re.compile('(?P<city>(\w\s?)*)(\,\s\w\w\b)?')
        match = just_city.match(city)
        city = match.group('city')
        city_names.append(city)
        
    return city_names

### Scraping all the names of the cities in each state
print('Collecting city names by state...')
all_cities = {}
for link in links:
    get_state = re.compile('/city/(?P<state>.*)\.html')
    state_match = get_state.search(link)
    all_cities.update({state_match.group('state'): get_cities(link)})

print('...City names collected')
### And now we can scrape all the information about each city
def scrape_city(url):
    new_soup = make_soup(url)
    if new_soup is None:
        return {}
    
    new_soup = new_soup.find('div',{'id':'content'})
    sections = new_soup.findAll('section')
    
    # Creating and adding dictionaries
    # print("\tFilling dictionary...")
    content = {}
    for section in sections:
        content.update({section['id']: [section.text]})
    return content

### By using all_cities, I can create a 2-level for loop (state and city)
### to scrape the information on each city. I need to construct the urls,
### scrape the data, put it into a dict and then turn it into a DataFrame
### that I can concat with the main DataFrame

print('Preparing to scrape cities...')

start = False
j = 1
for state in all_cities.keys():
    if state == start_state: # Start at the next state that needs to be recorded
        start = True
    if start:
        state_df = pd.DataFrame()
        print('Scraping '+state.replace('-',' ')+' cities:')
        for city in all_cities[state]:
            if (city == 'Santa Margarita') & (state == 'California'):
                continue
            print(j, f"{city}, {state.replace('-',' ')}")
            city_url = f"http://www.city-data.com/city/{city.replace(' ','-')}-{state}.html"
            city_data = {'state':state.replace('-',' '),'city':[city]}
            # print('\tAccessing site...')
            city_data.update(scrape_city(city_url))
            # print('\tConverting to DataFrame...')
            df = pd.DataFrame.from_dict(city_data)
            # print('\tConcatenating...')
            state_df = pd.concat([state_df,df])
            j += 1
        
        filename = 'C:/Users/lando/Desktop/Python/City Data/'+state+'-cities.xlsx'
        state_df.to_excel(filename,sheet_name='Unabridged')
        print(state.replace('-',' ') + ' cities written to Excel file')
print('All done. Time to party!')