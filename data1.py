import urllib.request
import datetime
import urllib
import pandas as pd
import os

import numpy as np
import csv
import time
# Бібліотека для роботи з графіками
import matplotlib.pyplot as plt
from pandas import read_csv

now_time = datetime.datetime.now()


def downloadwhtime(i):
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=1981&year2=2018&type=Mean".format(
        i)
    vhi_url = urllib.request.urlopen(url)
    out = open('vhi_id_{} {}.csv'.format(i, now_time.strtime('%Y %m %d')), 'wb')
    out.write(vhi_url.read())
    out.close()
    print("VHI is downloaded...")

    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=1981&year2=2018&type=VHI_Parea".format(
        i)
    vhi_url = urllib.request.urlopen(url)
    out = open('VHI_Parea_vhi_id_{} {}.csv'.format(i, now_time.strtime('%Y %m %d')), 'wb')
    out.write(vhi_url.read())
    out.close()
    print("VHI  is downloaded...")


# Функція, яка повертає справжній id країни з сайту
def state_id(id):
    S = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 9, 10, 1, 3, 2, 4]
    return S[id - 1]



def addfiles(i):

    df1 = pd.read_csv('files/csv/2018_02_12-00h_vhi_id_{}.csv'.format(i), index_col=False, header=1, skipfooter=1,
                     engine='python',
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'], delimiter='\,\s+|\s+|\,')
    df2 = pd.read_csv('files/Percent/2018_02_18-16h_vhi_id_{}.csv'.format(i), index_col=False, header=1, skipfooter=1,
                      engine='python',
                      names=['year', 'week', '0', '5', '10', '15', '20', '25', '30', '35', '40',
                             '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100'],
                      delimiter='\,\s+|\s+|\,')
    df = df1.merge(df2, how='outer')
    df.to_csv('test_all{}.csv'.format(i), index=False, header=False)

    print(get_state_name(state_id(i)))
    print(df.shape)
addfiles(1)



def readfile(i):
    df = pd.read_csv('test_all1.csv', index_col=False, header=1, skipfooter=1,
                     engine='python',
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', '0', '5', '10', '15', '20', '25', '30',
                            '35', '40',
                            '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100'],
                     delimiter='\,\s+|\s+|\,')
    return df
#print(readfile(1).to_string(index=False))
df= readfile(1)
def max(df, year):
    #df = readfile(i)
    df_year = df[df.year == year]
    maximum = df_year['VHI'].max()
    print('vhi max', maximum)


def min(df, year):
    #df = readfile(i)
    df_year = df[df.year == year]
    minimum = df_year['VHI'].min()
    print('vhi min', minimum)


def extr(df):
    df = df[(df['year'] != 0) |((df['0'] > 15)|(df['5'] > 15)|(df['10']> 15)| (df['15']> 15)| (df['20']> 15)| (df['25'] > 15)| (df['30'] > 15)| (df['35'] > 15))]
    #короче перші стопчики до 35, де  відcоток певний
    print(df.loc[:, ['year', 'week','VHI']])



max(df, 1987)
min(df, 1982)
extr(df)
