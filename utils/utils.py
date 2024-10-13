import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    
    print("Merging databases...")
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
    

    # Indiv:
    ### Individual Survey - Date conversor for merge
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
    indiv = indiv[['id_indiv','gender','age','spanish','studies','activity','day','month','year','week_day','datemerge','tmed','prec']]

    #Trips:
    ### Trips Survey - Arranging ids, Column study / renaming / drop
    trip['id_indiv']=trip['ID_HOGAR'].astype(str) + trip['ID_IND'].astype(str)
    trip['id_trip']=trip['id_indiv'].astype(str) + trip['ID_VIAJE'].astype(str)
    trip.rename(columns={'VFRECUENCIA':'freq',
                                'VNOPUBLICO': 'no_public',
                                'MOTIVO_PRIORITARIO': 'reason',
                                'DISTANCIA_VIAJE': 'distance',
                                'ELE_G_POND_ESC2': 'trip_pond',
                                'VORIHORAINI': 'start_trip',
                                'MODO_PRIORITARIO': 'transport'},inplace=True)
    trip = trip[['id_indiv','id_trip','start_trip','transport','freq','reason','distance','trip_pond']]
    ### Merge of indivs and trips:
    transp = pd.merge(trip,indiv, on="id_indiv", how="left")

    ###Treatment of transp:
    ### Convert tmed and prec to float
    transp['tmed']=transp['tmed'].str.replace(",",".").astype(float)
    transp['prec']=transp['prec'].str.replace("Ip","0") ### We count rain of < 0.1 mm as dry weather.
    transp['prec']=transp['prec'].str.replace(",",".").astype(float)

    return transp

def transp_conversion(df_transp):
    ''' Converts the categorical info to text, so the content is more readable. It also
    creates a new column, "weather" ("dry" if <0.1mm, "rain" if else)
    '''
    ### Convert as strings so we can apply the effects of the lists. As soon as one value is str, the whole 
    ### series is converted into object
    print("Converting data...")
    df_transp['transport'] = df_transp['transport'].astype(str)
    df_transp['reason'] = df_transp['reason'].astype(str)
    df_transp['activity'] = df_transp['activity'].astype(str)
    df_transp['studies'] = df_transp['studies'].astype(str)
    df_transp['gender'] = df_transp['gender'].astype(str)
    df_transp['week_day'] = df_transp['week_day'].astype(str)

    #Transport:
    ''' 
    "public". Includes the original 1,2,3,4,5,6,7,8 and 9
    "taxi". Includes the original 10
    "car". Includes 11,12,13,14,15,16
    "motorbike". Includes 17,18,19
    "bike". Includes 20,21,22 
    "walking". Includes 23
    "other". Includes 24
    '''
    public = ["1","2","3","4","5","6","7","8","9"]
    taxi = ["10"]
    car = ["11","12","13","14","15","16"]
    motorbike = ["17","18","19"]
    bike = ["20","21","22"]
    walking = ["24"]
    other = ["23"]

    df_transp['transport'] = np.where(df_transp['transport'].isin(public), "public" ,df_transp['transport'])
    df_transp['transport'] = np.where(df_transp['transport'].isin(taxi), "taxi" ,df_transp['transport'])
    df_transp['transport'] = np.where(df_transp['transport'].isin(car), "car" ,df_transp['transport'])
    df_transp['transport'] = np.where(df_transp['transport'].isin(motorbike), "motorbike" ,df_transp['transport'])
    df_transp['transport'] = np.where(df_transp['transport'].isin(bike), "bike" ,df_transp['transport'])
    df_transp['transport'] = np.where(df_transp['transport'].isin(walking), "walking" ,df_transp['transport'])
    df_transp['transport'] = np.where(df_transp['transport'].isin(other), "other" ,df_transp['transport'])

    #Reason:
    '''
    "home". Includes the original 1 and 11.
    "work". Includes 2 and 3.
    "study". Includes 4.
    "leisure". Includes 8 and 9
    "personal". Includes 6,7,10
    "other". Includes 12.
    '''
    home = ["1","11"]
    work = ["2","3"]
    study = ["4"]
    leisure = ["8","9"]
    shopping = ["5"]
    personal = ["6","7","10"]
    other = ["12"]

    df_transp['reason'] = np.where(df_transp['reason'].isin(home), "home" ,df_transp['reason'])
    df_transp['reason'] = np.where(df_transp['reason'].isin(work), "work" ,df_transp['reason'])
    df_transp['reason'] = np.where(df_transp['reason'].isin(study), "study" ,df_transp['reason'])
    df_transp['reason'] = np.where(df_transp['reason'].isin(leisure), "leisure" ,df_transp['reason'])
    df_transp['reason'] = np.where(df_transp['reason'].isin(shopping), "shopping" ,df_transp['reason'])
    df_transp['reason'] = np.where(df_transp['reason'].isin(personal), "personal" ,df_transp['reason'])
    df_transp['reason'] = np.where(df_transp['reason'].isin(other), "other" ,df_transp['reason'])

    # Activity:
    '''
    "worker". Includes the original 1 and 2.
    "retired". Includes 3.
    "jobless". Includes 4,5,7 and 8
    "student". Includes 6
    "other". Includes 9
    '''
    worker = ["1","2"]
    jobless = ["4","5","7","8"]
    df_transp['activity'] = np.where(df_transp['activity'].isin(worker), "worker" ,df_transp['activity'])
    df_transp['activity'] = np.where(df_transp['activity'].isin(jobless), "jobless" ,df_transp['activity'])
    df_transp['activity'] = np.where(df_transp['activity'] == "3", "retired" ,df_transp['activity'])
    df_transp['activity'] = np.where(df_transp['activity'] == "6", "student" ,df_transp['activity'])
    df_transp['activity'] = np.where(df_transp['activity'] == "9", "other" ,df_transp['activity'])

    # Studies:
    '''
    "primary". Includes the original 1 and 2 (primary or less).
    "second1". Includes 3.
    "second2". Includes 4 and 5
    "superior". Includes 6 and 7
    '''
    primary = ["1","2"]
    second2 = ["4","5"]
    superior = ["6","7"]
    df_transp['studies'] = np.where(df_transp['studies'].isin(primary), "primary" ,df_transp['studies'])
    df_transp['studies'] = np.where(df_transp['studies'] == "3", "second1" ,df_transp['studies'])
    df_transp['studies'] = np.where(df_transp['studies'].isin(second2), "second2" ,df_transp['studies'])
    df_transp['studies'] = np.where(df_transp['studies'].isin(superior), "superior" ,df_transp['studies'])

    # Gender:
    df_transp['gender'] = np.where(df_transp['gender'] == "1", "male" ,"female")

    #Day of week:
    df_transp['week_day'] = np.where(df_transp['week_day'] == "1", "monday" ,df_transp['week_day'])
    df_transp['week_day'] = np.where(df_transp['week_day'] == "2", "tuesday" ,df_transp['week_day'])
    df_transp['week_day'] = np.where(df_transp['week_day'] == "3", "wednesday" ,df_transp['week_day'])
    df_transp['week_day'] = np.where(df_transp['week_day'] == "4", "thursday" ,df_transp['week_day'])
    
    #Weather - new variable from prec
    df_transp['weather'] = np.where(df_transp['prec'] < 0.1,"dry","rain")

    print("Data converted")
    return df_transp

