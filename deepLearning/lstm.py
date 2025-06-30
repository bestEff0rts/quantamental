#Long Short-Term Memory (rnn которая решает проблему vanishing gradient)
from keras.models import Sequential
from keras.layers import Dense, LSTM
import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from master_function import data_preprocessing, plot_train_test_values
from master_function import calculate_accuracy, model_bias
from sklearn.metrics import mean_squared_error
#гиперпараметры
num_lags = 100
train_test_split = 0.80
num_neurons_in_hidden_layers = 20
num_epochs = 100
batch_size = 32
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

#lstm архитектура keras
lstm = Sequential()
#1st LSTM layer
lstm.add(LSTM(units = num_neurons_in_hidden_layers,input_shape = (num_lags, 1)))
#2nd hidden layer
lstm.add(Dense(num_neurons_in_hidden_layers, activation = 'relu'))
#Output layer
lstm.add(Dense(units = 1))
# Compile the model
lstm.compile(loss = 'mean_squared_error', optimizer = 'adam')
lstm.fit(x_train, y_train, epochs = num_epochs, batch_size = batch_size)
# Predict IS
y_predicted_train = np.reshape(lstm.predict(x_train), (-1, 1))
# Predict OOS
y_predicted = np.reshape(lstm.predict(x_test), (-1, 1))

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

