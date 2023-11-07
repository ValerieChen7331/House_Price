import pandas as pd
import numpy as np
import nums_from_string as nfs
import string

# 3-3.找出錯誤資訊
def address_district_error(data):
    # Correct 'District' errors using postal data
    print('Find the rows where "District" and "addr_district" do not match...')
    rows_disError = []
    c_list = [0, 0, 0, 0]
    dict_road = make_dict_road('tpe')
    for i, row in data.iterrows():
        if row['orig_district'] != row['district']:
            rows_disError.append(i)
            data.loc[i, 'district'], c_list = verify_postal_districts(row, dict_road, c_list)

    data.drop(columns=['orig_district'], inplace=True)

    print('Finish!')
    print(f"district_error count: {len(rows_disError)}")
    print(f'post: {c_list[0]}, orig: {c_list[1]}, addr: {c_list[2]}, unknown: {c_list[3]}')
    return data
#
def make_dict_road(cityname='tpe'):
    print('step1. Making dict_road...')
    dict_road = {}
    district_list = []

    # read the data downloaded from Post website
    post_file_name = {'tpe': 'data/post_district_road_tpe.csv'}
    data = pd.read_csv(post_file_name[cityname], low_memory=False)

    road_group = data.groupby('road')
    # save a dictionary {road: [district1,district2]}
    for road_name, group_data in road_group:
        district_list = group_data['district'].unique().tolist()
        dict_road[road_name] = district_list

    print('finish step1')
    return dict_road
def verify_postal_districts(row, dict_road, c_list):
    #print('verify_postal_districts...')
    # Count the number of corrected districts
    c_post = c_list[0]; c_orig = c_list[1]
    c_addr = c_list[2]; c_unknow = c_list[3]

    try:
        orig_district = row['orig_district']
        addr_district = row['district']
        road_name = row['road']

        if pd.notnull(road_name):
            post_district_list = dict_road[road_name]

            if (orig_district in post_district_list) and not (addr_district in post_district_list):
                verified_district = orig_district
                c_orig += 1
            elif (addr_district in post_district_list) and not (orig_district in post_district_list):
                verified_district = addr_district
                c_addr += 1
            elif len(post_district_list) == 1:
                verified_district = post_district_list[0]
                c_post += 1
            else:
                # 暫時先以'orig_district'帶入，因台北市267中，已知(orig: 247, addr: 2, UNKnow: 16)
                # 之後可以用爬蟲修改(待完成...)
                verified_district = orig_district
                c_unknow += 1
        else:
            verified_district = None

    except Exception as e:
        print(f'Error: {e}')
        print(row['orig_district'], row['district'], row['road'])
        verified_district = None

    #print('Finish!')
    c_list = [c_post, c_orig, c_addr, c_unknow]
    return (verified_district, c_list)

# 3-4.無法判讀的資料 (錯字)
def address_misspelled(data):
    print('Correcting the misspelled road names...')
    data = gongguan_rd_st(data)
    dict_district = make_dict_district('tpe')
    data = correcting_road_names(data, dict_district)
    print('Finish!')
    return data
#step1
def gongguan_rd_st(data):
    print('step1. Formatng "公舘路" and "公館街"...')
    for i in range(len(data)):
        road_string = data.loc[i, 'road']
        if pd.notnull(road_string):
            if (road_string[0] == '公') and (road_string[-1] == '路'):
                data.loc[i, 'road'] = '公舘路'
                data.loc[i, 'district'] = '北投區'
            elif (road_string[0] == '公') and (road_string[-1] == '街'):
                data.loc[i, 'road'] = '公館街'
                data.loc[i, 'district'] = '文山區'
    print('finish step1!')
    return data
#step2
def make_dict_district(cityname='tpe'):
    print('step2. Make a dictionary of districts...')
    dict_district = {}
    road_list = []
    # read the data downloaded from Post website
    post_file_name = {'tpe': 'data/post_district_road_tpe.csv'}
    data = pd.read_csv(post_file_name[cityname], low_memory=False)

    district_group = data.groupby('district')

    for district_name, group_data in district_group:
        road_list = group_data['road'].unique().tolist()
        dict_district[district_name] = road_list

    print('finish step2!')
    return dict_district
