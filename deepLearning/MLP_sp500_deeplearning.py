#MLP to forecast daily S&P 500 returns
from keras.models import Sequential
from keras.layers import Dense
import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from master_function import data_preprocessing, plot_train_test_values
from master_function import calculate_accuracy, model_bias
from sklearn.metrics import mean_squared_error

start_date = '2022-01-01'
end_date = '2025-01-01'
# Fetch S&P 500 price data
data = np.array((pdr.get_data_fred('SP500', start = start_date, end = end_date)).dropna())
# Difference the data and make it stationary
data = np.diff(data[:, 0])

#гиперпараметры =tuning parameters (or via CV)
num_lags = 100
train_test_split = 0.80
num_neurons_in_hidden_layers = 20
num_epochs = 500
batch_size = 16
x_train, y_train, x_test, y_test = data_preprocessing(data, num_lags, train_test_split)

#MLP architecture in keras
mlp = Sequential()
#1st hidden layer with ReLU as activation function
mlp.add(Dense(num_neurons_in_hidden_layers, input_dim = num_lags, activation = 'relu'))
#2nd hidden layer with ReLU as activation function
mlp.add(Dense(num_neurons_in_hidden_layers, activation = 'relu'))
# Output layer
mlp.add(Dense(1))
# Compiling
mlp.compile(loss = 'mean_squared_error', optimizer = 'adam')
# Fitting the model
mlp.fit(x_train, np.reshape(y_train, (-1, 1)), epochs = num_epochs,batch_size = batch_size)
# Predicting in-sample
y_predicted_train = np.reshape(model.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(model.predict(x_test), (-1, 1))

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
