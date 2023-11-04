import pandas as pd
import nums_from_string as nfs

# 1. Data Profile
def change_cols_names(df):
    #修改欄位名稱
    df.rename(columns={'欄1': 'Column1',
    '鄉鎮市區':	'District',
    '交易標的': 'Subject',
    '土地位置建物門牌':	'Address',
    '土地移轉總面積平方公尺': 'LandArea',
    '都市土地使用分區': 'UrbanZoning',
    '非都市土地使用分區': 'NonUrbanZoning',
    '非都市土地使用編定': 'NonUrbanDesignation',
    '交易年月日': 'TransactionDate',
    '交易筆棟數': 'NumberOfTransactions',
    '移轉層次': 'Floor',
    '總樓層數': 'Storeys',
    '建物型態': 'Type',
    '主要用途': 'Purpose',
    '主要建材': 'Material',
    '建築完成年月': 'CompletionDate',
    '建物移轉總面積平方公尺': 'TotalArea',
    '建物現況格局-房': 'Bedrooms',
    '建物現況格局-廳': 'LivingRooms',
    '建物現況格局-衛': 'Bathrooms',
    '建物現況格局-隔間': 'Partitions',
    '有無管理組織': 'Management',
    '總價元': 'TotalPrice',
    '單價元平方公尺': 'UnitPrice',
    '車位類別': 'ParkingSpaceType',
    '車位移轉總面積(平方公尺)': 'ParkingArea',
    '車位總價元': 'ParkingSpacePrice',
    '備註': 'Remarks',
    '編號': 'Identifier',
    '主建物面積': 'PrimaryArea',
    '附屬建物面積':	'AuxiliaryArea',
    '陽台面積':	'BalconyArea',
    '電梯': 'Elevator',
    '移轉編號': 'TransferNumber',
    '車位移轉總面積平方公尺': 'ParkingArea_1'}, inplace=True)
    return df
def drop_eng_headers(df):
    # drop rows 刪除英文表頭(多筆重複)
    print('Drop English Headers...')
    rows_to_drop = []
    for index, row in df.iterrows():
        if row['Column1'] == 0:
            rows_to_drop.append(index)
    df = df.drop(rows_to_drop, axis=0)
    df = df.reset_index(drop=True)
    print(len(rows_to_drop))
    print('Finish!')
    return df

# Delete
def reindex_missingno(df):
    df = df.reindex(columns=[
        'Identifier',
        'Address_gis',
        'District',
        'Type',
        'UrbanZoning',
        'Purpose',
        'Material',

        'Num_Land',
        'Num_Building',
        'Num_ParkingSpace',
        'Storeys',
        'Floor_Arabic',
        'Num_Floors',
        'HouseAge',
        'CompletionDate_AD',
        'TransactionDate_AD',

        'Bedrooms',
        'LivingRooms',
        'Bathrooms',
        'Partitions',
        'LandArea',
        'TotalArea',
        'PrimaryArea',
        'AuxiliaryArea',
        'BalconyArea',
        'ParkingArea',

        'Elevator',
        'Management',
        'Basement',

        'TotalPrice',
        'UnitPrice',
        'ParkingSpacePrice'])
    return df

# 2. Data Selection
def reindex_columns(df):
    df = df.reindex(columns=[
        'Identifier',
        'Address',
        'District',
        'Type',
        'UrbanZoning',
        'Purpose',
        'Material',
        'NumberOfTransactions',
        'Storeys',
        'Floor',
        'CompletionDate',
        'TransactionDate',

        'Bedrooms',
        'LivingRooms',
        'Bathrooms',
        'Partitions',
        'LandArea',
        'TotalArea',
        'PrimaryArea',
        'AuxiliaryArea',
        'BalconyArea',
        'ParkingArea',
        'Elevator',
        'Management',

        'TotalPrice',
        'UnitPrice',
        'ParkingSpacePrice'])
    return df

#5 Data Exploration
def reindex_columns_all(df):
    # with coordinate but no surroundings
    df = df.reindex(columns=[
        #-----not ML 1------
        'Identifier',
        #-----Numarical 18-----------
        'Num_Land', 'Num_Building', 'Num_ParkingSpace',
        'Storeys', 'Floor_Arabic', 'Num_Floors',

        'HouseAge', 'CompletionDate_AD',
                    'TransactionDate_AD',

        'Bedrooms', 'LivingRooms', 'Bathrooms',
        'TotalArea', 'LandArea', 'PrimaryArea', 'AuxiliaryArea',
        'ParkingArea', 'BalconyArea',
        #-----classification 4------
        'District',
        'Type',
        'Purpose',
        'Material',
        #-----Boolean 4-----
        'Elevator',
        'Management',
        'Basement',
        'Partitions',
        #-----surrounding-----
        'Latitude',
        'Longitude',
        #-----500m-----
        'Num_NIMBY', 'Num_Hospital', 'Num_Metro',
        'Num_Railway', 'Num_Primary_School', 'Num_Sec_School',
        #-----nearest-----
        'NIMBY_Dist', 'Hospital_Dist', 'Metro_Dist',
        'Railway_Dist', 'Primary_Dist',  'Sec_Dist',
        #-----Y 3------
        'TotalPrice'])
        #-----Deleted Y ------
        #'UnitPrice', 'ParkingSpacePrice'
        #-----Deleted------
        #'Address', 'Address_gis', 'UrbanZoning',
        #'addr_floor', 'addr_short', 'Floor',
        #'CompletionDate', 'TransactionDate'
        #'NIMBY_Station', 'Hospital', 'Metro_Station',
        #'Railway','Primary_School','Secondary_School',

    return df

# 7. Noisy Data
def reindex_noisydata(df):
    # with coordinate but no surroundings
    df = df.reindex(columns=[
        #-----not ML 1------
        'Identifier',
        #-----Numarical 18-----------
        'Num_Land', 'Num_Building', 'Num_ParkingSpace',
        'Storeys', 'Floor_Arabic', 'Num_Floors',

        'HouseAge', 'CompletionYear',
        'TransactionDate_AD','TransactionYear','TransactionMonth',

        'Bedrooms', 'LivingRooms', 'Bathrooms',
        'TotalArea', 'LandArea', 'PrimaryArea', 'AuxiliaryArea',
        'ParkingArea', 'BalconyArea',
        #-----classification 4------
        'District',
        'Type',
        'Purpose',
        'Material',
        #-----Boolean 4-----
        'Elevator',
        'Management',
        'Basement',
        'Partitions',
        #-----surrounding-----
        'Latitude', 'Longitude',
        #-----500m-----
        'Num_NIMBY', 'Num_Hospital', 'Num_Metro',
        'Num_Railway', 'Num_Primary_School', 'Num_Sec_School',
        #-----nearest-----
        'NIMBY_Dist', 'Hospital_Dist', 'Metro_Dist',
        'Railway_Dist', 'Primary_Dist',  'Sec_Dist',
        #-----Y 3------
        'TotalPrice'])
        #-----Deleted Y ------
        #'UnitPrice', 'ParkingSpacePrice'
        #-----Deleted------
        #'Address', 'Address_gis', 'UrbanZoning',
        #'addr_floor', 'addr_short', 'Floor',
        #'CompletionDate', 'TransactionDate'
        #'NIMBY_Station', 'Hospital', 'Metro_Station',
        #'Railway','Primary_School','Secondary_School',

    return df
