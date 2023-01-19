import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


my_pkg = "C://Users//welcome//Desktop//MyFuncs"
fpath = os.sys.path
if my_pkg not in fpath:
    fpath.append(my_pkg)

from visualize import VizUtils as viz
from ds_funcs import DsUtils as ds

# This is a sample Python script.
data_dir = "C://Users//welcome//Documents//Financial Recs//FinancialPlan//2022//CSV Files"
# data_dir = "C://Users//welcome//Desktop//Extract Here//Ex_Files_Learning_Data_Analytics_P2//Exercise Files//CH01//01_04"
# file_name = "//Customer and Order Data_begin.xlsx"
file_name = '//Expenses2022.txt'
fname = data_dir+file_name

class df(pd.DataFrame):
    pass

def show_result():
    # df =  pd.read_excel(fname)
    df = pd.read_csv(fname)
    print(df.head())
    print(df.columns)
    print(df.info())

    # replace nan with 0
    df = df.fillna(0)

    # assign datetime datatype to Date column
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df = df.sort_values(by=['Date'])
    print(df.info())

    # engineer days of the week from day
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Day of Week'] = df['Date'].dt.day_name()
    df['Day of Week No'] =  df['Date'].dt.isocalendar().day
    df['Day Count'] = df['Date'].dt.dayofyear
    df['Week Count'] = df['Date'].dt.isocalendar().week
    print(df)

    # only expense records
    cond = (df['Type'] == 'Expense')  # select expense records
    cols = ['ID', 'Date', 'Credit', 'Type']
    exp = df.loc[cond].drop(columns=cols)  # exclude the id, type, and credit columns

    # rename debit column to spend
    exp = exp.rename(columns={'Debit':'Spend'})
    print(exp.info())
    exp = exp.reset_index(drop=True)
    print(exp)

    # 1. Day of week I'm likely to spend most
    cols = ['Day of Week No', 'Day of Week', 'Spend']
    y_labe = f'Annual {cols[-1]}'
    spend_agg = ds.generate_aggregated_lookup(exp, using_cols=cols, y_col=cols[-1],
                                          calculation_goal='sum').sort_values(cols[0],
                                                                              ascending=True).rename(columns={cols[-1]:y_labe})
    print(spend_agg)
    labes = ds.combine_multiple_columns(spend_agg[cols[:-1]], output_name=cols[1])
    print(labes)
    total_spend = spend_agg[y_labe].sum()
    img_file = 'annual_spend_per_wkday.png'
    viz.plot_column(x=labes.values, y=spend_agg[y_labe], paletter=viz.dayname_cmap,
                      plot_title='Spending Habit per Weekday', include_perc=True, perc_total=total_spend,
                      perc_labe_gap=100, figsize=(10, 5), savefig=True, fig_filename=img_file)

    viz.view_image_file(img_file)

    # 2. Month I'm likely to spend most
    cols = ['Month', 'Spend']
    y_labe = f'Annual {cols[-1]}'
    spend_agg = ds.generate_aggregated_lookup(exp, using_cols=cols, y_col=cols[-1],
                                          calculation_goal='sum').sort_values(cols[0],
                                                                              ascending=True).rename(columns={cols[-1]:y_labe})
    print(spend_agg)
    labes = ds.combine_multiple_columns(spend_agg[cols[:-1]])
    print('\nHERE:\n')
    print(labes)
    total_spend = spend_agg[y_labe].sum()
    img_file = 'annual_spend_per_month.png'
    viz.plot_column(x=spend_agg[cols[0]], y=spend_agg[y_labe],
                    plot_title='Spending Habit per Month', include_perc=True, perc_total=total_spend,
                    perc_labe_gap=100, figsize=(10, 5), savefig=True, fig_filename=img_file)

    viz.view_image_file(img_file)

    # 3. daily spend per month
    cols = ['Month', 'Day of Week No', 'Day of Week', 'Spend']
    y_labe = f'Annual {cols[-1]}'
    spend_agg = ds.generate_aggregated_lookup(exp, using_cols=cols, y_col=cols[-1],
                                          calculation_goal='sum').sort_values(cols[:-2],
                                                                              ascending=True).rename(columns={cols[-1]:y_labe})
    print(spend_agg)
    total_spend = spend_agg[y_labe].sum()
    img_file = 'daily_spend_per_month.png'
    viz.plot_bar(x=spend_agg[y_labe], y=spend_agg[cols[0]], condition_on=spend_agg[cols[-2]],
                    plot_title='Daily Spending Habit per Month', #condition_order=spend_agg[cols[-2]],
                    include_perc=True, perc_total=total_spend, perc_labe_gap=100, figsize=(15, 6),
                    paletter=viz.dayname_cmap, show_legend_at=[0.5, 0.5], savefig=True, fig_filename=img_file)

    viz.view_image_file(img_file)

    # 4. trend of daily spend per month
    cols = ['Month', 'Day of Week No', 'Day of Week', 'Spend']
    y_labe = f'Annual {cols[-1]}'
    spend_agg = ds.generate_aggregated_lookup(exp, using_cols=cols, y_col=cols[-1],
                                          calculation_goal='sum').sort_values(cols[:-2],
                                                                              ascending=True).rename(columns={cols[-1]:y_labe})
    img_file = 'daily_spend_per_month_trend.png'
    viz.plot_line(y=spend_agg[y_labe], x=spend_agg[cols[0]], condition_on=spend_agg[cols[-2]],
                 plot_title='Trend of Daily Spending Habit per Month', marker='o',
                 figsize=(15, 6), paletter=viz.dayname_cmap, show_legend_at=[0.5, 0.5], savefig=True,
                fig_filename=img_file)
    viz.view_image_file(img_file)

    # 5. trend of daily spend per week
    cols = ['Week Count', 'Day of Week No', 'Day of Week', 'Spend']
    y_labe = f'Annual {cols[-1]}'
    spend_agg = ds.generate_aggregated_lookup(exp, using_cols=cols, y_col=cols[-1],
                                              calculation_goal='sum').sort_values(cols[:-2],
                                                                              ascending=True).rename(columns={cols[-1]:y_labe})
    img_file = 'daily_spend_per_week_trend.png'
    viz.plot_scatter(y=spend_agg[y_labe], x=spend_agg[cols[0]], condition_on=spend_agg[cols[-2]],
                  plot_title='Trend of Daily Spending Habit per Week', marker='o', #show_legend_at=[0.5, 0.5],
                  figsize=(15, 6), paletter=viz.dayname_cmap, savefig=True,
                  fig_filename=img_file)
    viz.view_image_file(img_file)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    show_result()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
