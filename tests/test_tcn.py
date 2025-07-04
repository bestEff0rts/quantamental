from tcn_deeplearning import build_tcn_model  

def test_tcn_architecture():
    model = build_tcn_model(input_shape=(20, 1), num_filters=64)
    assert any("TCN" in layer.__class__.__name__ for layer in model.layers)