def main_data_extraction(pth_indiv,pth_trip,pth_weather,pth_result):
    '''WARNING: Slow function, as the raw data is quite heavy. If it finds there is
    an already resulting csv, it stops.'''
    print("Extracting data...")
    if os.path.isfile(pth_result) == True:
        print(pth_result, "already exists")
    else:
        df_transp_ind = pd.DataFrame(pd.read_excel(pth_indiv, sheet_name = 'INDIVIDUOS'))
        df_transp_trp = pd.DataFrame(pd.read_excel(pth_trip, sheet_name = 'VIAJES'))
        df_weather=pd.DataFrame(pd.read_csv(pth_weather))
        df_transp = main_dfs_treat(df_transp_trp,df_transp_ind,df_weather) ### Merges the three dbs
        df_transp = transp_conversion(df_transp) ### Applies conversion on data.
        df_transp.to_csv("./data/treated/transp.csv",index_label=False)
        print("CSV on path", pth_result, "created")

def income_assign(df_main,df_educ,df_occup,df_gender_age):
    '''Income index contructor. Base level of 100, it gets multiplied by gender, age, education and activity, each adding 
    a base weight of 25'''
    print("Assigning income...")
    df_main['income'] = 100

    # Education
    df_main['income'] = np.where(df_main['studies'] == 'primary', df_main['income']+25*df_educ.iloc[0] ,df_main['income'])
    df_main['income'] = np.where(df_main['studies'] == 'second1', df_main['income']+25*df_educ.iloc[1] ,df_main['income'])
    df_main['income'] = np.where(df_main['studies'] == 'second2', df_main['income']+25*df_educ.iloc[2] ,df_main['income'])
    df_main['income'] = np.where(df_main['studies'] == 'superior', df_main['income']+25*df_educ.iloc[3] ,df_main['income'])

    # Activity
    df_main['income'] = np.where(df_main['activity'] == 'worker', df_main['income']+25*df_occup.iloc[0],df_main['income'])
    df_main['income'] = np.where(df_main['activity'] == 'student', df_main['income']+25*df_occup.iloc[3],df_main['income']) ###Students are counted as other inactive
    df_main['income'] = np.where(df_main['activity'] == 'retired', df_main['income']+25*df_occup.iloc[2],df_main['income'])
    df_main['income'] = np.where(df_main['activity'] == 'jobless', df_main['income']+25*df_occup.iloc[1],df_main['income'])
    df_main['income'] = np.where(df_main['activity'] == 'other', df_main['income']+25*df_occup.iloc[3],df_main['income'])

    #Gender, age
    df_main['income'] = np.where((df_main['gender'] == 'male') & (df_main['age'] < 16), df_main['income']+50*df_gender_age.iloc[0,0],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'male') & (df_main['age'] >= 16) & (df_main['age'] < 30), df_main['income']+50*df_gender_age.iloc[1,0],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'male') & (df_main['age'] >= 30) & (df_main['age'] < 45), df_main['income']+50*df_gender_age.iloc[2,0],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'male') & (df_main['age'] >= 45) & (df_main['age'] < 65), df_main['income']+50*df_gender_age.iloc[3,0],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'male') & (df_main['age'] >= 65), df_main['income']+50*df_gender_age.iloc[4,0],df_main['income'])

    df_main['income'] = np.where((df_main['gender'] == 'female') & (df_main['age'] < 16), df_main['income']+50*df_gender_age.iloc[0,1],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'female') & (df_main['age'] >= 16) & (df_main['age'] < 30), df_main['income']+50*df_gender_age.iloc[1,1],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'female') & (df_main['age'] >= 30) & (df_main['age'] < 45), df_main['income']+50*df_gender_age.iloc[2,1],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'female') & (df_main['age'] >= 45) & (df_main['age'] < 65), df_main['income']+50*df_gender_age.iloc[3,1],df_main['income'])
    df_main['income'] = np.where((df_main['gender'] == 'female') & (df_main['age'] >= 65), df_main['income']+50*df_gender_age.iloc[4,1],df_main['income'])
    print("Income assigned")
    return df_main

