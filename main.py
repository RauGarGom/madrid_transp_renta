print("Importing libraries...")
import hashlib
import requests
import datetime
import pandas as pd
from utils import utils as ut


### Main data
print("Extracting data...")
df_transp_ind = pd.DataFrame(pd.read_excel("./data/raw/EDM2018INDIVIDUOS.xlsx", sheet_name = 'INDIVIDUOS'))
df_transp_trp = pd.DataFrame(pd.read_excel("./data/raw/EDM2018VIAJES.xlsx", sheet_name = 'VIAJES'))
df_weather=pd.DataFrame(pd.read_csv('./data/treated/aemet_weather.csv'))

### Transformations
print("Transforming data")
df_transp = ut.main_dfs_treat(df_transp_trp,df_transp_ind,df_weather)

print(df_transp.head(10))