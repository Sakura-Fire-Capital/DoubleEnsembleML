import os
import torch
import torch.nn as nn
import torch.utils.data as Data
from sklearn.preprocessing import MinMaxScaler
import pandas as pd 
import numpy as np 
from tqdm import tqdm
import plotly.graph_objects as go
import talib




path = "/Users/zed/AI_Lab/PRP2021/prp_data/东阿阿胶000423.csv"
df = pd.read_csv(path,index_col = 0)
df.columns = ["Open","Close","High","Low","last_Close","Tag"]

dataset = df

def interval(series):
    return abs(series['high']-series['low'])/series['last_cls']


def tag(se):
    if se['tag'] <= thres[0]:
        return 0
    elif se['tag'] <= thres[1]:
        return 1
    elif se['tag'] <= thres[2]:
        return 2
    else:
        return 3
dataset['last_cls'] = dataset['close'].shift(1)
dataset['tag'] = 0
dataset['tag'] = dataset.apply(interval, axis=1)
thres = dataset['tag'].describe()[4:7]
dataset['tag'] = dataset.apply(tag, axis=1)
prd_data = dataset[["open", "close", "high", "low", "last_cls", 'tag']]
prd_data["tag"] = prd_data["tag"].shift(-1)

dataset = prd_data
dataset.columns = ["Open","Close","High","Low","last_Close","Tag"]

dataset['H-L'] = dataset['High'] - dataset['Low']
dataset['O-C'] = dataset['Close'] - dataset['Open']
dataset['3day MA'] = dataset['Close'].shift(1).rolling(window = 3).mean()
dataset['10day MA'] = dataset['Close'].shift(1).rolling(window = 10).mean()
dataset['30day MA'] = dataset['Close'].shift(1).rolling(window = 30).mean()
dataset['Std_dev']= dataset['Close'].rolling(5).std()
dataset['RSI'] = talib.RSI(dataset['Close'].values, timeperiod = 9)
dataset['Williams %R'] = talib.WILLR(dataset['High'].values, dataset['Low'].values, dataset['Close'].values, 7)
