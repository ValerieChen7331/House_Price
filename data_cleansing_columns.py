import pandas as pd
import numpy as np
import nums_from_string as nfs
import address_cleaning as ac

# 4-1.Storeys
def storeys_to_arabic(df):
    print('Converting "Storeys" from str to int...')
    def clean_storeys(row):
        try:
            storeys = row['Storeys']
            if pd.notnull(storeys):
                storeys = str(storeys)
                if nfs.get_nums(storeys):
                    number = nfs.get_nums(storeys)
                    return int(number[0])
                else:
                    return ac.chinese_to_arabic(storeys[0:-1])
            elif (pd.notnull(row['addr_floor'])) and (pd.notnull(row['Floor'])):
                if '全' in row['Floor']:
                    floorCut = nfs.get_nums(str(row['addr_floor']))
                    storeys = floorCut[-1]
                    return int(storeys)
                else:
                    return None
            else:
                return None

        except ValueError as e:
            print('Storeys Error: {}'.format(e))
            return None

    df['Storeys'] = df.apply(clean_storeys, axis=1)
    print('Finish!')
    # 缺失值數量
    print(f"總筆數: {len(df)}")
    print(f"Storeys 缺失值數量: {len(df) - df['Storeys'].count()}")
    return df

# 4-4.Elevator
def elevator_null_1(df):
    # 電梯補植
    print('Extracting "Elevator" information from the "Type" column...')
    def elevator(row):
        try:    # check 'Elevator'
            if pd.notnull(row['Elevator']):
                return '有' in row['Elevator']
            else:   # check 'Type'
                return '有' in row['Type']
        except Exception as e:
            print(f"Error at index {i}: {e}")

    row['Elevator'] = df.apply(elevator, axis=1)
    print('Finish!')
    print('總筆數: {}'.format(len(df)))
    print('缺失值數目: {}'.format(len(df)-df['Elevator'].count()))
    return df
def elevator_null(df):
    # 電梯補植
    print('Extracting "Elevator" information from the "Type" column...')
    df['Elevator'] = df.apply(elevator, axis=1)
    print('Finish!')
    print('總筆數: {}'.format(len(df)))
    print('缺失值數目: {}'.format(len(df) - df['Elevator'].count()))
    return df
def elevator(row):
    try:
        if pd.notnull(row['Elevator']):
            return '有' in row['Elevator']
        elif pd.notnull(row['Type']):
            return '有' in row['Type']
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
def clean_type(df):
    print('Removing \'(text)\' in the "Type" column...')
    def clean_types(types):
        if isinstance(types, str):
            typesLength = types.find('(')
            types = types[:typesLength]
        return types
    df['Type'] = df['Type'].apply(clean_types)
    print('Finish!')
    print(f"總筆數: {len(df)}")
    print(f"Type 缺失值數量: {len(df) - df['Type'].count()}")
    return df

# 4-6.Material
def material(df):
    print('Categorizing "Material" into five categories: SC, SRC, RC, RB, Others...')
    target_column = 'Material'

    # 鋼構.鋼骨.鋼筋.加強磚分類
    for index, row in df.iterrows():
        try:
            value = str(row[target_column])
            if '構' in value:    #鋼構 Steel Construction, 價格高
                df.at[index, target_column] = 'SC'
            elif '骨' in value:  #鋼骨鋼筋混凝土 Steel Reinforced Concrete, 中
                df.at[index, target_column] = 'SRC'
            elif '筋' in value:  #鋼筋混凝土 Reinforced Concrete, 低
                df.at[index, target_column] = 'RC'
            elif '加強磚' in value: # 加強磚造 reinforced brick, 最便宜
                df.at[index, target_column] = 'RB'
            else:
                df.at[index, target_column] = 'Others'
        except Exception as e:
            print(f"NoT Error at index {i}: {e}")
    print('Finish!')
    print(f"總筆數: {len(df)}")
    print(f"缺失值數量: {len(df) - df[target_column].count()}")
    return df

# 4-7.UnitPrice/ District
def unit_price(df):
    print('Calculating the missing values of UnitPrice...')
    count = 0
    for i in range(len(df)):
        if pd.isnull(df.loc[i, 'UnitPrice']):
            df.loc[i, 'UnitPrice'] = df.loc[i, 'TotalPrice'] / df.loc[i, 'TotalArea']
            count += 1
    print(f"Finish! Calculated unitPrice: {count}")
    return df
def district_english(df, city):
    if city == 'tpe':
        mapping = {'中正區': 'Zhongzheng','大同區': 'Datong','中山區': 'Zhongshan','松山區': 'Songshan','大安區': 'Da_an',
                   '萬華區': 'Wanhua','信義區': 'Xinyi','士林區': 'Shilin','北投區': 'Beitou','內湖區': 'Neihu',
                   '南港區': 'Nangang','文山區': 'Wenshan'}

    if city == 'tph':
        mapping = {'萬里區': 'Wanli','金山區': 'Jinshan','板橋區': 'Banqiao','汐止區': 'Xizhi','深坑區': 'Shenkeng',
                   '石碇區': 'Shiding','瑞芳區': 'Ruifang','平溪區': 'Pingxi','雙溪區': 'Shuangxi','貢寮區': 'Gongliao',
                    '新店區': 'Xindian','坪林區': 'Pinglin','烏來區': 'Wulai','永和區': 'Yonghe','中和區': 'Zhonghe',
                    '土城區': 'Tucheng','三峽區': 'Sanxia','樹林區': 'Shulin','鶯歌區': 'Yingge','三重區': 'Sanchong',
                    '新莊區': 'Xinzhuang','泰山區': 'Taishan','林口區': 'Linkou','蘆洲區': 'Luzhou','五股區': 'Wugu',
                    '八里區': 'Bali','淡水區': 'Tamsui','三芝區': 'Sanzhi','石門區': 'Shimen'}

    df['District'] = df['District'].replace(mapping)
    return df

# 4-8.Partitions
def partitions(df):
    # 將 "有/無" 轉為 "True/False"
    print('Converting "Partitions" from str to bool...')
    target_column = 'Partitions'
    df[target_column] = df[target_column].apply(string_to_boolean)
    print('Finish!')
    return df
def management(df):
    # 將 "有/無" 轉為 "True/False"
    print('Converting "Management" from str to bool...')
    target_column = 'Management'
    df[target_column] = df[target_column].apply(string_to_boolean)
    print('Finish!')
    return df
def string_to_boolean(target):
    try:
        if '有' in target:
            return True
        elif '無' in target:
            return False
        else:
            return None
    except Exception as e:
        print(f"Error: {e}, {target}")
        return None
