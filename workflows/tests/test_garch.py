from src.models.garch import fit_garch_model
import numpy as np

def test_garch_fit():
    returns = np.random.normal(0, 1, 1000)  # Синт данные
    model = fit_garch_model(returns)
    assert model.params is not None  # проверка -модель обучена?