#step3
def correcting_road_names(data, dict_district):
    print('step3. Find the correct road names...')

    #'軍功路'更名為'和平東路四段'
    data['road'].replace('軍功路', '和平東路四段', inplace=True)

    # 門街, 門?街, 復興南路 二 段
    punctuation_list = ['?m', 'm',' ','', '','', '○', '}', '', ',', '，', '、', '□', '?', ';', '；', ':', '：']
    #if pd.notnull(road_string) and any(punctuation in road_string for punctuation in punctuation_list):
    for i, row in data.iterrows():
        road_string = row['road']
        if pd.notnull(road_string):
            correct_road_name = road_string
            for punctuation in punctuation_list:
                if punctuation in road_string:
                    # remove punctuation, save road_string as a list ('門?街'->['門','街'])
                    road_string_list = road_string.split(punctuation)
                    post_roads_list = dict_district[row['district']]
                    # find the correct road name in post dictionary
                    correct_road_name = find_road_name(road_string_list, post_roads_list)
                    if correct_road_name:
                        #print(road_string, correct_road_name)
                        break
                    else:
                        # for '?公?路' -> ['','公?路'] -> ['公?路']
                        road_string = road_string_list[-1]
            data.loc[i, 'road'] = correct_road_name
    print('finish step3!')
    return data
def find_road_name(road_string_list, post_roads_list):
    #print(road_string_list)
    for road_name in post_roads_list:
        c = False
        for char in road_string_list:
            if char in road_name:
                c = True
            else:
                c = False
                break
        if c:
            return road_name
    #print(road_string_list)
    #print('Not found!')
    return None
#step4 (check)
def find_not_post(data, cityname='tpe'):
    print('Check the roads not in postal data...')
    rows_to_check = []
    rows_to_check_list = []
    # read the data downloaded from Post website
    post_file_name = {'tpe': 'data/post_district_road_tpe.csv'}
    data_road = pd.read_csv(post_file_name[cityname], low_memory=False)
    all_roads = data_road['road'].unique()

    for i in range(len(data)):
        road_string = data.loc[i, 'road']
        if pd.notnull(road_string):
            if road_string not in all_roads:
                rows_to_check.append(i)
                rows_to_check_list.append(road_string)

    print(f"unique roads to be checked: {len(set(rows_to_check_list))}")
    print(f"total number of rows to be checked: {len(rows_to_check)}")
    data_check = data.iloc[rows_to_check]
    data_check.to_csv('data_check.csv', encoding='utf-8-sig', index=False)
    print('Finish. Save the datas as data_check.csv')
    return rows_to_check, rows_to_check_list
# step5
def misspelled_roads(data):
    print('Correcting the misspelled roads...')

    #'軍功路'更名為'和平東路四段'
    data['road'].replace('軍功路', '和平東路四段', inplace=True)

    # 錯字更正
    for i in range(len(data)):
        road_string = data.loc[i, 'road']
        if pd.notnull(road_string):
            road_string = road_string.replace('ㄧ', '一')
            road_string = road_string.replace('錦洲', '錦州')
            road_string = road_string.replace('汀洲', '汀州')
            road_string = road_string.replace('溪州', '溪洲')
            road_string = road_string.replace('福洲', '福州')
            # save 'road_string' into the data
            data.loc[i, 'road'] = road_string

    print('finish step5')
    return data

# 3-5.合併與統整
def address_format_to_all(df, data):
    print('Address format...')

    # Address final format
    final_format = ['city', 'district', 'road', 'lane', 'alley', 'no']
    short_format = ['road', 'lane', 'alley', 'no']

    # save 'format_address' in data
    data['format_address'] = data[final_format].apply(lambda x: ''.join(x.dropna()), axis=1)
    data['short_address'] = data[short_format].apply(lambda x: ''.join(x.dropna()), axis=1)

    # save the format datas from data to df
    df['Address_gis'] = data['format_address']
    df['addr_district'] = data['district']
    df['addr_road'] = data['road']
    df['addr_no'] = data['no']
    df['addr_floor'] = data['floor']
    df['addr_short'] = data['short_address']

    # Drop rows where 'addr_no' or 'addr_road' has missing values
    print('Drop addresses that cannot be recognized...')
    before_count = (len(df))    #count datas
    df['addr_no'].replace('', np.nan, inplace=True) # for empty strings
    df['addr_road'].replace('', np.nan, inplace=True) # for empty strings
    df.dropna(subset=['addr_no', 'addr_road'], inplace=True)
    df = df.reset_index(drop=True)
    print(f'Drop: {before_count - (len(df))}')

    # 'addr_no', 'addr_road' are not needed
    df.drop(['addr_no', 'addr_road'], axis=1, inplace=True)

    data.to_csv('data_format_to_all.csv', encoding='utf-8-sig', index=False)
    print('Finish!')
    return df
