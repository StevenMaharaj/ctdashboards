import pytest
from add_trade_data import generate_trade_data

def test_generate_trade_data():
    n = 100
    symbol = "BTCUSDT"
    trade_data = generate_trade_data(n=n, symbol=symbol)

    # Check the number of trades generated
    assert len(trade_data) == n

    # Check the structure and content of each trade
    for trade in trade_data:
        assert "price" in trade
        assert "qty" in trade
        assert "time" in trade
        assert "symbol" in trade

        # Check that the symbol matches
        assert trade["symbol"] == symbol

        # Check that qty is one of the expected values
        assert trade["qty"] in [1, -1, 2, -2, 3, -3, 4, -4]

# Run this test using pytest