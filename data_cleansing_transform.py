import pandas as pd
import numpy as np
import nums_from_string as nfs
import math
import string   # house_age
from datetime import datetime   # house_age
import address_cleaning as ac

# 4-2.Floor
def floor_to_arabic(df):
    # Floor 改成樓層、層數、有無地下室
    print('Changing "Floor" to 3 columns: Floor_Arabic, Num_Floors, Basement...')
    df['Basement'] = False

    rows_to_drop = []
    try:
        for i in range(len(df)):
            floor_list = []
            num_floor = 0
            floorString = df.loc[i, 'Floor']

            # Step1. 如果樓層為空值，用Address來補值
            if pd.isnull(df.loc[i, 'Floor']):
                if pd.notnull(df.loc[i, 'addr_floor']):
                    addr_floor = str(df.loc[i, 'addr_floor'])
                    floorCut = nfs.get_nums(addr_floor)
                    floor_arabic = floorCut[-1]
                    num_floor = 1
                else:
                    floor_arabic = floorString  # 仍為空值
                    num_floor = floorString  # 為空值
                df.loc[i, 'Floor_Arabic'] = floor_arabic
                df.loc[i, 'Num_Floors'] = num_floor

            # Step2. 如果樓層文字為'全'，則 num_floor = floor_arabic = Storeys
            elif '全' in floorString:
                if pd.notnull(df.loc[i, 'Storeys']):
                    floor_arabic = int(df.loc[i, 'Storeys'])
                    num_floor = floor_arabic

                else:
                    continue
                df.loc[i, 'Floor_Arabic'] = floor_arabic
                df.loc[i, 'Num_Floors'] = num_floor

            # Step3. 如果樓層有文字，轉換樓層為阿拉伯數字(list)
            else:
                floorSplit = floorString.split('，')
                for floor in floorSplit:
                    if '地下' in floor:
                        df.loc[i, 'Basement'] = True
                        floor_list.append(0)
                        num_floor += 1
                    elif '層' in floor and not '夾層' in floor:
                        floor_list.append(ac.chinese_to_arabic(floor[:-1]))
                        num_floor += 1
                    else:
                        continue

                # 多層樓的交易，floor_arabic取平均數，小數點無條件進位
                if floor_list:
                    floor_arabic = math.ceil(sum(floor_list) / len(floor_list))
                else:
                    rows_to_drop.append(i)
                    print('非住宅房屋: {}, {}'.format(i, df.loc[i, 'Floor']))
                    floor_arabic = 999  # or any other default value you want to assign

                df.loc[i, 'Floor_Arabic'] = int(floor_arabic)
                df.loc[i, 'Num_Floors'] = int(num_floor)
    except:
        print('Floor Error: {}, {}'.format(i, floorString))
        rows_to_drop.append(i)


    print('刪除筆數: {}'.format(len(rows_to_drop)))
    df.drop(rows_to_drop, axis=0, inplace=True)
    df = df.reset_index(drop=True)
    print('保留總筆數: {}'.format(len(df)))
    return df

# 4-3.House Age
def house_age(df):
    print('Calculating HouseAge...')
    #error_count = 0
    df = df.apply(house_age_data, axis=1)

    print('Finish!')
    print(f"總筆數: {len(df)}")
    #print(f"error筆數: {error_count}")

    print(f"TransactionDate_AD 缺失值數量: {len(df) - df['TransactionDate_AD'].count()}")
    print(f"CompletionDate_AD 缺失值數量: {len(df) - df['CompletionDate_AD'].count()}")
    print(f"HouseAge 缺失值數量: {len(df) - df['HouseAge'].count()}")
    return df
