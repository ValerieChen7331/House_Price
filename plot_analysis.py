#載入套件
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import missingno as msno
import math

def draw_pie_groupby(df, target_column, gorup_column, percentage_plot=0):
    missing_values_count = {}
    values_count = {}
    missing_percentage = {}

    percentage = 100 * (len(df)-df[target_column].count())/len(df)
    print("Missing value percentage (%): {:.1f}".format(percentage))

    # Count missing values for each Type
    for type_name in df[gorup_column].unique():
        # missing values
        missing_count = df[df[gorup_column] == type_name][target_column].isnull().sum()
        missing_values_count[type_name] = missing_count
        # total values
        count = df[df[gorup_column] == type_name][target_column].sum()
        values_count[type_name] = int(count)
        # percentage
        missing_percentage[type_name] = missing_values_count[type_name]/values_count[type_name] *100

    # Create a DataFrame
    data_all = pd.DataFrame(list(zip(missing_values_count.values(), values_count.values(), missing_percentage.values())),
                            index=missing_values_count.keys(),
                            columns=['Missing_Count', 'Total_Count', 'Missing_Percentage'])
    print(data_all)

    # Datas of missing values for each Type
    data_values = values_count.values()
    labels_values = values_count.keys()
    data_missing = missing_values_count.values()
    labels_missing = missing_values_count.keys()

    # Define pie chart
    colors = sns.color_palette('pastel')
    fig = plt.figure(figsize=(12,4))
    plt.rcParams['font.size'] = 8

    # Pie chart for total values
    ax1 = plt.subplot2grid((1,2),(0,0))
    plt.pie(data_values, labels = labels_values, colors = colors, autopct='%.0f%%', radius=1,
            wedgeprops={"linewidth": 1, "edgecolor": "white"})
    plt.title(f"{gorup_column} Distribution for All Data")

    # Pie chart for missing values
    ax2 = plt.subplot2grid((1,2),(0,1))
    plt.pie(data_missing, labels = labels_missing, colors = colors, autopct='%.0f%%', radius=1,
            wedgeprops={"linewidth": 1, "edgecolor": "white"})
    plt.title(f"{gorup_column} Distribution for Missing Values of {target_column}")

    plt.tight_layout()
    plt.show()

    if percentage_plot:
        # Bar chart of Missing Percentage for each Type
        fig_width = (len(missing_percentage.keys())*8+44)/17
        fig = plt.figure(figsize=(fig_width,3))
        sns.barplot(missing_percentage, x = missing_percentage.keys(), y=missing_percentage.values(), color='#ffcc99')
        plt.xticks(rotation= 30)
        plt.xlabel(gorup_column)
        plt.ylabel('Percentage (%)')
        plt.title('Percentage of Missing Values ')

        plt.show()
    return data_all

def violin_box_one(df, column_name):
    box_plot_data = [df[column_name]]
    fig = plt.figure(figsize=(5, 3))
    # horizontal spacing between subplots
    plt.subplots_adjust(wspace=0.5)

    # Create a violin plot
    ax1 = fig.add_subplot(121)
    ax1.violinplot(box_plot_data)
    ax1.set_title('Violin Plot: {}'.format(column_name))

    # Create a box plot
    ax2 = fig.add_subplot(122)
    ax2.boxplot(box_plot_data)
    ax2.set_title('Box Plot: {}'.format(column_name))

    plt.show()

def violin_box_all(df, data_labels):
    # Data for the box and violin plots
    box_plot_data = []
    for data_label in data_labels:
        box_plot_data.append(df[data_label])

    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10))

    # Create a violin plot
    ax1.violinplot(box_plot_data, showmedians=True)
    ax1.set_xticks(range(1, len(data_labels) + 1))
    ax1.set_xticklabels(data_labels, rotation=45)
    ax1.set_title('Violin Plot')

    # Create a box plot
    ax2.boxplot(box_plot_data)
    ax2.set_xticks(range(1, len(data_labels) + 1))
    ax2.set_xticklabels(data_labels, rotation=20)
    ax2.set_title('Box Plot')

    plt.tight_layout()
    plt.show()

def one_column_heatmap(df, column_name):
    df_num = df.select_dtypes(include=['float64', 'int64'])

    # Create a corr_matrix heatmap
    corr_matrix = df_num.corr()
    price_corr = corr_matrix[[column_name]]

    # Determine the minimum and maximum absolute values
    min_val = abs(price_corr.values).min()
    max_val = abs(price_corr.values).max()

    # Create a Horizontal Heatmap
    plt.figure(figsize=(22, 1))
    sns.heatmap(price_corr.T, annot=True, cmap='coolwarm', fmt=".2f",
     linewidths=.5, center=0, vmin=-max_val, vmax=max_val)
    plt.title('Correlation Heatmap of ' + column_name)
    plt.show()
    return

