import pandas_datareader as pdr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import MetaTrader5 as mt
from sklearn.dummy import DummyRegressor
from master_function import data_preprocessing, mass_import
from master_function import plot_train_test_values, calculate_accuracy, model_bias
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = np.array(pd.read_excel('D:/RStudio/stats/Daily_GBPUSD_Historical_Data.xlsx') ['<CLOSE>'])
# Difference the data = make it stationary
data = np.diff(data)

#масштабирование _тут не нужно
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# x_train_scaled = scaler.fit_transform(x_train)
# x_test_scaled = scaler.transform(x_test)

#hyperparameters
num_lags = 500
train_test_split = 0.8

# Creating the training and test sets
x_train, y_train, x_test, y_test = data_preprocessing(data, num_lags, train_test_split)

import numpy as np
from sklearn.metrics import mean_squared_error

##1- Random Forest reg
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(max_depth = 10, random_state = 69)
rf.fit(x_train, y_train)
print(rf.get_params())
# Predicting in-sample
y_predicted_train = np.reshape(rf.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(rf.predict(x_test), (-1, 1))
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

##2- Adaptive Boosting (adaboost)
from sklearn.ensemble import AdaBoostRegressor
adb= AdaBoostRegressor(random_state = 69)
adb.fit(x_train, y_train)
# Predicting in-sample
y_predicted_train = np.reshape(adb.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(adb.predict(x_test), (-1, 1))
print(adb.get_params())
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

##3-  extreme gradient boosting =xgboost
from xgboost import XGBRegressor
xgb= XGBRegressor(random_state = 69, n_estimators = 16,max_depth = 12)
xgb.fit(x_train_scaled, y_train)
# Predicting in-sample
y_predicted_train = np.reshape(xgb.predict(x_train_scaled), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(xgb.predict(x_test_scaled), (-1, 1))
print(xgb.get_params())
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


