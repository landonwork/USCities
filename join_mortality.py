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
cities = jn.join_counties()
cities['weight'] = cities['total-population'] / cities.groupby(['state','county_name'])['total-population'].transform('sum')
cities['percent-student'] = cities['student-population']/cities['total-population']
### Not entirely sure if this line is necessary but I want to make sure
### that the data is as consistent as possible
### Luckily, I only lose about 30 observations by doing this
cities = cities.loc[cities['year']==2017] 
###
weighted_col = ['percent-female','poverty-level','median-age',
                'pop-density','high-school-education','obesity-rate',
                'feel-bad','married','elevation','lat']
weighted_cities = pd.concat([cities[col]*cities['weight'] for col in weighted_col]+[cities[['state_id','county_name']]], axis=1)
counties = weighted_cities.groupby(['state_id','county_name']).sum()
counties.columns = weighted_col
counties = jn.retrieve_index(counties,['state_id','county_name'])

##############################################################################
def split_county(df):
    s = df['County'].str.split(', ',expand=True)
    s.columns = ['county_name','state_id']
    s['county_name'] = s['county_name'].str.replace(' County','')
    s['county_name'] = s['county_name'].str.replace(' Parish','')
    s['county_name'] = s['county_name'].str.replace(' Census Area','')
    s['county_name'] = s['county_name'].str.replace(' Borough','')
    s['county_name'] = s['county_name'].str.replace(' city','')
    s['county_name'] = s['county_name'].str.replace('Dona','Doña')
    s.index = df.index
    return pd.concat([df.drop('County',axis=1),s],axis=1)

pwd = 'C:/Users/lando/Desktop/Python/City Data/'
mortality = pd.read_csv(pwd+'Suicides by County for 2017.txt',sep='\t')
mortality = mortality.drop('Notes',axis=1).dropna()
mortality = split_county(mortality)

# So the suppressed values are obviously going to be null
# Missing values are also going to be null
# Unreliable is used for suicide rates where there are less than 20 deaths
# by suicide in a county. Maybe it's there to warn about loss of precision?
# I'm going to replace all the rates with newly computed
mortality[:] = np.where(mortality=='Missing',np.nan,mortality)
mortality[:] = np.where(mortality=='Suppressed',np.nan,mortality)
mortality['Crude Rate'] = (mortality['Deaths'].astype(float)/mortality['Population'].astype(float))*100000

### To remember after the data sets are combined ###
# The Crude Rate for any row that has a null value for the County Code
# is going to be a zero.
# The Crude Rate for any row that has a County Code but has a null value
# for the Crude Rate is still going to be a null value

combined = jn.join_by_col(
    counties,
    mortality.drop_duplicates(['state_id','county_name']),
    ['state_id','county_name'],['state_id','county_name']
    )

# Unfortunately, there are about 59 counties for which we do not have data
# but the CDC did, but that's okay
# Those con be removed and we can replace the other values as discussed before
combined = combined.dropna(subset=['percent-female'])
combined = combined.loc[~(~combined['County Code'].isna() & combined['Crude Rate'].isna())]
new_col = pd.DataFrame(np.where(combined['Crude Rate'].isna(),0,combined['Crude Rate']),index=combined.index,columns=['suicide-rate'],dtype=float)
cols = ['percent-female','poverty-level','median-age','pop-density',
        'high-school-education','obesity-rate','feel-bad','married',
        'elevation','lat']
combined = pd.concat([combined[cols],new_col],axis=1)

combined.to_csv(pwd+'suicide-rate-by-county.csv')