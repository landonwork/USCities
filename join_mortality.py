# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:32:36 2021

@author: lando
"""

import pandas as pd
import numpy as np
import join as jn

def count_na(df):
    for name in df.columns:
        print(f"{name}: {df[name].isnull().sum()}")

### Important Notes ###
# The suicide mortality data comes from the CDC
# Counties that are not included in their data had zero deaths
# So when joining this with other data it is important to treat some
# null values as zeros and others as actual null values

# The suicide mortality data comes with county populations that
# will be more reliable than summing populations from the collection
# of cities

# However, I should be able to use the populations as weights for cities within
# the same counties and (very roughly) approximate county **averages**
def county_info():
    cities = jn.join_counties()
    cities = cities.reset_index(drop=False)
    cities = cities.rename({'level_0':'state','level_1':'city'},axis=1)
    ### Not entirely sure if this line is necessary but I want to make sure
    ### that the data is as consistent as possible
    ### Luckily, I only lose about 30 counties by doing this
    cities = cities.loc[cities['year']==2017]
    
    cities['weight'] = cities['total_population'] / cities.groupby(['state','county_name'])['total_population'].transform('sum')
    weighted_col = ['percent_female','poverty_level','median_age',
                    'pop_density','high_school_education','bachelor_education',
                    'graduate_education','obesity_rate',
                    'feel_bad','married','elevation','lat']
    weighted_cities = pd.concat([cities[col]*cities['weight'] for col in weighted_col]+[cities[['state_id','county_name']]], axis=1)
    # I wonder if it's safe to assume that all of the college towns are included
    # in the data set. If I assume that, I can include student population in 
    # the counties DataFrame
    counties = weighted_cities.groupby(['state_id','county_name']).sum()
    counties['student_population'] = cities[['student_population','state_id','county_name']].groupby(['state_id','county_name']).sum()
    counties.columns = weighted_col + ['student_population']
    counties = counties.reset_index(drop=False)
    return counties

##############################################################################
def split_county(df,option=1):
    s = df['County'].str.split(', ',expand=True)
    s.columns = ['county_name','state_id']
    s['county_name'] = s['county_name'].str.replace(' County','')
    s['county_name'] = s['county_name'].str.replace(' Parish','')
    s['county_name'] = s['county_name'].str.replace(' Census Area','')
    s['county_name'] = s['county_name'].str.replace(' Borough','')
    
    if option:
        s['county_name'] = s['county_name'].str.replace(' city','')
        # This line creates duplicate state/county pairs
        # When I remove the duplicates, I get 25 less county observations.
        # I don't know why this happens because when I do not use this line,
        # none of the county names contain "city" in them anyway.
        # I have decided to continue using this line because I get
        # 10 less observations that do not have suicide data.
        
    s['county_name'] = s['county_name'].str.replace('Dona','Doña')
    s.index = df.index
    return pd.concat([df.drop('County',axis=1),s],axis=1)

def mortality_info(option=1):
    pwd = 'C:/Users/lando/Desktop/Python/City Data/'
    mortality = pd.read_csv(pwd+'Suicides by County for 2017.txt',sep='\t')
    mortality = mortality.drop('Notes',axis=1).dropna()
    mortality = split_county(mortality,option=option)
    
    # So the suppressed values are obviously going to be null
    # Missing values are also going to be null
    # Unreliable is used for suicide rates where there are less than 20 deaths
    # by suicide in a county. Maybe it's there to warn about loss of precision?
    # I'm going to replace all the rates with newly computed
    mortality[:] = np.where(mortality=='Missing',np.nan,mortality)
    mortality[:] = np.where(mortality=='Suppressed',np.nan,mortality)
    mortality['Crude Rate'] = (mortality['Deaths'].astype(float)/mortality['Population'].astype(float))*100000
    return mortality

### To remember after the data sets are combined ###
# The Crude Rate for any row that has a null value for the County Code
# is going to be a zero.
# The Crude Rate for any row that has a County Code but has a null value
# for the Crude Rate is still going to be a null value

def combine(option=1, keep='first'):
    combined = jn.join_by_col(
        county_info(),
        mortality_info(option=option).drop_duplicates(subset=['state_id','county_name'], keep=keep),
        ['state_id','county_name'],
        ['state_id','county_name'],
        )
    
    # Unfortunately, there are about 59 counties for which we do not have data
    # but the CDC did, but that's okay
    # Those can be removed and we can replace the other values as discussed before
    combined = combined.dropna(subset=['percent_female'])
    combined = combined.loc[~(~combined['County Code'].isna() & combined['Crude Rate'].isna())]
    
    new_cols = pd.DataFrame(
        np.where(
            combined[['Deaths','Population','Crude Rate']].isna(),
            0,
            combined[['Deaths','Population','Crude Rate']]
        ), 
        index=combined.index,
        columns=['deaths','population','suicide_rate'],
        dtype=float)
    
    combined = pd.concat([combined,new_cols],axis=1)
    combined['percent_students'] = combined['student_population']/combined['population']
    return combined.drop(['County Code','Crude Rate','Deaths','Population','population','student_population'],axis=1)

pwd = 'C:/Users/lando/Desktop/Python/City Data/'
combined = combine(option=1)
combined = combined.reset_index()
combined.to_csv(pwd+'suicide.csv')

combined = combine(option=1, keep=False)
combined = combined.reset_index()
combined.to_csv(pwd+'suicide_no_dups.csv')