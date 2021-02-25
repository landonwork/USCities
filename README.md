# Cross-sectional Data of U.S. Cities
## Extracted from city-data.com
### Landon Work and collaborators

### Summary

This is a public repository with Python and R scripts involved in compiling
and analyzing cross-sectional data scraped from <https://www.city-data.com>                   .
The data set is a .csv file called all_nums.csv (names likely to change
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

#### total_population, male_population, female_population
The male and female population columns sum to exactly the total population,
so it is assumed their timestamp matches total population. The year is
recorded by the year column.

#### percent_male, percent_female
The percents are calculated manually from the population columns.
There is little variation in the ratio between sexes.

#### land_area, pop_density
Total area of land inside the city boundaries in square miles,
and population density recorded out to 3 decimal places. Because
of this there is a loss of precision and the year of record cannot
be confirmed.

#### foreign_born, student_population
Number of foreign-born residents (essentially immigrant population).  
Number of full-time university/technical college students attending any of
the 20 largest higher education facilities in the city.  
Unknown year of record.

### Median Age
#### median_age
Median age by city. Unknown year of record.

### Elevation
#### elevation
Elevation of the city in feet. Unknown year of record.

### Income Measures
#### poverty_level, median_household_income, per_capita_income

Poverty level by city (poverty guidelines for the U.S. can be found [here][3]),
estimated median total household income, and
total recorded earnings of city inhabitants divided by the total population.
All values are recorded in 2017.

### Housing Prices
#### median_home_value, median_rent

Median home value on the market by city (house/condo). Unknown whether it is
median value of homes sold or homes on the market.  
The median rent value in a city. Unknown whether monthly or yearly.  
Both are recorded in 2017.

### Education

#### gini_index
The Gini Education Inequality Index. Higher numbers represent more inequality
within the citizens of a city. Unknown year of record.

#### high_school_education, bachelor_education, graduate_education
Percent of adults 25 or older who have a level of education, its equivalent,
or higher. Unknown year of record.

### Health and Nutrition

#### diabetes_rate, obesity_rate, preschool_obesity
Adult diabetes rate, adult obesity rate, and percent of preschool-age
children from low-income households who are obese.
Gives meaningful information about the
standard of living among the impoverished.  
Unknown year of record.

#### average_health, average_hearing, healthy_diet_rate, teeth_and_gums
Average health measures which were recorded in percents.
Unknown year of record.

#### feel_bad, no_alcohol, average_sleep
Percent of the population that feels bad about themselves (possible measure
of mental health),  
percent of the population that claims to never drink alcohol, and  
number of hours that the average adult sleeps in a given night.

### Marital Status
#### never_married, married, separated, widowed, divorced
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

#### suicide_rate
Number of deaths in a county per 100,000 people in the year 2017.  
Retrieved from the [CDC][1] and used as the dependent variable
in the regression.

#### lat
Average latitude of the county's population. City latitudes taken from
Raouf Sayem's data on [Kaggle][2] and averaged.  
Included in an attempt to capture the effect of the difference in
daylight hours at higher latitudes or more northern regions.

#### percent_students
Percent of the county population that is attending a university or technical
college full-time. Calculated by summing the full-time student population
from all_cities.csv and dividing by the county population in the CDC data set.
Assuming all_cities.csv contained all the city student populations from 2017,
this should come close to the actual county student ratio.

### Interpretation of Results

Results of the linear regression analysis are stored in summary.txt and
summary_no_dups.txt. Because the data contained duplicate county/state
name combinations there was no way to tell whether the data was matched
correctly by keeping the first, so I removed all duplicates and did
everything again. It didn't seem to change much.

The regression summaries all contain the unrestricted model of the data
for comparison. The first in each are initial unrestricted results. The
second summary contains all data points, but comparing different restricted
models. When all data points are included, married and percent_students contain
information that is important for the coefficients of the education variables.
The third summary discards data points where the number of deaths by county was
less than 20. These were marked by the CDC as "Unreliable." When removed,
percent_students becomes highly significant and married loses significance.

The coefficients of all percentage measures can be interpreted as the change
in the county suicide rate (deaths per 100,000 people) for a one percentage
point increase of that measure. The coefficient of population density is the
change in the suicide rate for a 100 person per square increase. The coefficient
of elevation is the change in the suicide rate for a 1,000 foot increase in
elevation.


[1]: <https://wonder.cdc.gov/mcd.html>
[2]: <https://www.kaggle.com/raoufseyam1/us-cities-counties-and-states>
[3]: <https://www.payingforseniorcare.com/federal-poverty-level>