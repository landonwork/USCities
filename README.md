# Cross-sectional Data of U.S. Cities
## Extracted from city-data.com
### Landon Work and collaborators

## Summary

This is a public repository with Python and R scripts
involved in compiling and analyzing a cross-sectional data set scraped
from city-data.com.
The data set is a .csv file called all-nums.csv. The original text data
from online was too big to upload but the script to extract the numbers
from the text is available.

The data has a wide range of variables across almost all cities in the
United States. Unfortunately, some variables were recorded at times
different from other variables even in the same city and most do not
have a date provided at which they were recorded. A description of
what is known about each variable will follow.

The hope for this data is to be useful in econometric analysis on the 
city level across the recent United States. Variables include
economic indicators such as median prices and incomes, and standard of
living such as education, health and nutrition, air quality, and poverty.
The sample is imperfect since we do not know how to tell if there is a
relationship between cities that do not have sites on city-data.com and
other factors or if it is truly random, but hopefully the size of the
data set can make up for accuracy somewhat with precision. Another caveat
is that the data set does include a few duplicates, most likely because of
cities with identical names in the same state and not knowing the correct
protocol for building each separate URL.

## Variables
### Year

The year column is recorded from the total population text data. The most
frequent year is 2017 (15,968 observations), followed by 2010 and 2007 in that order.
This is useful because most other variables that are timestamped are from
more recent years (2017, 2018, 2019). The year column serves mainly to
select cities whose population data comes from 2017.

### Population

Total, Male, and Female Population

The male and female population columns sum to exactly the total population,
so it is assumed their timestamp matches total population. The year is
recorded by the year column.
There is little variation in the ratio between sexes.

### Poverty Level

Poverty level by city. Values are ratios in decimal form. All recorded values
are recorded from the year 2017.

### Median Age

Median age by city. The year of record is unknown.

### Median Household Income

Estimated median total household income. Recorded in 2017.

### Per Capita Income

Total recorded earnings of city's inhabitants divided by the total population.
All observations recorded in 2017.

### Home Value

Median home value on the market by city (house/condo). Unknown whether it is
median value of homes sold or homes on the market. Recorded in 2017.

### Median Rent

The median rent value in a city. Also recorded in 2017.

### Land Area

Total area of land inside the city boundaries. Unknown year of record.

### Population Density

Population density recorded as a decimal out to three decimal places. For this
reason there is a loss of precision for cities with small populations and 
large land areas. Unknown year of record.

### Foreign Born

Number of foreign-born residents (essentially immigrant population). Unknown
year of record.

### Gini Index

The Gini Education Inequality Index. Higher numbers represent more inequality
within the citizens of a city. Unknown year of record.

### Student Population

Number of full-time university/technical college students attending any of
the 20 largest higher education facilities in the city. Could have important
relationships with median age/income and home values should a large part of
the population be students. Unknown year of record.

### High School, Bachelor, and Graduate Education

Percent of adults 25 or older with a certain level of education or higher.
Represented in all-nums.csv as a decimal value.
Unknown year of record.

### Diabetes and Obesity Rate

Adult diabetes and obesity rates by city. Percent represented as a decimal.
Unknown year of record.

### Preschool Obesity

Percent of obese preschool-age children from low-income households. Gives
meaningful information about the standard of living among the impoverished.
Unknown year of record.

## Additional Variables

Several other variables remain to be extracted from the text data:

* Marital Status
* Religion
* Racial Demographics (though this will be difficult and probably somewhat inaccurate)
* Air Quality
* Possibly Crime Rate
* Possibly Unemployment
* Healthy Diet Rate
* Average Teeth and Gums Health
* Alcohol/Tobacco Consumption
* Number of People Who Feel Badly About Themselves (mental health measure)