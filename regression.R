library(corrgram)
library(stargazer)
library(car)

df = read.csv('C:/Users/lando/Desktop/Python/City Data/suicide.csv')
df1 = df[is.finite(rowSums(df[, -c(1:3)])), -c(1,3)]

corrgram(df1, upper.panel = panel.pie, lower.panel = panel.pts)

# percent_female, median_age, high_school_education, obesity_rate,
# feel_bad, married, and lat are all highly positively correlated.

# The most promising predictors of suicide rates are, in order:
#      1. pop_density
#      2. elevation
#      3. bachelor_education
#      4. graduate_education
#      5. poverty_level
#      6. median_age
#      7. feel_bad
#      8. percent_students
#      9. obesity_rate
#     10. lat
#     11. percent_female
#     12. married
#     13. high_school_education

model <- lm(suicide_rate ~ pop_density + 
              I(elevation/1000) + 
              I(high_school_education*100) + 
              I(bachelor_education*100) +
              I(graduate_education*100) +
              I(percent_female*100) + 
              median_age + 
              lat + 
              I(married*100) + 
              I(feel_bad*100) + 
              I(obesity_rate*100) + 
              I(percent_students*100),
            data=df1)

summary1 <- stargazer(model,type='text')

myH0 <- c('I(percent_female * 100)','lat','I(married * 100)','I(feel_bad * 100)','I(obesity_rate * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# (p-value: 0.06013)
# There may be reason to keep some variables but not all

myH0 <- c('I(percent_female * 100)','lat','I(married * 100)','I(feel_bad * 100)','I(obesity_rate * 100)')
linearHypothesis(model,myH0)
# p-value: .1719

myH0 <- c('I(percent_female * 100)','lat','I(married * 100)','I(feel_bad * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .06823

myH0 <- c('I(percent_female * 100)','lat','I(married * 100)','I(obesity_rate * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .05027

myH0 <- c('I(percent_female * 100)','lat','I(feel_bad * 100)','I(obesity_rate * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .1507

myH0 <- c('I(percent_female * 100)','I(married * 100)','I(feel_bad * 100)','I(obesity_rate * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .08195

myH0 <- c('lat','I(married * 100)','I(feel_bad * 100)','I(obesity_rate * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .03687

myH0 <- c('I(married * 100)','I(feel_bad * 100)','I(obesity_rate * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .05199

# It seems married and percent_students are the most important variables out of this lot
myH0 <- c('I(married * 100)','I(percent_students * 100)')
linearHypothesis(model,myH0)
# p-value: .03236

restricted_model1 = lm(suicide_rate ~ pop_density + 
                        I(elevation/1000) + 
                        I(high_school_education*100) + 
                        I(bachelor_education*100) + 
                        I(graduate_education*100) +
                        median_age + 
                        I(married*100) + 
                        I(percent_students*100),
                      data=df1)

restricted_model2 = lm(suicide_rate ~ pop_density + 
                         I(elevation/1000) + 
                         I(high_school_education*100) + 
                         I(bachelor_education*100) + 
                         I(graduate_education*100) +
                         median_age,
                       data=df1)

summary2 <- stargazer(model,restricted_model1,restricted_model2,type='text')
# I think the best model includes married and percent_students because
# it cause three of the estimators to change by a pretty significant
# amount. In order to understand this better, it may be useful
# to look at a covariance matrix.

# Now I am only using observations that were not deemed "unreliable"
# by the CDC
df2 = df1[subset(df1, select=c("deaths")) >= 20, ]

model <- lm(suicide_rate ~ pop_density + 
              I(elevation/1000) + 
              I(high_school_education*100) + 
              I(bachelor_education*100) +
              I(graduate_education*100) +
              I(percent_female*100) + 
              median_age + 
              lat + 
              I(married*100) + 
              I(feel_bad*100) + 
              I(obesity_rate*100) + 
              I(percent_students*100),
            data=df2)

myH0 = c("I(percent_female * 100)","lat","I(married * 100)","I(obesity_rate * 100)")
linearHypothesis(model,myH0)
# P-value: .6832

restricted_model = lm(suicide_rate ~ pop_density + 
                         I(elevation/1000) + 
                         I(high_school_education*100) + 
                         I(bachelor_education*100) + 
                         I(graduate_education*100) +
                         median_age + 
                         I(feel_bad*100) +
                         I(percent_students*100),
                       data=df2)

summary3 <- stargazer(model,restricted_model,type='text')
# feel_bad and percent_students is super significant now.
# This model has a super high R^2 also.

# No duplicates
df3 = read.csv('C:/Users/lando/Desktop/Python/City Data/suicide_no_dups.csv')
df3 = df3[is.finite(rowSums(df3[,-c(1:3)])), -c(1:3)]

model1 <- lm(suicide_rate ~ pop_density + 
              I(elevation/1000) + 
              I(high_school_education*100) + 
              I(bachelor_education*100) +
              I(graduate_education*100) +
              I(percent_female*100) + 
              median_age + 
              lat + 
              I(married*100) + 
              I(feel_bad*100) + 
              I(obesity_rate*100) + 
              I(percent_students*100),
            data=df1)

model2 <- lm(suicide_rate ~ pop_density + 
               I(elevation/1000) + 
               I(high_school_education*100) + 
               I(bachelor_education*100) +
               I(graduate_education*100) +
               I(percent_female*100) + 
               median_age + 
               lat + 
               I(married*100) + 
               I(feel_bad*100) + 
               I(obesity_rate*100) + 
               I(percent_students*100),
             data=df3)


summary_dups_vs_no_dups <- stargazer(model1,model2,type='text')
# No shocking or surprising changes

restricted_model1 = lm(suicide_rate ~ pop_density + 
                         I(elevation/1000) + 
                         I(high_school_education*100) + 
                         I(bachelor_education*100) + 
                         I(graduate_education*100) +
                         median_age + 
                         I(married*100) + 
                         I(percent_students*100),
                       data=df3)

restricted_model2 = lm(suicide_rate ~ pop_density + 
                         I(elevation/1000) + 
                         I(high_school_education*100) + 
                         I(bachelor_education*100) + 
                         I(graduate_education*100) +
                         median_age,
                       data=df3)

summary1_no_dups <- stargazer(model2,restricted_model1,restricted_model2,type='text')
# Again, no shocking revelations

df4 = df3[df3$deaths >= 20, ]

model <- lm(suicide_rate ~ pop_density + 
              I(elevation/1000) + 
              I(high_school_education*100) + 
              I(bachelor_education*100) +
              I(graduate_education*100) +
              I(percent_female*100) + 
              median_age + 
              lat + 
              I(married*100) + 
              I(feel_bad*100) + 
              I(obesity_rate*100) + 
              I(percent_students*100),
            data=df4)

myH0 = c("I(percent_female * 100)","lat","I(married * 100)","I(obesity_rate * 100)")
linearHypothesis(model,myH0)

restricted_model = lm(suicide_rate ~ pop_density + 
                        I(elevation/1000) + 
                        I(high_school_education*100) + 
                        I(bachelor_education*100) + 
                        I(graduate_education*100) +
                        median_age + 
                        I(feel_bad*100) +
                        I(percent_students*100),
                      data=df2)

summary2_no_dups <- stargazer(model,restricted_model,type='text')
# Same performance as the df2 model

# There are some other things that I would like to do now:
#       1. I need to add in the other measures of education because those
#          are correlated and some levels of education could be more
#          important than others.
#          Edit: CHECK
#       2. I need to rinse and repeat without the counties that have:
#             a. No entry from the CDC
#                Edit: I cannot use percent_students and test this at
#                      the same time but it doesn't bother me too much
#                      because there were only 9 observations lost
#             b. The counties called "unreliable"
#                Edit: CHECK
#             c. No duplicate counties and cities (neither first nor last)
#                Edit: Use suicide_no_dups.csv
#                Edit: CHECK
#       3. Then I have to ask for advice about causality
#          Edit: There's not much I can do there, but I would like
#                to do a robustness test by taking out one state at a time
#                Perhaps there is one state that makes elevation or some other
#                variable look more important than it is
#                I'll need to study loops to do this