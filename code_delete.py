import pandas as pd
import nums_from_string as nfs



def encoding_TF(df):
    # 要處理的col
    target_columns = ['Elevator', 'Management']
    # 編碼
    encoding_mapping = {
        '無': 0,
        '有': 1,
    }
    for target_column in target_columns:
        df[target_column] = df[target_column].replace(encoding_mapping)
    return df

def district_number(df, city):
    if city == 'tpe':
    # 編碼
        mapping = {'中正區': '100','大同區': '103','中山區': '104','松山區': '105','大安區': '106',
                   '萬華區': '108','信義區': '110','士林區': '111','北投區': '112','內湖區': '114',
                   '南港區': '115','文山區': '116'}
    if city == 'tph':
        mapping = {'萬里區': '207','金山區': '208','板橋區': '220','汐止區': '221','深坑區': '222',
                   '石碇區': '223','瑞芳區': '224','平溪區': '226','雙溪區': '227','貢寮區': '228',
                    '新店區': '231','坪林區': '232','烏來區': '233','永和區': '234','中和區': '235',
                    '土城區': '236','三峽區': '237','樹林區': '238','鶯歌區': '239','三重區': '241',
                    '新莊區': '242','泰山區': '243','林口區': '244','蘆洲區': '247','五股區': '248',
                    '新莊區': '248','八里區': '249','淡水區': '251','三芝區': '252','石門區': '253'}

    df['District'] = df['District'].replace(mapping)
    return df
def district_english(df, city):
    if city == 'tpe':
        mapping = {'中正區': 'Zhongzheng','大同區': 'Datong','中山區': 'Zhongshan','松山區': 'Songshan','大安區': 'Da_an',
                   '萬華區': 'Wanhua','信義區': 'Xinyi','士林區': 'Shilin','北投區': 'Beitou','內湖區': 'Neihu',
                   '南港區': 'Nangang','文山區': 'Wenshan'}
    if city == 'tph':
        mapping = {'207': 'Wanli','208': 'Jinshan','220': 'Banqiao','221': 'Xizhi','222': 'Shenkeng',
                   '223': 'Shiding','224': 'Ruifang','226': 'Pingxi','227': 'Shuangxi','228': 'Gongliao',
                    '231': 'Xindian','232': 'Pinglin','233': 'Wulai','234': 'Yonghe','235': 'Zhonghe',
                    '236': 'Tucheng','237': 'Sanxia','238': 'Shulin','239': 'Yingge','241': 'Sanchong',
                    '242': 'Xinzhuang', '243':'Taishan','244': 'Linkou','247': 'Luzhou','248': 'Wugu',
                    '249': 'Bali','251': 'Tamsui','252': 'Sanzhi','253': 'Shimen'}
    if city == 'tphc':
        mapping = {'萬里區': 'Wanli','金山區': 'Jinshan','板橋區': 'Banqiao','汐止區': 'Xizhi','深坑區': 'Shenkeng',
                   '石碇區': 'Shiding','瑞芳區': 'Ruifang','平溪區': 'Pingxi','雙溪區': 'Shuangxi','貢寮區': 'Gongliao',
                    '新店區': 'Xindian','坪林區': 'Pinglin','烏來區': 'Wulai','永和區': 'Yonghe','中和區': 'Zhonghe',
                    '土城區': 'Tucheng','三峽區': 'Sanxia','樹林區': 'Shulin','鶯歌區': 'Yingge','三重區': 'Sanchong',
                    '新莊區': 'Xinzhuang','泰山區': 'Taishan','林口區': 'Linkou','蘆洲區': 'Luzhou','五股區': 'Wugu',
                    '八里區': 'Bali','淡水區': 'Tamsui','三芝區': 'Sanzhi','石門區': 'Shimen'}

    df['District'] = df['District'].replace(mapping)
    return df
    
def fix_floor_err(df):
    df['Num_Floors'].replace('None', '', inplace=True)
    return df

def describe_dataframe(group, target_column):
    #查看 target_column，在不同'Type'中的資料分布
    all_data = {}
    for name, group_data in group:
        # Create a dictionary for each 'Type' group
        description = group_data[target_column].describe()
        type_data = {
            'count': description['count'],
            'mean': description['mean'],
            'std': description['std'],
            'min': description['min'],
            '25%': description['25%'],
            '50%': description['50%'],
            '75%': description['75%'],
            'max': description['max']
            }
        all_data[name] = type_data  # Assign 'type_data' dictionary to all_data using the 'Type' as key

    df_data = pd.DataFrame(all_data)
    return df_data

def unit_price_1(df):
    # UnitPrice
    print('UnitPrice...')
    count = 0

    def unit_price_null(row, count):
        if pd.isnull(row['UnitPrice']):
            unit_price = row['TotalPrice'] / row['TotalArea']
            count += 1
            print(count)
            return unit_price
        else:
            return row['UnitPrice']

    df['UnitPrice'] = df.apply(lambda row: unit_price_null(row, count), axis=1)
    print(f"Finish! {count} calculations were made.")
    return df

def drop_columns(df):
    # drop columns 刪除不需要的欄位
    print('Drop Columns')
    df = df.drop(columns=['Column1',
                        'Subject',
                        'TransactionDate',
                        'CompletionDate',
                        'Partitions',
                        'AuxiliaryArea',
                        'TransferNumber',
                        'TransactionDate_AD',
                        'Floor'], axis=1)
    return df

def address_misspelled(df):
    for i in range(len(df)):
        address_string = df.loc[i, 'Address_gis']
        road_string = df.loc[i, 'addr_road']
        short_string = df.loc[i, 'addr_short']

        print(df.loc[i, 'Address_gis'])
        # Remove punctuation marks
        if pd.notnull(df.loc[i, 'Address_gis']):
            df.loc[i, 'Address_gis'] = address_string.translate(str.maketrans('', '', string.punctuation))
        if pd.notnull(df.loc[i, 'Address_gis']):
            df.loc[i, 'addr_road'] = road_string.translate(str.maketrans('', '', string.punctuation))
        if pd.notnull(df.loc[i, 'addr_short']):
            df.loc[i, 'addr_short'] = short_string.translate(str.maketrans('', '', string.punctuation))

        print(df.loc[i, 'Address_gis'])
    print('Finish!')
    #if isinstance(FTString, str) and any(keyword in FTString for keyword in keywords):
    return df

def address_misspelled(df):
    punctuation_list = [' ', ',', '，', '、', '□', '?', ';', '；', ':', '：']
    for i in range(len(df)):
        road_string = df.loc[i, 'addr_road']

        if pd.notnull(road_string) and any(punctuation in road_string for punctuation in punctuation_list):
            print(i, road_string)

    print('Finish!')
    #if isinstance(FTString, str) and any(keyword in FTString for keyword in keywords):
    return df

def drop_rows(df, target_column, conditional_statement):
    rows_to_drop = []
    for i, row in df.iterrows():
        try:
            target_value = row[target_column]
            if conditional_statement:
                rows_to_drop.append(i)
        except Exception as e:
            print(f"Error at index {i}: {e}")

    # Drop the specified rows
    df.drop(rows_to_drop, axis=0, inplace=True)
    df = df.reset_index(drop=True)
    print('Finish! Dropped rows: {len(rows_to_drop)}')
    print('Kept rows: {len(df)}')
    return df
