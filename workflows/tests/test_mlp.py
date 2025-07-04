from MLP_recursive_multiperiod_forecasting import predict_mlp  
import pandas as pd

def test_mlp_prediction():
    sample_data = pd.DataFrame({"Close": [100, 101, 102, 103, 104]})
    prediction = predict_mlp(sample_data, lookback=3)
    assert isinstance(prediction, float)  # Проверяем, что возвращается число
