import pandas as pd
import numpy as np
import nums_from_string as nfs
import string

# 3-6."地域環境"資料
def coordinates(df, cityname='tpe'):
    print('Convert Addresses to Latitude and Longitude...')
    # read the data downloaded from Post website
    post_file_name = {'tpe': 'data_gis_tpe/tpe_Address_Coords_GoogleEarth.csv'}
    data = pd.read_csv(post_file_name[cityname], low_memory=False)

    print('Before--df.shape: {}'.format(df.shape))
    #check if the Identifier is unique or not
    print('Duplicate IDs: {}'.format(len(data['Identifier']) - len(data['Identifier'].unique())))
    # drop the unnecessary columns
    data = data.drop(columns=['District', 'Address'], axis=1)
    # (left join) merge into the main dataFrame by the 'Identifier'
    df = pd.merge(left = df, right = data, how= 'left', on='Identifier', validate="1:1")

    print('Finish!')
    print('After--df.shape: {}'.format(df.shape))
    return df

def surroundings_500m(df, cityname='tpe'):
    print('Merge with Surrounding DataFrames (500m Radius)...')

    # The file names of Surrounding dataFrames (500m)
    data_fileName_500m = ['data_gis_tpe/TPE_NIMBY_500m.csv',
                     'data_gis_tpe/TPE_hospital_500m.csv',
                     'data_gis_tpe/TPE_metro_500m.csv',
                     'data_gis_tpe/TPE_railway_500m.csv',
                     'data_gis_tpe/TPE_primary_school_500m.csv',
                     'data_gis_tpe/TPE_secondary_school_500m.csv']

    # Change the columns' names for the main dataFrame after merging
    colName_list_500m = ['Num_NIMBY', 'Num_Hospital', 'Num_Metro', 'Num_Railway', 'Num_Primary_School', 'Num_Sec_School']
    zipped_datas_500m = zip(data_fileName_500m, colName_list_500m)

    print('Before--df.shape: {}'.format(df.shape))
    for fileName, colName in zipped_datas_500m:
        try:
            #import each Surrounding dataFrames (500m)
            data = pd.read_csv(fileName)
            #check if the Identifier is unique or not
            print('{} (number of duplicate IDs): {}'.format(colName, len(data['Identifier']) - len(data['Identifier'].unique())))
            # Change the columns' names
            data.rename(columns={'NUMPOINTS': colName}, inplace=True)
            # drop the unnecessary columns
            data = data.drop(columns=['District', 'Address', 'Latitude', 'Longitude'], axis=1)
            # (left join) merge into the main dataFrame by the 'Identifier'
            df = pd.merge(left = df, right = data, how= 'left', on='Identifier', validate="1:1")
        except:
            print('Surrounding Error, {}, {}',format(fileName, colName))

    print('Finish!')
    print('After--df.shape: {}'.format(df.shape))
    return df

def surroundings_nearest(df, cityname='tpe'):
    print('Merge with Surrounding DataFrames (Nearest)...')

    # The file names of Surrounding dataFrames (500m)
    data_fileName_nearest = ['data_gis_tpe/TPE_NIMBY_nearest.csv',
                            'data_gis_tpe/TPE_hospital_nearest.csv',
                            'data_gis_tpe/TPE_metro_nearest.csv',
                            'data_gis_tpe/TPE_railway_nearest.csv',
                            'data_gis_tpe/TPE_primary_school_nearest.csv',
                            'data_gis_tpe/TPE_secondary_school_nearest.csv']

    # Change the columns' names for the main dataFrame after merging
    colName_list_nearest = [('NIMBY_Station', 'NIMBY_Dist'),
                            ('Hospital', 'Hospital_Dist'),
                            ('Metro_Station', 'Metro_Dist'),
                            ('Railway', 'Railway_Dist'),
                            ('Primary_School','Primary_Dist'),
                            ('Secondary_School', 'Sec_Dist')]

    colName_1, colName_2 = zip(*colName_list_nearest)
    zipped_datas_nearest = zip(data_fileName_nearest, colName_1, colName_2)

    print('Before--df.shape: {}'.format(df.shape))
    for fileName, colName_1, colName_2 in zipped_datas_nearest:
        try:
            #import each Surrounding dataFrames (500m)
            data = pd.read_csv(fileName)
            # Change the columns' names
            data.rename(columns={'InputID': 'Identifier', 'TargetID': colName_1, 'Distance': colName_2}, inplace=True)
            #check if the Identifier is unique or not
            print('{} (number of duplicate IDs): {}'.format(colName_1, len(data['Identifier']) - len(data['Identifier'].unique())))
            # (left join) merge into the main dataFrame by the 'Identifier'
            df = pd.merge(left = df, right = data, how= 'left', on='Identifier', validate="1:1")
        except:
            print('Nearest Surrounding Error, {}',format(fileName))

    #print('before--df.shape: {}'.format(df.shape))
    #df.dropna(subset=['Num_NIMBY'], inplace=True)
    #df.dropna(subset=['NIMBY_Station'], inplace=True)
    print('Finish!')
    print('After--df.shape: {}'.format(df.shape))
    return df
