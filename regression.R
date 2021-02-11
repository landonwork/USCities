library(corrgram)
library(stargazer)
library(car)

df = read.csv('C:/Users/lando/Desktop/Python/City Data/suicide-rate-by-county.csv')

corrgram(df, upper.panel = panel.pie, lower.panel = panel.pts)

# percent.female, median.age, high.school.education, obesity.rate,
# feel.bad, married, and lat are all highly positively correlated.
# Curious.

# The most promising predictors of suicide rates are, in order:
#      1. pop.density
#      2. elevation
#      3. poverty level
#      4. high.school.education
#      5. percent.female
#      6. median.age
#      7. lat
#      8. married
#      9. feel.bad
#     10. obesity.rate
#     11. student.population??? I doubt I would have been able to 
#         include an accurate representation of this variable in
#         the dataset, but I wish I could.

model <- lm(suicide.rate ~ pop.density+I(elevation/1000)+I(high.school.education*100)+I(percent.female*100)+median.age+lat+I(married*100)+I(feel.bad*100)+I(obesity.rate*100),data=df)
stargazer(model,type='text')

myH0 <- c('percent.female','lat','feel.bad')
linearHypothesis(model,myH0)
# (p-value: 0.4385)
# There is no reason to say that percent.female, lat, or feel.bad have
# any impact on the suicide rate

restricted_model = lm(suicide.rate ~ pop.density+I(elevation/1000)+I(high.school.education*100)+median.age+I(married*100)+I(obesity.rate*100),data=df)
stargazer(restricted_model,type='text')

# These results are crazy!
# There are three more things that I need to do now
#       1. I need to add in the other measures of education because those
#          are correlated
#       2. I need to rinse and repeat without the counties that have:
#             a. No entry from the CDC
#             b. The counties called "unreliable"
#             c. Without duplicate counties and cities (because there is
#                   no way to match them up with what I have)
#       3. Then I have to ask for advice about causality