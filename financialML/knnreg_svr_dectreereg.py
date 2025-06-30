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

#hyperparameters
num_lags = 100
train_test_split = 0.80

# Creating the training and test sets
x_train, y_train, x_test, y_test = data_preprocessing(data, num_lags, train_test_split)

##1- linear reg 
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(x_train, y_train)
# Predicting in-sample
y_predicted_train = np.reshape(lr.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(lr.predict(x_test), (-1, 1))

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

##2-support vector reg
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
num_lags = 50
svr = make_pipeline(StandardScaler(),SVR(kernel = 'rbf', C = 1, gamma = 0.04, epsilon = 0.01))
svr.fit(x_train, y_train)
# Predicting in-sample
y_predicted_train = np.reshape(svr.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(svr.predict(x_test), (-1, 1))

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

##3-Stochastic Gradient Descent Regression
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

sgd= make_pipeline(StandardScaler(), SGDRegressor(max_iter = 50, tol = 1e-3))
sgd.fit(x_train, y_train)
y_predicted_train = np.reshape(sgd.predict(x_train), (-1, 1))
y_predicted = np.reshape(sgd.predict(x_test), (-1, 1))

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

##4-KNN Reg
from sklearn.neighbors import KNeighborsRegressor
knnr = KNeighborsRegressor(n_neighbors = 10)
knnr.fit(x_train, y_train)
# Predicting in-sample
y_predicted_train = np.reshape(knnr.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(knnr.predict(x_test), (-1, 1))

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

##5- decision tree (regression tree)
from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor(random_state = 69)
dtr.fit(x_train, y_train)
# Predicting in-sample
y_predicted_train = np.reshape(dtr.predict(x_train), (-1, 1))
# Predicting out-of-sample
y_predicted = np.reshape(dtr.predict(x_test), (-1, 1))

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

