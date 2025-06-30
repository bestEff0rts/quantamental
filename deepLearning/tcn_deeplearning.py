#temporal convolutional network (TCN)
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from master_function import data_preprocessing, plot_train_test_values
from master_function import calculate_accuracy, model_bias
from sklearn.metrics import mean_squared_error

#data
start_date = '2022-01-01'
end_date = '2025-01-01'
# Fetch S&P 500 price data
data = np.array((pdr.get_data_fred('SP500', start = start_date, end = end_date)).dropna())
# Difference the data and make it stationary
data = np.diff(data[:, 0])
#scaling- масштабирование
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test= scaler.transform(x_test)
#3d arrays of features
x_train = x_train.reshape((-1, num_lags, 1))
x_test = x_test.reshape((-1, num_lags, 1))

#tuning parameters
num_lags = 100
train_test_split = 0.80
filters = 64
kernel_size = 4
pool_size = 2
num_epochs = 100
batch_size = 8

#архитектура temporal convolutional network (TCN)
tcn = Sequential()
tcn.add(Conv1D(filters = filters, kernel_size = kernel_size, activation = 'relu', input_shape = (num_lags, 1)))
tcn.add(MaxPooling1D(pool_size = pool_size))
tcn.add(Flatten())
tcn.add(Dense(units = 1))
# Compile the model
tcn.compile(loss = 'mean_squared_error', optimizer = 'adam')
# Train the model
tcn.fit(x_train, y_train, epochs = num_epochs , batch_size = batch_size)
y_predicted_train = np.reshape(tcn.predict(x_train), (-1, 1))
y_predicted = np.reshape(tcn.predict(x_test), (-1, 1))

# Performance evaluation
print('---')
print('Accuracy Train = ', round(calculate_accuracy(y_predicted_train, y_train), 2), '%')
print('Accuracy Test = ', round(calculate_accuracy(y_predicted, y_test), 2), '%')
print('RMSE Train = ', round(np.sqrt(mean_squared_error(y_predicted_train, y_train)), 10))
print('RMSE Test = ', round(np.sqrt(mean_squared_error(y_predicted, y_test)), 10))
print('Correlation In-Sample Predicted/Train = ', round(np.corrcoef(np.reshape(y_predicted_train, (-1)), y_train)[0][1], 3))
print('Correlation Out-of-Sample Predicted/Test = ', round(np.corrcoef(np.reshape(y_predicted, (-1)), np.reshape(y_test, (-1)))[0][1], 3))
print('Model Bias = ', round(model_bias(y_predicted), 2))
print('---')
