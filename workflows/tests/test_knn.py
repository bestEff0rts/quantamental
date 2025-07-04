from KNN_StockMarket import knn_predict 
import numpy as np

def test_knn_output():
    X_train = np.array([[1, 2], [3, 4]])
    y_train = np.array([0, 1])
    prediction = knn_predict(X_train, y_train, np.array([[2, 3]]))
    assert prediction in [0, 1]  # KNN должен возвращать класс 0 или 1