def all_corr_heatmap(df):
    # Calculate the correlation coefficient matrix
    df_num = df.select_dtypes(include = ['float64', 'int64'])
    corr_matrix = df_num.corr()

    # Create a mask that hides duplicate numbers
    mask = (np.triu(np.ones_like(corr_matrix), k=0))

    # Determine the minimum and maximum absolute values
    min_val = abs(corr_matrix.values).min()
    max_val = abs(corr_matrix.values).max()

    # creat a heat map with the mask
    plt.figure(figsize=(20, 12))
    sns.heatmap(corr_matrix, annot=True, mask=mask, cmap='coolwarm', fmt=".2f",
     linewidths=.5, center=0, vmin=-max_val, vmax=max_val)

    plt.title('Correlation Heatmap (Upper Triangle)')
    plt.show()
    return

#------------------------------------------
def normalization(df, column_name):
    nmax = df[column_name].max()
    nmin = df[column_name].min()
    df[column_name] = (df[column_name] - nmin) / (nmax - nmin)
    return df

def IQR(df, column_name):
    # 將所有特徵超出1.5倍IQR的概念將這些Outlier先去掉，避免對Model造成影響。
    print ("Shape Of The Before Ouliers: ", df[column_name].shape)
    n=2
    #IQR = Q3-Q1
    IQR = np.percentile(df[column_name],75) - np.percentile(df[column_name],25)
    print(np.percentile(df[column_name],75), np.percentile(df[column_name],25))
    # outlier = Q3 + n*IQR
    transform_data = df[df[column_name] < np.percentile(df[column_name],75) + n*IQR]
    # outlier = Q1 - n*IQR
    transform_data = transform_data[transform_data[column_name] > np.percentile(transform_data[column_name],25) - n*IQR]
    print ("{} Shape Of The After Ouliers: {}".format(column_name, transform_data.shape))
    violin_box_one(df, column_name)
    violin_box_one(transform_data, column_name)
    return transform_data

# 數值方法補值
def statistics_dataframe(group, target_column):

    dis_type = []
    dis_count = []
    dis_mean = []
    dis_std = []
    dis_min = []
    dis_max = []
    dis_mode = []

    for name, group_data in group:
        dis_type.append(name)
        dis_count.append(int(group_data[target_column].count()))
        dis_mean.append(group_data[target_column].mean())
        dis_std.append(group_data[target_column].std())
        dis_min.append(int(group_data[target_column].min()))
        dis_max.append(int(group_data[target_column].max()))

        mode_value = group_data[target_column].mode().values
        if len(mode_value) > 1:
            print(f"more than 1 mode in {name}: {mode_value}")
        dis_mode.append(int(mode_value[0]))

    # Example of creating a DataFrame from the lists
    statistics_df = pd.DataFrame({
        'Type': dis_type,
        'Count': dis_count,
        'Mean': dis_mean,
        'Std': dis_std,
        'Min': dis_min,
        'Max': dis_max,
        'Mode': dis_mode})

    # Print the resulting DataFrame
    statistics_df.to_csv('statistics_storeys.csv', encoding='utf-8-sig', index=False)
    #print(statistics_df)
    return statistics_df

def statistics_houseage(group, group_column, target_column):
    dis_dis = []
    dis_type = []
    dis_count = []
    dis_mean = []
    dis_std = []
    dis_min = []
    dis_max = []
    dis_mode = []

    for name, group_data in group:
        group_data_t = group_data.groupby(group_column)
        for name_d, group_data_d in group_data_t:
            #print(name_d)
            #print(group_data_d['HouseAge'].describe())
            dis_type.append(name)
            dis_dis.append(str(name_d))
            dis_count.append(group_data_d[target_column].count())
            dis_mean.append(group_data_d[target_column].mean())
            dis_std.append(group_data_d[target_column].std())
            dis_min.append(group_data_d[target_column].min())
            dis_max.append(group_data_d[target_column].max())
            # Compute the mode
            mode_value = group_data[target_column].mode().values
            if len(mode_value) > 1:
                print(f"more than 1 mode in {name}: {mode_value}")
            dis_mode.append(int(mode_value[0]))

    # Create a DataFrame from the collected data
    statistics_df = pd.DataFrame({
        group_column: dis_dis,
        'Type': dis_type,
        'Count': dis_count,
        'Mean': dis_mean,
        'Std': dis_std,
        'Min': dis_min,
        'Max': dis_max,
        'Mode': dis_mode
        })
    # save the resulting DataFrame
    statistics_df.to_csv('statistics_houseage.csv', encoding='utf-8-sig', index=False)
    #print(statistics_df)
    return statistics_df
