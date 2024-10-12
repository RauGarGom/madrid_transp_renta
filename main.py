print("Importing libraries...")
import pandas as pd
from utils import utils as ut



ut.data_extraction("./data/raw/EDM2018INDIVIDUOS.xlsx","./data/raw/EDM2018VIAJES.xlsx",'./data/treated/aemet_weather.csv','./data/treated/transp.csv')
df_transp = pd.read_csv("./data/treated/transp.csv")
print(df_transp.head(10))