def pie_charts(pies,df):
    ''' Generates pie charts of the columns included in a "pies" list, from the "df"
    dataframe'''
    print("Generating pie charts...")
    for pie in pies:
        plt.figure()
        plt.pie(df[pie].value_counts().values, labels = df[pie].value_counts().index,autopct='%1.1f%%')
        plt.savefig("./img/plots/pies/"+pie+"_distrib.png")
    print("Pie charts generated in /img/plots/pies")

def dry_rain (df):
    ''' Generates a csv with a comparison of usage of transportation and weather'''
    print("Generating dry/rain comparison")
    dry_work_filter = (df['weather']=="dry") & (df['reason']=="work")
    rain_work_filter = (df['weather']=="rain") & (df['reason']=="work")
    dry_work = round(df[dry_work_filter].groupby('transport')["id_indiv"].count()/len(df[dry_work_filter])*100,1)
    rain_work = round(df[rain_work_filter].groupby('transport')["id_indiv"].count()/len(df[rain_work_filter])*100,1)
    weather_work = pd.concat([dry_work,rain_work],axis=1,keys=["dry","rain"])
    weather_work['difference'] = round(weather_work['dry']-weather_work['rain'],1)
    weather_work.to_csv("./data/output/weather_work.csv",index_label=False)
    print("Dry/rain comparison saved on data/output/weather_work.csv")

def aux_data_extraction():
    ''' Extracts different incomes (gender, age, education, occupation) and returns normalized indexes in dataframes'''
    print("Extracting auxiliary data...")
    # Gender and age, single dataframe
    df_men_age = pd.DataFrame(pd.read_excel("./data/raw/ecv19.xlsx", sheet_name="2.1.1",skiprows=19,index_col=1,nrows=5,header=None))
    df_women_age = pd.DataFrame(pd.read_excel("./data/raw/ecv19.xlsx", sheet_name="2.1.1",skiprows=26,index_col=1,nrows=5,header=None))
    df_gender_age = pd.concat([df_men_age.iloc[:,1],df_women_age.iloc[:,1]],axis=1, keys=["men","women"])
    df_gender_age = round(((df_gender_age-np.nanmean(df_gender_age))/np.nanstd(df_gender_age)+1),2) ### np.nanmean takes the mean of the whole df
    df_gender_age

    # Education
    df_educ = pd.DataFrame(pd.read_excel("./data/raw/ecv19.xlsx", sheet_name="2.1.2",skiprows=11,index_col=1,nrows=4,header=None)).iloc[:,1]
    df_educ = round(((df_educ-df_educ.mean())/df_educ.std()+1),2)
    df_educ

    # Occupation
    df_occup = pd.DataFrame(pd.read_excel("./data/raw/ecv19.xlsx", sheet_name="2.1.3",skiprows=11,index_col=1,nrows=4,header=None)).iloc[:,1]
    df_occup = round(((df_occup-df_occup.mean())/df_occup.std()+1),2)
    df_occup
    print("Auxiliary data extracted")
    return df_gender_age,df_educ,df_occup
