# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:11:11 2020

@author: lando
"""
import numpy as np
import pandas as pd
import re

def count_na(df):
    for name in df.columns:
        print(f"{name}: {df[name].isnull().sum()}")

# Good to go
# Total Population (years vary and are include by get_year)
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
    return pd.DataFrame({'total_population':li},index = df.index)

# Good to go
# Year (of population columns)
def get_year(df):
    li = [int(re.search('\d{4}',text).group()) for text in df['city-population']]
    return pd.DataFrame({'year':li},index=df.index)
    
# Good to go
# Male Population, Female Population
# Male and female add to exactly Total Population
# Percents all add to 1
# Assumed same year as Total Population
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
    return pd.DataFrame({'male_population':male_pop,'female_population':female_pop,'percent_male':perc_male,'percent_female':perc_female}, index = df.index)

# Good to go
# Poverty Level
# I don't have the guts to try and grab all of the racial poverty levels right now. That's a lot.
# All values between 0 and 1
# All from 2017
def get_poverty(df):
    li=[]
    get_pov = re.compile('in \d{4}:\s(?P<pov>.*?)\%')
    for text in df['poverty-level']:
        if text is np.nan:
            li.append(text)
            continue
        else:
            li.append(float(get_pov.search(text).group('pov'))/100)
    return pd.DataFrame({'poverty_level':li},index=df.index)

# Good to go
# Median Age
# Year is unknown
def get_age(df):
    li=[]
    get_age = re.compile('resident age:(?P<age>\d*\.?\d?) years')
    for text in df['median-age']:
        age = float(get_age.search(text).group('age'))
        li.append(age)
    return pd.DataFrame({'median_age':li},index=df.index)

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
    return pd.DataFrame({'household_income':hh_income,'per_capita_income':per_capita_income,'median_home_value':home_value},index=df.index)

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
    return pd.DataFrame({'median_rent':li},index=df.index)

# Good to go
# Land Area and Population Density
# Population density only goes out to one decimal place
# so there are 71 cities whose population, as calculated using land area
# and population density, varies by more than 5 percent from the true
# population. They are all large land-wise and sparsely populated.
# Year is unknown
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
    return pd.DataFrame({'land_area':areas,'pop_density':dens},df.index)

# Good to go
# Foreign-Born Residents (Immigrants)
# Year is unknown
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
    return pd.DataFrame({'foreign_born':li},index=df.index)

# Good to go
# Gini Education Inequality Index
# Year is unknown
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
    return pd.DataFrame({'gini_index':li}, index = df.index)

# Good to go
# Student Population
# Full-time students from the 20 largest colleges/universities in the city
# 0 for most cities
# Some schools did not include enrollment, so it's not perfect
# Year is unknown
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
    return pd.DataFrame({'student_population':li},index=df.index)
            
# Good to go
# Percent High School, Bachelor's, Graduate
# Percent of population 25 or older with a certain level of education or higher
# Year is unknown
def get_educ(df):
    names = ['High school','Bachelor','Graduate']
    extras = [' or higher',"\'s degree or higher",' or professional degree']
    d = {}
    zipped = zip(names,extras)
    for name, extra in zipped:
        get_educ = re.compile(name+extra+':\s(?P<educ>\d*?\.\d)%')
        li = []
        for i, cell in enumerate(df['education-info']):
            if cell is np.nan:
                ans = np.nan
            else:
                try:
                    ans = float(get_educ.search(cell).group('educ'))/100
                except AttributeError:                
                    ans = np.nan
            li.append(ans)
        col = name.lower().replace(' ','_') + '_education'
        d.update({col:li})
    return pd.DataFrame(d,index=df.index)


# I will work on this later. Lots of variation in which races are included.
# Does that mean I can count na's as 0? I have to decide what to do about that.
def add_race(df,race,name):
   pass

# Before I get to that I think I will grab marital status, diabetes and 
# obesity rates, healthy diet, teeth and gums, alcohol/tobacco consumption,
# how people feel about themselves, etc. and maybe air quality

# Good to go
# Adult Diabetes Rate, Adult Obesity Rate, Preschool Obesity Rate
# Unknown year
def get_food(df):
    dia = re.compile('Adult diabetes rate:.*?:\s?(?P<perc>\d*\.\d)%')
    obese = re.compile('Adult obesity rate:.*?:\s?(?P<perc>\d*\.\d)%')
    pre_obese = re.compile('Low-income preschool obesity rate:.*?:\s?(?P<perc>\d*\.\d)%')
    names = ['diabetes_rate','obesity_rate','preschool_obesity']
    patterns = [dia,obese,pre_obese]
    lists = [[],[],[]]
    for city in df['food-environment']:
        for i in range(len(names)):
            m = patterns[i].search(city)
            if bool(m):
                lists[i].append(float(m.group('perc'))/100)
            else:
                lists[i].append(np.nan)
    return pd.DataFrame({names[j]:lists[j] for j in range(3)},index=df.index)

# Good to go
# There are 7000 NA values in each column but in the 2017 data set, there
# are fewer than 1000 in each
# Unknown year
def get_health(df):
    
    diet = re.compile('Healthy diet rate:.*?:\s?(?P<num>\d*\.\d)%')
    teeth_n_gums = re.compile('teeth and gums:.*?:\s?(?P<num>\d*\.\d)%')
    feel_bad = re.compile('feeling badly about themselves:.*?:\s?(?P<num>\d*\.\d)%')
    health = re.compile('General health condition:.*?:\s?(?P<num>\d*\.\d)%')
    hearing = re.compile('hearing:.*?:\s?(?P<num>\d*\.\d)%')
    no_alcohol = re.compile('not drinking alcohol at all:.*?:\s?(?P<num>\d*\.\d)%')
    
    names = ['average_health','average_hearing','healthy_diet_rate','teeth_and_gums','feel_bad','no_alcohol']
    patterns = [health,hearing,diet,teeth_n_gums,feel_bad,no_alcohol]
    lists = [[],[],[],[],[],[]]
    for city in df['health-nutrition']:
        for i in range(len(names)):
            if city is np.nan:
                lists[i].append(np.nan)
                continue
            m = patterns[i].search(city)
            if bool(m):
                lists[i].append(float(m.group('num'))/100)
            else:
                lists[i].append(np.nan)
    return pd.DataFrame({names[j]:lists[j] for j in range(len(names))},index=df.index)

# Good to go
# Again 7000 NA values but few for 2017
# Unknown year
def get_sleep(df):
    li = []
    for city in df['health-nutrition']:
        if city is np.nan:
           li.append(np.nan)
           continue
        m = re.search('sleeping at night:.*?:\s?(?P<num>\d{1,2}\.\d)',city)
        if bool(m):
            li.append(float(m.group('num')))
        else:
            li.append(np.nan)
    return pd.DataFrame({'average_sleep':li},index=df.index)

# Good to go
# Elevation in feet
# This would be an interesting variable to test with suicide rates
# Someone mentioned to me suicide rates being higher in places with higher
# elevations. We could also try northern states versus southern states
# to see if latitude has something to do with it. Or maybe cities that are
# right on the northern/southern border
def get_elevation(df):
    li = []
    for city in df['elevation']:
        if city is np.nan:
            li.append(np.nan)
            continue
        m = re.search('Elevation: (?P<num>\d+) f',city)
        if bool(m):
            li.append(int(m.group('num')))
        else:
            li.append(np.nan)
    return pd.DataFrame({'elevation':li},index=df.index)
        

# Good to go
# I believe marital status could be another important factor in suicide rates
def get_marriage(df):
    
    never = re.compile('Never married:\s*(?P<num>\d*\.\d)%')
    married = re.compile('Now married:\s*(?P<num>\d*\.\d)%')
    separated = re.compile('Separated:\s*(?P<num>\d*\.\d)%')
    widowed = re.compile('Widowed:\s*(?P<num>\d*\.\d)%')
    divorced = re.compile('Divorced:\s*(?P<num>\d*\.\d)%')
    
    names = ['never_married','married','separated','widowed','divorced']
    patterns = [never,married,separated,widowed,divorced]
    lists = [[],[],[],[],[]]
    for city in df['marital-info']:
        for i in range(len(names)):
            if city is np.nan:
                lists[i].append(np.nan)
                continue
            m = patterns[i].search(city)
            if bool(m):
                lists[i].append(float(m.group('num'))/100)
            else:
                lists[i].append(np.nan)
    return pd.DataFrame({names[j]:lists[j] for j in range(len(names))},index=df.index)


# I haven't been able to grab the racial demographics in a clean way and
# I have wasted a lot of time trying, so it is not included.
# For the same reason, I am not going to include religion in the data set.                
        
df = pd.read_excel('C:/Users/lando/Desktop/Python/City Data/all-cities.xlsx',sheet_name='Unabridged')

# Set the index; this unfortunately must be done every time
# the DataFrame is read from the file. However, it is not
# entirely necessary. It just simplifies looking for specific cities.
df = df.set_index(['state','city'])

# Dropping rows that are completely empty or only have useless information
df = df.dropna(thresh = 8) # thresh drops rows that have less than 8 non-n/a values

# city-population has been a pretty good indicator of the
# completeness of the data, so I'm going to sort by that
df = df[df['city-population'].notna()]
df_2017 = df[df['city-population'].str.contains('2017')]
df_2010 = df[df['city-population'].str.contains('2010')]
df_july07 = df[df['city-population'].str.contains('in July 2007')]
# If I can make the cleaning functions work with any date, I think I can
# scrub the data first and split them later.
# This leaves 46 rows unaccounted for. They are from random years.

# Building the numerical dataset
nums = pd.DataFrame(index=df.index)
fns = [get_year, get_pop,    get_sex,       get_poverty, get_age,  get_income,
       get_rent, density,    get_elevation, foreign,     get_gini, get_students,
       get_educ, get_food,   get_health,    get_sleep,   get_marriage]
for fn in fns:
    nums = pd.concat([nums,fn(df)],axis=1)
nums.to_csv('C:/Users/lando/Desktop/Python/City Data/all_nums.csv')