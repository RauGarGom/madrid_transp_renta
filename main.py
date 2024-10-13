print("Importing libraries...")
import pandas as pd
from utils import utils as ut



ut.main_data_extraction("./data/raw/EDM2018INDIVIDUOS.xlsx","./data/raw/EDM2018VIAJES.xlsx",'./data/treated/aemet_weather.csv','./data/treated/transp.csv')
df_transp = pd.read_csv("./data/treated/transp.csv")
df_gender_age, df_educ, df_occup = ut.aux_data_extraction()
ut.pie_charts(['gender','week_day','transport','reason','activity','studies','weather'],df_transp)
ut.dry_rain(df_transp)
df_transp=ut.income_assign(df_transp,df_educ,df_occup,df_gender_age)
print(df_transp.groupby('income')['id_indiv'].count()) ### Test that income assign works

### ANALYSIS: From the rain impact on transportation for workers we detect that there is no significant change 
### on their behaviour. However, the sample is rich enough so only dry days will be taken into account.
# df_transp_dry = df_transp[df_transp["weather"] == "dry"]
# print(df_transp_dry.info())