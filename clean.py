# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:11:11 2020

@author: lando
"""
import numpy as np
import pandas as pd
import re
from functools import reduce

def count_na(df):
    for name in df.columns:
        print(name +': '+str(df[name].isnull().sum()))

# Good to go
# Total Population
def get_pop(df):
    peeps = re.compile('\d{4}:\s(?P<population>\d+(\,\d{3})*)')
    li = []
    for text in df['city-population']:
        match = peeps.search(text)
        if bool(match):
            num = int(match.group('population').replace(',',''))
            li.append(num)
        else:
            li.append(np.nan)
    return pd.DataFrame({'total-population':li},index = df.index)

# Good to go
# Year (of population columns)
def get_year(df):
    li = [int(re.search('\d{4}',text).group()) for text in df['city-population']]
    return pd.DataFrame({'year':li},index=df.index)
    
# Good to go
# Male Population, Female Population
# Male and female add to exactly Total Population
# Percents all add to 1
def get_sex(df):
    males = re.compile('Males:\s(?P<male>\d*(\,\d{3})*)\s*\((?P<perc_male>.+?)%\)')
    females = re.compile('Females:\s(?P<female>\d*(\,\d{3})*)\s*\((?P<perc_female>.+?)%\)')
    male_pop, perc_male, female_pop, perc_female = [],[],[],[]
    for text in df['population-by-sex']:
        if bool(males):
            male_pop.append(int(males.search(text).group('male').replace(',','')))
            perc_male.append(float(males.search(text).group('perc_male'))/100)
        else:
            male_pop.append(np.nan)
            perc_male.append(np.nan)
        if bool(females):
            female_pop.append(int(females.search(text).group('female').replace(',','')))
            perc_female.append(float(females.search(text).group('perc_female'))/100)
        else:
            female_pop.append(np.nan)
            perc_female.append(np.nan)
    return pd.DataFrame({'male-population':male_pop,'female-population':female_pop,'percent-male':perc_male,'percent-female':perc_female}, index = df.index)

# Good to go
# Poverty Level
# I don't have the guts to try and grab all of the racial poverty levels right now. That's a lot.
# All values between 0 and 1
def get_poverty(df):
    li=[]
    get_pov = re.compile('in \d{4}:\s(?P<pov>.*?)\%')
    for text in df['poverty-level']:
        if text is np.nan:
            li.append(text)
            continue
        else:
            li.append(float(get_pov.search(text).group('pov'))/100)
    return pd.DataFrame({'poverty-level':li},index=df.index)

# Good to go
# Median Age
def get_age(df):
    li=[]
    get_age = re.compile('resident age:(?P<age>\d*\.?\d?) years')
    for text in df['median-age']:
        age = float(get_age.search(text).group('age'))
        li.append(age)
    return pd.DataFrame({'median-age':li},index=df.index)

# Good to go
# Median household Income, Per Capita Income, Median Home Value
# Interestingly, all of the data in these columns are from 2017
# This may cause problems if I try to use this with populations from
# different years
def get_income(df):
    hh_income, per_capita_income, home_value = [],[],[]
    list_tuple = (hh_income, per_capita_income, home_value)
    hh = re.compile('household income in \d{4}: \$(?P<value>\d+(\,\d{3})*)\s')
    per_capita = re.compile('per capita income in \d{4}: \$(?P<value>\d+(\,\d{3})*)\s')
    home = re.compile('value in \d{4}: \$(?P<value>\d+(\,\d{3})*)\s')
    for text in df['median-income']:
        match_tuple = (hh.search(text), per_capita.search(text), home.search(text))
        for i in range(len(match_tuple)):
            if match_tuple[i] is None:
                list_tuple[i].append(np.nan)
            else:
                list_tuple[i].append(float(match_tuple[i].group('value').replace(',','')))        
    return pd.DataFrame({'median-household-income':hh_income,'per-capita-income':per_capita_income,'median-home-value':home_value},index=df.index)

# Good to go
# Median Rent
# This column also only has data from 2017
def get_rent(df):
    li = []
    for text in df['median-rent']:
        if text is np.nan:
            li.append(np.nan)
        else:
            li.append(float(re.search('\d{4}: \$(?P<rent>\d+(\,\d{3})*(\.d{2})?)',text).group('rent').replace(',','')))
    return pd.DataFrame({'median-rent':li},index=df.index)

# Good to go
# Land Area and Population Density
# Population density only goes out to one decimal place
# so there are 71 cities whose population, as calculated using land area
# and population density, varies by more than 5 percent from the true
# population
def density(df):
    areas, dens = [], []
    get_area = re.compile('area:\s(?P<area>\d*(\,\d*)*(\.\d+)?)\s')
    get_dens = re.compile('density:\s(?P<dens>\d*(\,\d*)*(\.\d+)?)\s')
    for cell in df['population-density']:
        try:
            a = get_area.search(cell).group('area')
            a = float(a.replace(',',''))
            d = get_dens.search(cell).group('dens')
            d = float(d.replace(',',''))
        except TypeError:
            a = np.nan
            d = np.nan
        areas.append(a)
        dens.append(d)
    return pd.DataFrame({'land-area':areas,'pop-density':dens},df.index)

# Good to go
# Foreign-Born Residents (Immigrants)
def foreign(df):
    li=[]
    get_born = re.compile('\d*(\,\d*)*')
    for cell in df['foreign-born-population']:
        if cell is np.nan:
            ans = np.nan
        else:
            ans = get_born.match(cell).group()
            ans = float(ans.replace(',',''))
        li.append(ans)
    return pd.DataFrame({'foreign-born':li},index=df.index)

# Good to go
# Gini Education Inequality Index
def get_gini(df):
    li=[]
    get_gini = re.compile('Here:(?P<gini>\d*?\.\d)')
    for cell in df['education-graphs']:
        try:
            ans = get_gini.search(cell).group('gini')
            ans = float(ans.replace(',',''))
        except (AttributeError, TypeError):
            ans = np.nan
        li.append(ans)
    return pd.DataFrame({'gini-index':li}, index = df.index)

# Good to go
# Student Population
# Full-time students from the 20 largest colleges/universities in the city
# 0 for most cities
# Some schools did not include enrollment, so it's not perfect
# I figure it can hugely affect income, age, housing prices, and education
def get_students(df):
    li = []
    for city in df['schools']:
        num = 0
        begin = False
        schools = city.split('\n')
        for s in schools:
            if s == '' and begin:
                break
            if bool(re.match('(Biggest )?College(s?)/Universit(y|ies)',s)):
                begin = True
            if begin:
                try:
                    num += int(re.search('enrollment:\s*(?P<num>\d*(\,\d*)*)',s).group('num').replace(',',''))
                except AttributeError:
                    pass
        li.append(num)
    return pd.DataFrame({'student-population':li},index=df.index)
            


# Percent High School, Bachelor's, Doctorate
def get_educ(df,level,or_hi=True):
    hi = ' or higher:' if or_hi == True else ':'
    get_educ = re.compile(level+hi+'\s(?P<educ>\d*?\.\d)%')
    l = []
    for cell in df['education-info']:
        try:
            ans = float(get_educ.search(cell).group('educ'))
        except AttributeError:
            ans = np.nan
        l.append(ans)
    name = level.lower().replace(' ','-').replace('\'','')
    return pd.concat([df,pd.DataFrame(l,df.index,columns=[name])],axis=1)


# I will work on this later. Lots of variation in which races are included.
# Does that mean I can count na's as 0?
def add_race(df,race,name):
    l=[]
    get_nums = re.compile('(?P<nums>\d*(\,\d*)*\.\d*)\%'+race)
    for i in range(len(df)):
        print(race,i)
        cell = df.iloc[i]['races-graph']
        if cell is np.nan:
            l.append(np.nan)
            continue
        if cell.find(r'%'+race) == -1:
            l.append(np.nan)
            continue
        nums = get_nums.search(cell).group('nums')
        y = 0
        while y != -1:
            last_comma = y
            y = nums.find(',',y+1)
        if last_comma == 0:
            x = nums.find('.')-1
            pop = df.iloc[i]['population']
            while x != 0:
                num1 = int(nums[:x])
                num2 = float(nums[x:])
                diff = abs(num1 / pop * 100 - num2)
                if diff < 20:
                    break
                else:
                    x -= 1
            ans = num1 if x != 0 else np.nan
        else:
            ans = int(nums[0:last_comma+4].replace(',',''))
        l.append(ans)
    print(race,'population added to the dataset')
    return pd.concat([df,pd.DataFrame(l,index=df.index,columns = [name])],axis=1)

    
df = pd.read_excel('C:/Users/lando/Desktop/Python/City Data/all-cities.xlsx',sheet_name='Unabridged')
df = df.set_index(['state','city'])
# Dropping rows that are completely empty or only have useless information
df = df.dropna(thresh = 8) # thresh drops rows that have less than 8 non-n/a values
# city-population has been a pretty good indicator of the
# completeness of the data, so I'm going to sort by that
df = df[df['city-population'].notna()]
df_2017 = df[df['city-population'].str.contains('in 2017')]
df_2010 = df[df['city-population'].str.contains('in 2010')]
df_july07 = df[df['city-population'].str.contains('in July 2007')]
# If I can make the cleaning functions work with any date, I think I can
# scrub the data first and split them later

# This leaves 46 rows unaccounted for. They are from random years.
df_other = df.drop(df_2017.index)
df_other = df_other.drop(df_2010.index)
df_other = df_other.drop(df_july07.index)

# Building the numerical dataset
nums = pd.DataFrame(index=df.index)
fns = [get_year, get_pop, get_sex, get_poverty, get_age, get_income,
       get_rent, density, foreign, get_gini, get_students]
for fn in fns:
    nums = pd.concat([nums,fn(df)],axis=1)
nums.to_csv('all-nums.csv')