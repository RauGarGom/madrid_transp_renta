import requests
import pandas as pd
import os

def retrieve_aemet(url,data_destination):
    ''' This function retrieves data to be used as weather. url has to be given by AEMET
    (https://opendata.aemet.es/centrodedescargas/inicio), and data_destination will be the
    path where the resulting csv will be stored.'''
    res = requests.get(url)
    weather = res.json()
    weather = pd.DataFrame(weather)
    weather.to_csv(data_destination)

def main_dfs_treat(trip,indiv,weather):
    ''' Ensembles the required data in order to extract the main database. From a weather, 
    individuals and trips database, it returns a merged and more treatable dataframe.'''
    
    print("Transforming data")
    # Weather:
    weather['datemerge'] = weather['fecha'].str.split("-")
    weather['datemerge']
    ### Expanding to three new colums
    weather [['year','month','day']] = pd.DataFrame(weather.datemerge.tolist(), index = weather.index)
    ### Drops of 0s on month and day
    weather['month'] = weather['month'].str.replace("0","")
    weather['day'] = weather['day'].str[0].replace("0","")+weather['day'].str[1]
    weather['day'].head(50)
    ### Concatenate year, month, day
    weather['datemerge'] = weather['year']+"-"+weather['month']+"-"+weather['day']

    ### Indiv:
    # Individual Survey - Date conversor for merge
    indiv['datemerge'] = indiv['DANNO'].astype(str) + '-' + indiv['DMES'].astype(str) + '-' + indiv['DDIA'].astype(str)
    ### Concatenate columns so we get an unique id
    indiv['id_indiv']=indiv['ID_HOGAR'].astype(str) + indiv['ID_IND'].astype(str)
    indiv.head()
    ### Merge of transp indiv and weather
    weather_merge = weather[['datemerge','tmed','prec']]
    indiv = pd.merge(indiv,weather_merge, on = 'datemerge', how = 'left')
    ### Indv Survey - Column study / renaming / drop
    indiv.rename(columns={'C2SEXO' : 'gender',
                            'EDAD_FIN' : 'age',
                            'ELE_G_POND' : 'indiv_pond',
                            'C4NAC' : 'spanish',
                            'C7ESTUD' : 'studies',
                            'C8ACTIV' : 'activity',
                            'DDIA' : 'day',
                            'DMES' : 'month',
                            'DANNO' : 'year',
                            'DIASEM' : 'week_day',}, inplace=True)
    indiv = indiv[['id_indiv','gender','age','spanish','studies','activity','day','month','year','datemerge','tmed','prec']]

    ###Trips:
    ### Trips Survey - Arranging ids, Column study / renaming / drop
    trip['id_indiv']=trip['ID_HOGAR'].astype(str) + trip['ID_IND'].astype(str)
    trip['id_trip']=trip['id_indiv'].astype(str) + trip['ID_VIAJE'].astype(str)
    trip.rename(columns={'VFRECUENCIA':'freq',
                                'VNOPUBLICO': 'no_public',
                                'MOTIVO_PRIORITARIO': 'reason',
                                'DISTANCIA_VIAJE': 'distance',
                                'ELE_G_POND_ESC2': 'trip_pond',
                                'VORIHORAINI': 'start_trip'},inplace=True)
    trip = trip[['id_indiv','id_trip','start_trip','freq','reason','distance','trip_pond']]
    ### Merge of indivs and trips:
    transp = pd.merge(trip,indiv, on="id_indiv", how="left")

    return transp

def data_extraction(pth_indiv,pth_trip,pth_weather,pth_result):
    # TODO: Any way of inserting this on utils without messing up the paths? Maybe
    # giving the paths as arguments?
    '''WARNING: Slow function, as the raw data is quite heavy. If it finds there is
    an already resulting csv, it stops.'''
    print("Extracting data...")
    if os.path.isfile(pth_result) == True:
        print(pth_result, "already exists")
    else:
        df_transp_ind = pd.DataFrame(pd.read_excel(pth_indiv, sheet_name = 'INDIVIDUOS'))
        df_transp_trp = pd.DataFrame(pd.read_excel(pth_trip, sheet_name = 'VIAJES'))
        df_weather=pd.DataFrame(pd.read_csv(pth_weather))
        df_transp = main_dfs_treat(df_transp_trp,df_transp_ind,df_weather)
        df_transp.to_csv("./data/treated/transp.csv",index_label=False)
        print("CSV on path", pth_result, "created")