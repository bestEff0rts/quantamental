#!/usr/bin/env python
# coding: utf-8

# In[1]:


#EURUSD’s weekly returns using rsi and dist between the previous week’s close price and the 20-week moving average.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from master_function import mass_import, rsi, ma, calculate_accuracy
from master_function import plot_train_test_values
from master_function import multiple_data_preprocessing
from sklearn.metrics import mean_squared_error
from master_function import add_column, delete_column


# In[24]:


import datetime
import pytz
import pandas                    as pd
import MetaTrader5               as mt5
import matplotlib.pyplot         as plt
import numpy                     as np
import cot_reports               as cot
import requests
import json  

now = datetime.datetime.now()

assets = ['EURUSD', 'USDCHF', 'GBPUSD', 'USDCAD', 'AUDUSD', 'NZDUSD', 'EURGBP', 'EURCHF', 'EURCAD', 'EURAUD']
 
def get_quotes(time_frame, year = 2005, month = 1, day = 1, asset = "EURUSD"):    
    if not mt5.initialize(): 
        print("initialize() failed, error code =", mt5.last_error()) 
        quit()
    timezone = pytz.timezone("Europe/Paris")
    time_from = datetime.datetime(year, month, day, tzinfo = timezone)
    time_to = datetime.datetime.now(timezone) + datetime.timedelta(days=1)
    rates = mt5.copy_rates_range(asset, time_frame, time_from, time_to)
    rates_frame = pd.DataFrame(rates)
    
    return rates_frame 
def mass_import(asset, time_frame):
    if time_frame == 'M15':
        data = get_quotes(mt5.TIMEFRAME_M15, 2023, 6, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)    
    if time_frame == 'M30':
        data = get_quotes(mt5.TIMEFRAME_M30, 2023, 6, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)              
    if time_frame == 'H1':
        data = get_quotes(mt5.TIMEFRAME_H1, 2015, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)         
    if time_frame == 'D1':
        data = get_quotes(mt5.TIMEFRAME_D1, 2003, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
    if time_frame == 'W1':
        data = get_quotes(mt5.TIMEFRAME_W1, 2002, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
    if time_frame == 'M1':
        data = get_quotes(mt5.TIMEFRAME_MN1, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)             
    
    return data


# In[26]:


data = mass_import(0, 'W1')[:, -1]
data


# In[27]:


data = rsi(np.reshape(data, (-1, 1)), 5, 0, 1)
data = ma(data, 5, 0, 2)
data[:, 2] = data[:, 0] - data[:, 2]
data = add_column(data, 1)
for i in range(len(data)):
    data[i, 3] = data[i, 0] - data[i - 1, 0]
data[:, 0] = data[:, -1]
data = delete_column(data, 3, 1)


# In[29]:


data


# In[30]:


#гиперпараметры
num_lags = 6 # Must equal the number of the lagged values you create
train_test_split = 0.80
neurons = 300
num_epochs = 300
batch_size = 200


# In[31]:


def multiple_data_preprocessing(data, train_test_split):
    """
    Processes fractionally differentiated data for time series forecasting
    with multiple lagged features.
    
    Args:
        data: 2D numpy array of fractionally differentiated values (shape: [n_samples, n_features])
        train_test_split: float (0-1), ratio for train-test split
        
    Returns:
        x_train, y_train, x_test, y_test
    """
    # Ensure input is 2D numpy array
    data = np.array(data)
    if len(data.shape) == 1:
        data = data.reshape(-1, 1)
    
    # Add columns for lagged features (adjust number )
    n_lags = 6 # Number of lagged features to create
    n_cols = data.shape[1]
    
    # Create new array with original + lagged features
    processed_data = np.zeros((len(data), 1 + n_lags*n_cols))
    processed_data[:, 0] = data[:, 0]  # Original series
    
    # Create lagged features
    for lag in range(1, n_lags + 1):
        for col in range(n_cols):
            processed_data[:, 1 + (lag-1)*n_cols + col] = np.roll(data[:, col], lag)
    
    # Remove rows with NaN (from rolling)
    processed_data = processed_data[n_lags:]
    
    # Split into features (X) and target (y)
    x = processed_data[:, 1:]  # All columns except first
    y = processed_data[:, 0]   # First column is target
    
    # Train-test split
    split_index = int(train_test_split * len(x))
    x_train = x[:split_index]
    y_train = y[:split_index]
    x_test = x[split_index:]
    y_test = y[split_index:]
    
    return x_train, y_train, x_test, y_test


# In[32]:


#train test split
x_train, y_train, x_test, y_test = multiple_data_preprocessing(frac_data, train_test_split)


# In[33]:


x_train = x_train.reshape((-1, num_lags, 1))
x_test = x_test.reshape((-1, num_lags, 1))


# In[ ]:





# model.fit(x_train, y_train, epochs = num_epochs, batch_size = batch_size)

# In[35]:


model.fit(x_train, y_train, epochs = num_epochs, batch_size = batch_size)


# In[34]:


#lstm архитектруа keras
model = Sequential()
model.add(LSTM(units = neurons, input_shape = (num_lags, 1)))
model.add(Dense(neurons, activation = 'relu'))
model.add(Dense(neurons, activation = 'relu'))
model.add(Dense(neurons, activation = 'relu'))
model.add(Dense(neurons, activation = 'relu'))
model.add(Dense(units = 1))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')


# In[16]:


# Predicting in the training set for illustrative purposes
y_predicted_train = model.predict(x_train)
# Predicting in the test set
y_predicted = model.predict(x_test)


# In[39]:


print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)


# In[17]:


plot_train_test_values(100, 50, y_train, y_test, y_predicted)


# In[20]:


# Performance evaluation

print('Accuracy Train = ', round(calculate_accuracy(y_predicted_train, y_train), 2), '%')
print('Accuracy Test = ', round(calculate_accuracy(y_predicted, y_test), 2), '%')
print('RMSE Train = ', round(np.sqrt(mean_squared_error(y_predicted_train, y_train)), 10))
print('RMSE Test = ', round(np.sqrt(mean_squared_error(y_predicted, y_test)), 10))
print('Correlation In-Sample Predicted/Train = ', round(np.corrcoef(np.reshape(y_predicted_train, (-1)), y_train)[0][1], 3))
print('Correlation Out-of-Sample Predicted/Test = ', round(np.corrcoef(np.reshape(y_predicted, (-1)), np.reshape(y_test, (-1)))[0][1], 3))

