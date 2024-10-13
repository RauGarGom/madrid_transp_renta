print("Importing libraries...")
import pandas as pd
from utils import utils as ut



ut.data_extraction("./data/raw/EDM2018INDIVIDUOS.xlsx","./data/raw/EDM2018VIAJES.xlsx",'./data/treated/aemet_weather.csv','./data/treated/transp.csv')
df_transp = pd.read_csv("./data/treated/transp.csv")
ut.pie_charts(['gender','week_day','transport','reason','activity','studies','weather'],df_transp)
ut.dry_rain(df_transp)
print(df_transp.head(10))