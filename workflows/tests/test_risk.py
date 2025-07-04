from src.risk_management import calculate_var

def test_var():
    returns = [-0.1, -0.2, -0.3, -0.25]
    var = calculate_var(returns, alpha=0.95)
    assert var <= -0.2  # VaR не мягче минимального убытка
