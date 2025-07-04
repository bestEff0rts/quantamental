import numpy as np
from lstm import build_lstm_model  

def test_lstm_model_creation():
    model = build_lstm_model(input_shape=(10, 1))  # 10 временных шагов
    assert model is not None
    assert "LSTM" in [layer.__class__.__name__ for layer in model.layers]
