import os, gc
import numpy as np 
import pandas as pd 
import pickle
import multiprocessing
import datetime, math

import matplotlib
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import plotly.graph_objs as go
import plotly.tools as tls
import seaborn as sns
import plotly.offline as py


def pickle_save(fname, results):
    with open(fname, 'wb') as f:
        pickle.dump(results, f)
    
def pickle_load(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)
    
def check_duplicates(df):
    return (df.shape != df.drop_duplicates().shape)

def join_df(left, right, left_on, method='left', right_on=None, suffix='_y'):
    if right_on is None: right_on = left_on
    return left.merge(right, how=method, left_on=left_on, right_on=right_on, suffixes=("", suffix))

def missing_count(df):
    r'''count number of missing values in each type of attributes'''
    msv = df.isnull().sum()
    msv_percent = 100 * df.isnull().sum() / len(df)
    msv_table = pd.concat([msv, msv_percent], axis=1)
    msv_table_cols = msv_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
    msv_table_cols = msv_table_cols[msv_table_cols.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(msv_table_cols.shape[0]) +
              " columns that have missing values.")
    return msv_table_cols

def replace_by_index(df, col, index, value):
    df.loc[index, col] = value

def convert(s):
    r'''convert string to datetime object'''
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()

def delta(dt1,dt2): 
    r'''calculates the difference btw 2 datetime objects in days'''
    return (dt1 - dt2).days

def to_datetime(ts):
    return datetime.fromtimestamp(ts)

def to_datetime_str(ts):
    return to_datetime(ts).strftime('%Y-%B-%d %H:%M:%S')

def num2bins(df, colname, bins, labels, drop=True):
    df[colname+'_cat'] = pd.cut(df[colname], 
                                bins=bins, 
                                labels=labels, 
                                right=True, 
                                include_lowest=True)
    if drop:
        df = df.drop(columns=colname)