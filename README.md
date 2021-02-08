# Cross-sectional Data of U.S. Cities
## Extracted from city-data.com
### Landon Work and collaborators

### Summary

This is a public repository with Python and R scripts involved in compiling
and analyzing cross-sectional data scraped from <https://www.city-data.com>                   .
The data set is a .csv file called all-nums.csv (names likely to change
eventually). The original text data from online was too big to upload
but the script to extract the numbers from the text is available.

The hope for this data is to be useful in econometric analysis
across the recent United States. Variables include economic indicators
(such as median prices and incomes) and standard of living indicators
(such as education, health and nutrition, air quality, and poverty).

### Data

The data have a wide range of variables across most cities in the
United States. Unfortunately, some variables were recorded at times
different from other variables even in the same city and most do not
have a date provided at which they were recorded. A description of
each variable and when they were recorded, if it is known, is included.

The sample is imperfect since we do not know how to tell if there is a
relationship between cities that do not have sites on city-data.com and
other factors or if it is truly random, but hopefully the size of the
data set can make up for accuracy somewhat with precision. Another caveat
is that the data set does include a few duplicates, most likely because of
cities with identical names in the same state and not knowing the correct
protocol for building a separate URL for each "twin".

### Related Projects

As an example and for personal practice, there is a project included that
looks to find a relationship between elevation and suicide risk. It
combines the USCities data and data from the [CDC][1]. Cities were grouped by
county (thanks to Raouf Sayem on [Kaggle][2]) and stored in
suicide-rates-by-county.csv

All variables in the data used for the regression are *estimated averages*
weighted by population. As far as is visible, the largest cities are not
missing from the data and these would have more influence over county
averages. The results for the regression are stored in regression-results.txt
and Restricted Regression Model.txt.

## USCities Variables

### General

All percent columns are stored in decimal form.

### Year

The year column is recorded from the total population text data. The most
frequent year is 2017 (15,968 observations), followed by 2010 and 2007 in
that order.  
This is useful because most other variables that are timestamped are from
more recent years (2017, 2018, 2019). The year column serves mainly to
select cities whose population data comes from 2017.

### Population

#### total-population, male-population, female-population
The male and female population columns sum to exactly the total population,
so it is assumed their timestamp matches total population. The year is
recorded by the year column.

#### percent-male, percent-female
The percents are calculated manually from the population columns.
There is little variation in the ratio between sexes.

#### land-area, pop-density
Total area of land inside the city boundaries, and population density
recorded out to 3 decimal places. Because of this there is a loss of
precision and the year of record cannot be confirmed.

#### foreign-born, student-population
Number of foreign-born residents (essentially immigrant population).  
Number of full-time university/technical college students attending any of
the 20 largest higher education facilities in the city.  
Unknown year of record.

### Median Age
#### median-age
Median age by city. Unknown year of record.

### Elevation
#### elevation
Elevation of the city in feet. Unknown year of record.

### Income Measures
#### poverty-level, median-household-income, per-capita-income

Poverty level by city (poverty guidelines for the U.S. can be found [here][3]),
estimated median total household income, and
total recorded earnings of city inhabitants divided by the total population.
All values are recorded in 2017.

### Housing Prices
#### median-home-value, median-rent

Median home value on the market by city (house/condo). Unknown whether it is
median value of homes sold or homes on the market.  
The median rent value in a city. Unknown whether monthly or yearly.  
Both are recorded in 2017.

### Education

#### gini-index
The Gini Education Inequality Index. Higher numbers represent more inequality
within the citizens of a city. Unknown year of record.

#### high-school-education, bachelor-education, graduate-education
Percent of adults 25 or older who have a level of education, its equivalent,
or higher. Unknown year of record.

### Health and Nutrition

#### diabetes-rate, obesity-rate, preschool-obesity
Adult diabetes rate, adult obesity rate, and percent of preschool-age
children from low-income households who are obese.
Gives meaningful information about the
standard of living among the impoverished.  
Unknown year of record.

#### average-health, average-hearing, healthy-diet-rate, teeth-and-gums
Average health measures which were recorded in percents.
Unknown year of record.

#### feel-bad, no-alcohol, average-sleep
Percent of the population that feels bad about themselves (possible measure
of mental health),  
percent of the population that claims to never drink alcohol, and  
number of hours that the average adult sleeps in a given night.

### Marital Status
#### never-married, married, separated, widowed, divorced
Percent of population who has never been married, is currently married,
is currently separated, is currently widowed, and is currently divorced.  
Unknown year of record.

### Additional Future Variables

A few other variables remain to be extracted from the text data:

* Religion and racial Demographics (these will be almost impossible to extract cleanly)
* Air Quality (year of record is 2018)
* Possibly Crime Rate (This could provide an entirely new panel data set.)
* Possibly Unemployment (Only has March 2017)

## Suicide Rate Regression Analysis
### Unique Variables in suicide-rates-by-county.csv

#### suicide-rate
Number of deaths in a county per 100,000 people in the year 2017.  
Retrieved from the [CDC][1] and used as the dependent variable
in the regression.

#### lat
Average latitude of the county's population. City latitudes taken from
Raouf Sayem's data on [Kaggle][2] and averaged.  
Included in an attempt to capture the effect of the difference in
daylight hours at higher latitudes or more northern regions.


[1]: <https://wonder.cdc.gov/mcd.html>
[2]: <https://www.kaggle.com/raoufseyam1/us-cities-counties-and-states>
[3]: <https://www.payingforseniorcare.com/federal-poverty-level>