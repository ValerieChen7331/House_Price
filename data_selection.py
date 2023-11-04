import pandas as pd
import nums_from_string as nfs

#-------2_DataSelection----------
def drop_rows_purposes(df):
    #"住""都留，'國民住宅'不要
    print('Drop the rows, where the Purpose is not for living...')
    rows_to_drop = []
    setDropPurpose = set()
    setKeepPurpose = set()
    for index, row in df.iterrows():
        try:
            PurposeString = row['Purpose']
            setKeepPurpose.add(PurposeString)
            if '住' not in str(PurposeString) or '國民住宅' in str(PurposeString):
                rows_to_drop.append(index)
                setDropPurpose.add(PurposeString)
        except Exception as e:
            print(f"Purposes Error at index {index}: {e}")

    # Drop the specified rows
    df.drop(rows_to_drop, axis=0, inplace=True)
    df = df.reset_index(drop=True)
    print('Finish!')

    setKeepPurpose -= setDropPurpose
    print('保留項目: {}'.format(setKeepPurpose))
    print('刪除項目: {}'.format(setDropPurpose))
    return df

def drop_rows_type(df):
    # DropType
    print('Drop the rows, where the Type is not 公寓, 住宅大樓, 套房, 透天, 華廈...')
    rows_to_drop = []
    keywords = ['公寓', '住宅大樓', '套房', '透天', '華廈']
    for index, row in df.iterrows():
        try:
            TypeString = row['Type']
            if isinstance(TypeString, str) and not (any(keyword in TypeString for keyword in keywords)):
                rows_to_drop.append(index)
        except Exception as e:
            print(f"Type Error at index {i}: {e}")

    # Drop the specified rows
    df.drop(rows_to_drop, axis=0, inplace=True)
    df = df.reset_index(drop=True)
    print('Finish!')
    return df

def drop_rows_remarks(df):
    # 刪除"備註"有"親"的筆數
    print('Drop the Family Transaction rows...')
    setKeepFTString = set()
    setDropFTString = set()
    totalLength = len(df)

    rows_to_drop = []
    keywords = ['親', '父', '叔', '夫', '伯', '兄', '姪', '妻', '母', '婆', '朋友', '債務']
    for index, row in df.iterrows():
        try:
            FTString = row['Remarks']
            setKeepFTString.add(FTString)
            if isinstance(FTString, str) and any(keyword in FTString for keyword in keywords):
                rows_to_drop.append(index)
                setDropFTString.add(FTString)
        except Exception as e:
            print(f"Remarks Error at index {i}: {e}")

    # Drop the specified rows
    df.drop(rows_to_drop, axis=0, inplace=True)
    df = df.reset_index(drop=True)
    print('Finish!')

    setKeepFTString -= setDropFTString
    #查看刪除筆數和剩餘筆數
    print('Nums of Kept Strings: {}'.format(totalLength - len(rows_to_drop)))
    print('Nums of Deleted Strings: {}'.format(len(rows_to_drop)))
    #仍需辨識的筆數(存成set.csv)
    df_keep = pd.DataFrame({'Keep_Purpose': list(setKeepFTString)})
    df_keep.to_csv('purpose_set_keep.csv', index=False, encoding='utf-8-sig')
    df_drop = pd.DataFrame({'Drop_Purpose': list(setDropFTString)})
    df_drop.to_csv('purpose_set_drop.csv', index=False, encoding='utf-8-sig')
    return df

def merge_parking_area(df):
    print('合併"車位移轉總面積(平方公尺)"...')
    def parking(row):
        try:
            if pd.notnull(row['ParkingArea']):
                return row['ParkingArea']
            else:
                return row['ParkingArea_1']
        except Exception as e:
            print(f"ParkingArea Error at index {i}: {e}")
            return row['ParkingArea']

    # Apply to df['ParkingArea'], and drop the column 'ParkingArea_1'
    df['ParkingArea'] = df.apply(parking, axis=1)
    df.drop(columns=['ParkingArea_1'], axis=1, inplace=True)

    print('Finish!')
    print('整合後空值數量: {}'.format(len(df['ParkingArea']) - df['ParkingArea'].count()))
    return df

#-------word cloud----------
def remove_stop_words(file_name, seg_list):
    # 移除停用詞
    with open(file_name, 'r', encoding='utf-8') as f:  # Specify the encoding as 'utf-8'
        stop_words = f.readlines()
    stop_words = [stop_word.rstrip() for stop_word in stop_words]

    new_list = []

    for seg in seg_list:
        if seg not in stop_words:
            new_list.append(seg)
    return new_list

def count_segment_freq(seg_list):
    # 統計詞頻
    seg_df = pd.DataFrame(seg_list,columns=['seg'])
    seg_df['count'] = 1
    sef_freq = seg_df.groupby('seg')['count'].sum().sort_values(ascending=False)
    sef_freq = pd.DataFrame(sef_freq)
    return sef_freq
#------------------------------------
def urban_zoning(df):
    print('UrbanZoning...')
    cNUZ = 0
    cNUD = 0
    for i in range(len(df)):
        if pd.isnull(df.loc[i, 'UrbanZoning']) and pd.notnull(df.loc[i, 'NonUrbanZoning']):
            df.loc[i, 'UrbanZoning'] = 'NUZ_' + str(df.loc[i, 'NonUrbanZoning'])
            cNUZ += 1
        if pd.isnull(df.loc[i, 'UrbanZoning']) and pd.notnull(df.loc[i, 'NonUrbanDesignation']):
            df.loc[i, 'UrbanZoning'] = 'NUD_' + str(df.loc[i, 'NonUrbanDesignation'])
            cNUD += 1

    df.drop(['NonUrbanZoning', 'NonUrbanDesignation'], axis=1, inplace=True)
    print('Finish!')
    print(f"fill 'UrbanZoning' from 'NonUrbanZoning': {cNUZ} ")
    print(f"fill 'UrbanZoning' from 'NonUrbanDesignation': {cNUD} ")
    missing_values_count = len(df) - df['UrbanZoning'].count()
    print(f"Missing Value of 'UrbanZoning': {missing_values_count}")
    return df

def drop_price_null(df):
    #---------Drop TotalPrice = 0-------------
    print('Drop the rows, in which the TotalPrice/UnitPrice is null')
    rows_to_drop = []
    for index, row in df.iterrows():
        try:
            TotalPriceInt = row['TotalPrice']
            UnitPriceFloat = row['UnitPrice']
            if pd.isnull(TotalPriceInt) and pd.isnull(UnitPriceFloat):
                rows_to_drop.append(index)

        except Exception as e:
            print(f"Price Error at index {i}: {e}")

    # Drop the specified rows
    print('TotalPrice/UnitPrice both are null: {}'.format(len(rows_to_drop)))
    df.drop(rows_to_drop, axis=0, inplace=True)
    df = df.reset_index(drop=True)
    print('Finish!')
    return df

def building_layout(df):
    print('Bedrooms: 1-10, LivingRooms: 0-10, Bathrooms: 0-10')
    df = df[(df['Bedrooms'].astype(int) <= 10) & (df['Bedrooms'].astype(int) > 0)]
    df = df[(df['LivingRooms'].astype(int) <= 10)]
    df = df[(df['Bathrooms'].astype(int) <= 10)]
    #df = pd.get_dummies(df, columns=['Partitions'])
    #df = pd.get_dummies(df, columns=['Management'])
    return df