#
def house_age_data(row):
    try:
        completionValue = row['CompletionDate']
        transactionValue = row['TransactionDate']

        # Convert Completion/Transaction Date from ROC to AD format
        completionString = comp_date_ad(completionValue)
        transactionString = trans_date_ad(transactionValue)

        # Calculate HouseAges(year)
        if completionString and transactionString:
            row['HouseAge'] = calculate_houseAge(completionString, transactionString)
        else:
            row['HouseAge'] = None

        #save
        if completionString:
            row['CompletionDate_AD'] = int(completionString[:6])
        if transactionString:
            row['TransactionDate_AD'] = int(transactionString[:6])

    except Exception as e:
        print(f"house_age_data Error: {e}")
        print('completion: {}, transaction {}'.format(completionValue, transactionValue))
        #error_count += 1
    return row
def comp_date_ad(completionValue):
    # Convert CompletionDate from ROC format to AD format
    if pd.notnull(completionValue):
        completionString = str(int(completionValue))

        if len(completionString) >= 6:
            completionString = str(int(completionString) + 19110000)

        elif len(completionString) == 5:
            if int(completionString[:3]) < 112:
                completionString = str(int(completionString[:3]) + 1911) + completionString[3:] + '01'

            else:
                completionString = str(int(completionString[:2]) + 1911) + '0601'

        elif len(completionString) == 4:
            completionString = str(int(completionString) + 191100) + '01'

        elif len(completionString) <= 2:
            completionString = str(int(completionString) + 1911) + '0601'

        else:
            completionString = None
    else:
        completionString = None
    return completionString
def trans_date_ad(transactionValue):
    # Convert TransactionDate from ROC format to AD format
    if pd.notnull(transactionValue):
        transactionString = str(transactionValue)

        if len(transactionString) >= 6:
            transactionString = str(int(transactionString) + 19110000)
        else:
            transactionString = None

        if transactionString[4:6] == "00":
            transactionString = transactionString[:4] + '0601'
        else:
            pass
    else:
        transactionString = None
    return transactionString
def calculate_houseAge(completionString, transactionString):
    # Calculate HouseAges(year)
    try:
        comp_datetime = datetime.strptime(completionString, '%Y%m%d').date()
        trans_datetime = datetime.strptime(transactionString, '%Y%m%d').date()
        houseAgeDays = trans_datetime - comp_datetime
        houseAgeYear = round(houseAgeDays.days / 365)
        return houseAgeYear
    except Exception as e:
        print(f"calculate_houseAge Error: {e}")
        print('completion: {}, transaction {}'.format(completionString, transactionString))
        return None
#
def transaction_filter(df, min_year):
    before_data = len(df)
    filtered_df = df[df['TransactionDate_AD'] >= min_year*100]
    print(f'Before delete: {before_data}')
    print(f'Drop: {before_data - len(filtered_df)}')
    print(f'After delete: {len(filtered_df)}')
    return filtered_df

# 4-5.NoT
def number_of_transactions(df):
    # 將"交易筆棟數(NoT)轉成3欄 (Num_Land, Num_Building, Num_ParkingSpace)
    print('Changing " 交易筆棟數" to 3 columns: Num_Land, Num_Building, Num_ParkingSpace...')
    iLand = []
    iBuilding = []
    iParkingSpace = []
    counter = 0
    try:
        NTCol = df.columns.get_loc('NumberOfTransactions')
        for i in range(len(df)):
            NTString = df.iloc[i, NTCol]
            #使用 get_nums() 函數
            number_list = nfs.get_nums(NTString)
            if number_list:
                iLand.append(number_list[0])
                iBuilding.append(number_list[1])
                iParkingSpace.append(number_list[2])
            else:
                iLand.append('0')
                iBuilding.append('0')
                iParkingSpace.append('0')
                counter +=1

        df.insert(NTCol+1, 'Num_Land', iLand)
        df.insert(NTCol+2, 'Num_Building', iBuilding)
        df.insert(NTCol+3, 'Num_ParkingSpace', iParkingSpace)
        df = df.drop(df.columns[NTCol], axis=1)
    except Exception as e:
        print(f"NoT Error at index {i}: {e}")

    print('Finish!')
    print(f"總筆數: {len(df)}")
    print(f"缺失值數量: {len(df) - df['Num_Land'].count()}")
    print(f"錯誤筆數: {counter}")
    return df
