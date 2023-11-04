import pandas as pd
import numpy as np
import nums_from_string as nfs
import string

# 3-1.文字清理
def address_text(df, cityName, cleanAddress):
    # 刪除缺失值
    missing_value = len(df['Address']) - df['Address'].count()
    print('缺失值數量: {}'.format(missing_value))
    if missing_value > 0:
        print('地址刪除缺失值...')
        df['Address'].replace('', np.nan, inplace=True) # for empty strings
        df.dropna(subset=['Address'], inplace=True)
        print('缺失值數量: {}'.format(len(df['Address']) - df['Address'].count()))

    # 計數
    count_city = 0; count_floor = 0;  count_con = 0;
    # 主程式
    print('Cleaning address text...')
    try:
        for i in range(len(df)):
            addressString = df.loc[i, 'Address']

            #全形轉半形
            addressString = full_to_half(addressString)
            # 統一使用"台"
            addressString = addressString.replace('臺', '台')

            # 補上District
            if (not '區' in addressString) or (('區街' in addressString) and (addressString.count('區') < 2)):
                addressString = df.loc[i, 'District'] + addressString
            # 補上City
            if not cityName in addressString:
                addressString = cityName + addressString
                count_city += 1

            if cleanAddress:
                # 清理地址，刪除"樓"之後的文字
                if '樓' in addressString:
                    addressLength = addressString.find('樓')
                    addressString = addressString[0: addressLength + 1]
                    count_floor += 1
                # 清理地址，刪除"及",";"之後的文字
                if '及' in addressString:
                    addressLength = addressString.find('及')
                    addressString = addressString[0: addressLength]
                    count_con += 1
                if ';' in addressString:
                    addressLength = addressString.find(';')
                    addressString = addressString[0: addressLength]
                    count_con += 1
            df.loc[i, 'Address'] = addressString

    except Exception as e:
        print(f"Address Format Error at index {i}: {e}")
        print(addressString)

    print('Finish!')
    print('Missing city: {},  Split_樓: {},  Split_及/;: {}'.format(count_city, count_floor, count_con))
    print('缺失值數量: {}'.format(len(df['Address']) - df['Address'].count()))
    return df
#
def full_to_half(text):
    import unicodedata
    result = ''
    for char in text:
        half_char = unicodedata.normalize('NFKC', char)
        result += half_char
    return result

# 3-2.統一地址格式
def address_creat_dataframe(df):
    print('Address Creat a dataframe and clean it...')
    data = parse_addr_data(df)
    data = format_address_numbers(data)
    data = segments_cleaner(data)
    print('Finish!')
    return data
#step1
def parse_addr_data(df):
    print('step1. Parse address data...')

    # Create an empty DataFrame to store processed data
    data = pd.DataFrame(columns=['identifier', 'orig_address', 'orig_district',
    'city', 'district', 'village', 'neighborhood', 'road', 'lane', 'alley', 'no', 'floor'])

    # Define keywords for address processing
    keywords_split = ['市', '區', '里', '鄰', '段', '路', '街', '大道', '巷', '弄', '號', '樓']
    road_to_chinese = ['段', '路', '街', '大道']

    # Dictionary to map keywords to DataFrame columns
    dictionary_address = {'市': 'city', '區': 'district', '里': 'village', '鄰': 'neighborhood',
                        '段': 'road', '路': 'road', '街': 'road', '大道': 'road',
                        '巷': 'lane', '弄': 'alley', '號': 'no', '樓': 'floor'}

    # Save columns from df to data
    data['identifier'] = df['Identifier']
    data['orig_address'] = df['Address']
    data['orig_district'] = df['District']

    for i in range(len(data)):
        address = data.loc[i, 'orig_address']
        try:
            # split "address" by keywords_split
            for keyword in keywords_split:
                if keyword in address:
                    temp = address.split(keyword, 1)
                    address = temp[1]
                    temp = temp[0] + keyword

                    # 存入data: 如果已有'段'的話，'路'就不需儲存
                    if (keyword in road_to_chinese) and (pd.notnull(data.loc[i, dictionary_address[keyword]])):
                        pass
                    # save tokenizations into data(frame)
                    else:
                        data.loc[i, dictionary_address[keyword]] = str(temp)

        except Exception as e:
            print('Error:', e)
            print(i, temp, address)

    data.drop(['village', 'neighborhood'], axis=1, inplace=True)
    data.to_csv('dataframe_addr.csv', encoding='utf-8-sig', index=False)
    print('finished step1')
    return data
