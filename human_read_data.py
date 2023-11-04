import pandas as pd
import numpy as np
from datetime import datetime

def process_month_year(df):
    df = df.apply(month_year, axis=1)
    return df
def month_year(row):
    # CompletionDate
    if pd.notnull(row['CompletionDate_AD']):
        row['CompletionYear'] = int(row['CompletionDate_AD'] / 100)
        #row['CompletionMonth'] = int(str(row['CompletionDate_AD'])[4:6])
    # TransactionDate
    if pd.notnull(row['TransactionDate_AD']):
        row['TransactionYear'] = int(row['TransactionDate_AD'] / 100)
        row['TransactionMonth'] = int(str(row['TransactionDate_AD'])[4:6])
    return row

#-------------------------
def total_price_k(df):
    #TotalPrice_k
    print('TotalPrice_k...')
    df['TotalPrice'] = df['TotalPrice'].astype(float) / 1000
    df.rename(columns={'TotalPrice': 'TotalPrice(k)'}, inplace=True)
    return df
def square_meter_to_ping(df):
    df['UnitPrice_ping'] = df['TotalPrice'] / (df['TotalArea'] / 3.305785)
    df['TotalArea_ping'] = df['TotalArea'] / 3.305785
    return df
#------------------------
def reindex_columns_all(df):
    #all
    df = df.reindex(columns=[
        'Identifier',
        'Num_Land', 'Num_Building', 'Num_ParkingSpace',
        'Storeys', 'Floor_Arabic', 'Floor_Ratio', 'Num_Floors',
        'HouseAge', 'TransactionYear',
        'Bedrooms', 'LivingRooms', 'Bathrooms',
        'TotalArea', 'LandArea', 'PrimaryArea',
        'ParkingArea', 'BalconyArea',
        #-----surrounding (500m)------
        'Num_Garbage', 'Num_Hospital', 'Num_Metro',
        'Num_Railway', 'Num_Primary_School', 'Num_Sec_School',
        #----------nearest?-------------
        'Garbage_Station', 'Garbage_Dist', 'Hospital', 'Hospital_Dist',
        'Metro_Station', 'Metro_Dist', 'Railway', 'Railway_Dist',
        'Primary_School','Primary_Dist', 'Secondary_School', 'Sec_Dist',
        #-----type------
        'District',
        'Type',
        'ParkingSpaceType',
        'Purpose',
        'Material',
        'Elevator',
        'Management',
        #-----not ML------
        'CompletionDate_AD',
        'TransactionDate_AD',
        'Address',
        'Latitude',
        'Longitude',
        'Remarks',
        #-----Y------
        'TotalPrice',
        'UnitPrice',
        'ParkingSpacePrice',
        #-----Deleted-------
        'UrbanZoning',
        'NonUrbanZoning',
        'NonUrbanDesignation',
        ])
    return df

def reindex_columns_without_sur(df):
    # with coordinate but no surroundings
    df = df.reindex(columns=[
        #-----not ML 3------
        'Identifier',
        'Address',
        #'UrbanZoning',
        #-----Numarical 22-----------
        'Land', 'Building', 'ParkingSpace',
        'Storeys', 'Floor_Arabic', 'Num_Floors',
        'HouseAge', 'TransactionDate_AD', 'TransactionYear', 'TransactionMonth',
                    'CompletionDate_AD', 'CompletionYear', 'CompletionMonth',
        'Bedrooms', 'LivingRooms', 'Bathrooms',
        'TotalArea', 'LandArea', 'PrimaryArea', 'AuxiliaryArea',
        'ParkingArea', 'BalconyArea',
        #-----classification 5------
        'District',
        'Type',
        'Purpose',
        'Material',
        #-----Boolean 4-----
        'Elevator',
        'Management',
        'Basement',
        'Partitions',
        #-----Y 3------
        'TotalPrice',
        'UnitPrice',
        'ParkingSpacePrice'])
    return df

#-----------------------


#-----------------------
def material_encoding(df):
    #刪除 'x'
    df['Material'].replace('x', np.nan, inplace=True)
    df.dropna(subset=['Material'], inplace=True)
    # 編碼
    encoding_mapping = {
        'RB': int(1),     #加強磚造
        'RC': int(2),     #鋼筋混凝土
        'SRC': int(3),    #鋼骨鋼筋混凝土
        'SC': int(4)      #鋼骨結構
    }
    df['Material'] = df['Material'].replace(encoding_mapping)

    print('Finished material_encoding df.shape: {}'.format(df.shape))
    print('Finished material_encoding (len):{}',format(len(df)))
    return df
