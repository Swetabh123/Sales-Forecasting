##..................................................................................................
##IMPORTING LIBRARIES

import os
#For Working with Data Frames
import pandas as pd
import datetime
import numpy as np

#Plotting Libraries
import plotly.express as px
import matplotlib as plt

#To ignore warnings
import warnings
warnings.filterwarnings('ignore')

#Importing app library
import streamlit as st
import requests
from streamlit_lottie import st_lottie

#Importing app libraries
from pmdarima import auto_arima

##.......................................................................
##USER DEFINED FUNCTIONS

#image function
def load_lottie(url): 
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Normalizing
def stand_data(df):
    Data_Type = {'Sales': float}
    df = df.astype(Data_Type)
    df['Date'] = pd.to_datetime(df['Date'],errors='coerce').dt.date
    return df

#categorical standardization
def stand_data_cat(df):
    Data_Type = {'Sales': float,'Category':object}
    df = df.astype(Data_Type)
    df['Date'] = pd.to_datetime(df['Date'],errors='coerce').dt.date
    return df

#Outlier function
def outlier_rem(data,col):
    Q1 = np.percentile(data[col],25)
    Q3 = np.percentile(data[col],75)
    IQR = Q3-Q1
    # Upper bound
    upper=Q3+1.5*IQR  
    # Removing the outliers
    data = data[data[col]<=upper]
    return data


def agg_ts_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    df = df.groupby(by = ['Year','Month']).agg({'Sales':np.sum})
    df = df.reset_index()
    df['Year_Month'] = df.Month.map(str) + "-" + df.Year.map(str)
    df = df.drop(columns = ['Year','Month'])
    df['Year_Month']=pd.to_datetime(df['Year_Month'])
    df = df.groupby(['Year_Month']).agg({'Sales':np.sum})
    return df

#fitting auto arima to the dataset & returning summarry
def modeling(df):
    model = auto_arima(df['Sales'],start_p = 1, start_q = 1, max_p=3, max_q = 3, m=12,
                  start_P = 0, seasonal= True, d=None, D =1, trace = False, error_action = 'ignore',
                  suppress_warnings=True, stepwise = True)
    return model


def forecast(model,n_period,sig_level):
    return model.predict(n_periods = n_period, return_conf_int = False, alpha = sig_level)
