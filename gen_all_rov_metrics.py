import pandas as pd

df_age = pd.read_csv("results/age_rov.csv")
df_education = pd.read_csv("results/education_rov.csv")
df_income = pd.read_csv("results/income_rov.csv")
df_poverty = pd.read_csv("results/poverty_rov.csv")
df_sex = pd.read_csv("results/sex_rov.csv")

result = df_age.merge(df_education, on="precinct_id")
result = result.merge(df_income, on="precinct_id")
result = result.merge(df_poverty, on="precinct_id")
result = result.merge(df_sex, on="precinct_id")

result.to_csv("result.csv")