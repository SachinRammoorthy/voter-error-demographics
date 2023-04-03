import pandas
from sklearn import linear_model

df = pandas.read_csv("regression_data.csv")

# X = df[['18_29', '30_44','45_64','65_','<9','9_12','high_school','college','associate','bachelor','grad','median_income','below_poverty']]
# X = df[['65_']]
X = df[['18_29','65_','grad','median_income','below_poverty']]
y = df['rate_overvote']
regr = linear_model.Ridge()
regr.fit(X.values, y.values)

predicted_rate_overvote = regr.predict([[0.8, 0.01, 0.8, 200000, 0.01]])
print(predicted_rate_overvote)
predicted_rate_overvote = regr.predict([[0.01, 0.8, 0.01, 30000, 0.3]])
print(predicted_rate_overvote)

# TODO: Logistic Regression, but would need to generate
# separate entries for each voter (overvote=0 or 1).
# Need a discrete space for the response variable

# TODO: divide dataset into training and testing data
# come up with accuracy metric for model
# 75-25 split

# correlation coefficient, pearson's correlation coefficient
# one correlation-number that we can calculate for all metrics

# r^2 - if we model age vs overvote as linear, then this is
    # how accurate that model is.

# correlation – does not look at models. Looks at the two datasets
    # and says whether they are correlated or not.

# z-test or p-test or t-test

# correlation coefficient