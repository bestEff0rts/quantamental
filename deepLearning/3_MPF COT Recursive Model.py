#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from master_function import data_preprocessing, import_cot_data
from master_function import plot_train_test_values, recursive_mpf
from master_function import calculate_directional_accuracy


# In[ ]:


#гиперпараметры
num_lags = 100
train_test_split = 0.80
neurons = 100
num_epochs = 200
batch_size = 2


# In[ ]:


CAD = 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE'
data = import_cot_data(2015, 2023, CAD)
data = np.array(data.iloc[:, -1], dtype = np.float64)


# In[ ]:


#train test split 
x_train, y_train, x_test, y_test = direct_mpf(data, num_lags, train_test_split, forecast_horizon)
#предикторы в 3д
x_train = x_train.reshape((–1, num_lags, 1))
x_test = x_test.reshape((–1, num_lags, 1))


# In[ ]:


model = Sequential()
model.add(LSTM(units = neurons, input_shape = (num_lags, 1)))
model.add(Dense(neurons, activation = 'relu'))
model.add(Dense(units = 1))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')


# In[ ]:


#обучение
model.fit(x_train, y_train, epochs = num_epochs, batch_size = batch_size)


# In[ ]:


x_test, y_predicted = recursive_mpf(x_test, y_test, num_lags, model)


# In[ ]:


plot_train_test_values(100, 50, y_train, y_test, y_predicted)

