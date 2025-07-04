import requests
import json
import pandas as pd
import numpy as np
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from master_function import add_column, delete_row, volatility
from master_function import data_preprocessing, plot_train_test_values
from master_function import calculate_directional_accuracy
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller

def import_crypto(symbol, interval = '1h'): 
    # Getting the original link from Binance
    url = 'https://api.binance.com/api/v1/klines'
    # Linking the link with the Cryptocurrency and the time frame
    link = url + '?symbol=' + symbol + '&interval=' + interval
    # Requesting the data in the form of text
    data = json.loads(requests.get(link).text)
    # Converting the text data to dataframe
    data = np.array(data)
    data = data.astype(np.float64)
    data = data[:, 1:5]
    
    return data

frequency = '1h'
# Importing hourly BTCUSD data
data = import_crypto('BTCUSDT')
data 
import pandas as pd
df = pd.DataFrame(data)  # Convert if needed
###### 
x_n = df.iloc[-1,:].values
w = [3000, 4000, 5000] #inv amount
p_0 = sum(w)
w_s = w/x_n

h_sim = (df/df.shift(1) * x_n) [1:]
p_n = h_sim @ w_s

loss= p_0-p_n
VaR_sim=np.quantile(loss, 0.99)  
print(VaR_sim)
#unequal weighting bootstrapping VaR via GARCH(1,1)
u = np.diff(df, axis=0) / df.iloc[:-1, :] # Arithmetic return
u = u.dropna()
total_na = u.isna().sum().sum()
total_na
has_inf = np.isinf(u).sum().sum()
has_inf
u = u.replace([np.inf, -np.inf], np.nan)  # Замена inf на NaN
u = u.dropna()  # Удаление строк с NaN
import arch as gh
import numpy as np
from arch import arch_model

# Создание и обучение GARCH(1,1) модели
model = arch_model(u, vol="GARCH", p=1, q=1)
results = model.fit(update_freq=5)  # MLE по умолчанию

print(results.summary())
