print("Importing libraries...")
import pandas as pd
from utils import utils as ut



ut.main_data_extraction("./data/raw/EDM2018INDIVIDUOS.xlsx","./data/raw/EDM2018VIAJES.xlsx",'./data/treated/aemet_weather.csv','./data/treated/transp.csv')
df_transp = pd.read_csv("./data/treated/transp.csv")
df_gender_age, df_educ, df_occup = ut.aux_data_extraction()
ut.pie_charts(['gender','week_day','transport','reason','activity','studies','weather'],df_transp)
ut.dry_rain(df_transp)
df_transp = ut.income_assign(df_transp,df_educ,df_occup,df_gender_age)
print(df_transp.groupby('income')['id_indiv'].count()) ### Test that income assign works

### ANALYSIS: From the rain impact on transportation for workers we detect that there is no significant change 
### on their behaviour. However, the sample is rich enough so only dry days will be taken into account.

# Rain impact
df_weather = pd.read_csv("./data/output/weather.csv")
df_weather_work = pd.read_csv("./data/output/weather_work.csv")
ut.weather_change(df_weather,df_weather_work)
    # From the rain impact on transportation for workers we detect that there is no significant change 
    # on their behaviour. However, the sample is rich enough so only dry days will be taken into account.
print(df_transp.head(25))

### Analysis on income distribution
ut.income_dist(df_transp)

# Hypothesis 1:

df_transp_dry_work_main = df_transp[(df_transp["weather"] == "dry") & (df_transp["reason"] == "work") & (df_transp["transport"].isin(["car","public","walking"]))]
ut.hypo_1(df_transp_dry_work_main,jitter=True,n_obs=True)
#Hypothesis 2: