# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:33:40 2021

@author: lando

This script contains tools for accessing sites and scraping data
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from socket import timeout
from datetime import datetime
import re

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

from time import sleep

# Decorator that will add the time a function is called to a list
def log_request(fn,log):
    def wrapped_fn(*args,**kwargs):
        value = fn(*args,**kwargs)
        log.append(datetime.now())
        return value
    return wrapped_fn

# Returns True if host (str) responds to a ping request, otherwise False
def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host] # Building the command. Ex: "ping -c 1 google.com"
    return subprocess.call(command) == 0

# Return a BeautifulSoup object if successful, None if the site does
# not exist, or False if the request times out
def make_soup(url):
    try:
        site = urlopen(url, timeout = 20)
    except (HTTPError, URLError) as error:
        if isinstance(error.reason,timeout):
            print(f"Connection timed out.")
            return False
        else:
            print("Site does not exist.")
            return None
    except timeout:
        print(f"Connection timed out.")
        return False
    html = site.read()
    site.close()
    html_soup = soup(html,'html.parser')
    return html_soup

def get_cities(url):
    state_soup = make_soup(url)
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

def scrape_city(url):
    new_soup = make_soup(url)
    if not bool(new_soup):
        if new_soup is None:
            return {}
        elif not new_soup:
            return False
        else:
            raise Exception("Something weird happened")
    new_soup = new_soup.find('div',{'id':'content'})
    sections = new_soup.findAll('section')
    content = {}
    for section in sections:
        content.update({section['id']: [section.text]})
    return content

def repent(mini,maxi,guess,url):
    begrudged = True
    pings = []
    while True:
        print(f"Repenting for {guess} hours")
        sleep(60*60*guess)
        begrudged = not ping(url)
        pings.append(datetime.now())
        if begrudged:
            mini = guess
            guess = (mini+maxi)/2
        else:
            maxi = guess
            break
    return mini, maxi, pings