#step2
def format_address_numbers(data):
    print('step2. Format address numbers (Chinese/Arabic)...')
    # Define columns for format_address_numbers
    to_arabic_columns = ['lane', 'alley', 'no', 'floor']

    for i, row in data.iterrows():
        # change arabic number to chinese number in "road" column
        road_string = row['road']
        if pd.notnull(road_string) and nfs.get_nums(road_string):
            road_number_list = nfs.get_nums(road_string)
            for number in road_number_list:
                number = str(number)
                chinese_number = arabic_to_chinese(number)
                road_string = road_string.replace(number, chinese_number)
            data.loc[i, 'road'] = road_string
        else:
            pass

        # change mix_numbers to arabic number (in "to_arabic_columns")
        for column_name in to_arabic_columns:
            column_string = row[column_name]
            if pd.notnull(column_string):
                column_string = mix_numbers_to_arabic(column_string)
                data.loc[i, column_name] = column_string

    print('finished step2')
    return data
def mix_numbers_to_arabic(temp):
    chinese_number_list = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九',
                                '壹', '貳', '叁', '肆', '伍', '陸', '柒', '捌', '玖',
                                '十', '百', '拾', '佰']
    cut = True
    for i, char in enumerate(temp):
        # 拆分數字 '1九' -> '1/九' -> '9'
        if char in chinese_number_list:
            if cut:
                word = char
                cut = False
                if (i > 0) and (nfs.get_nums(temp[i-1])):
                    temp = temp.replace(temp[i-1], (temp[i-1] + '/'))
                    i += 1
            elif not cut:
                word += char
        # change to arabic number
        elif not cut:
            arabic_number = chinese_to_arabic(word)
            temp = temp.replace(word, str(arabic_number))
            cut = True
        else:
            continue
    return temp
def chinese_to_arabic(chinese_number):
    chinese_number_map = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                 '壹': 1, '貳': 2, '叁': 3, '肆': 4,
        '伍': 5, '陸': 6, '柒': 7, '捌': 8, '玖': 9}

    powers_of_ten_map = {
        '十': 10, '百': 100, '拾': 10, '佰': 100}

    arabic_number = 0
    current_number = 1

    try:
        for char in chinese_number:
            if char in chinese_number_map:
                current_number = chinese_number_map[char]
            elif char in powers_of_ten_map:
                current_unit = current_number * powers_of_ten_map[char]
                arabic_number += current_unit
                current_number = 0
            else:
                print(f"Error! Invalid character: {char}")
                return
        arabic_number += current_number
    except Exception as e:
        print(f"Error! {e}")
    return arabic_number
def arabic_to_chinese(number):
    number_map = {
            '0': '零', '1': '一', '2':'二', '3':'三', '4':'四',
            '5':'五', '6':'六', '7':'七', '8':'八', '9':'九', '10': '十'}
    if number in number_map.keys():
        number = number_map[number]
    return number
#step3
def segments_cleaner(data):
    print('step3. Cleaning the text of each segments...')
    # creat two dictionaries of column 'no' and column 'floor'
    dict_no = {'column': 'no', 'get_number': 0, 'keyword': '號'}
    dict_floor = {'column': 'floor', 'get_number': -1, 'keyword': '樓'}
    dict_all = [dict_no, dict_floor]

    for i in range(len(data)):
        try:
            # 'no': 號只保留第一項: 3之4號 -> 3號, 4號之3 -> 4號
            # 'floor': 樓數只保留最後一項 (1至4樓, 之3/4樓, 11-4樓??)
            for dictionary in dict_all:
                column_name = dictionary['column']
                get_number = dictionary['get_number']
                keyword = dictionary['keyword']
                dict_string = data.loc[i, column_name]
                if pd.notnull(dict_string) and nfs.get_nums(dict_string):
                    data.loc[i, column_name] = str(nfs.get_nums(dict_string)[get_number]) + keyword
                else:
                    data.loc[i, column_name] = None

            # 刪除重複的"oo市oo區"
            road_duplicate_list = ['區', '北市']
            for keyword in road_duplicate_list:
                road_string = data.loc[i, 'road']
                if pd.notnull(road_string):
                    if (keyword in road_string) and (len(road_string) > 5):
                        road_list = road_string.split(keyword)
                        road_string = road_list[-1]
                        data.loc[i, 'road'] = str(road_string)

        except Exception as e:
            print('Error:', e)
            print(i)

    print('finished step3')
    return data
