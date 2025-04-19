from datetime import datetime, timedelta
import random

def generate_trade_data(n=1000, symbol="ETHUSDT"):
    """
    Generate trade data with random prices, quantities, and timestamps.
    """

    # Generate random trade data
    price = 500
    n_trades = 0
    trade_data = []
    dt = datetime.now()

    # Define possible quantities and their probabilities
    qty_values = [1, -1, 2, -2, 3, -3, 4, -4, 0]
    qty_probabilities = [0.1, 0.1, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05, 0.4]

    while n_trades < n:
        price += random.uniform(-0.1, 0.1)
        qty = random.choices(qty_values, weights=qty_probabilities, k=1)[0]
        if qty == 0:
            continue
        dt = dt - timedelta(seconds=1)
        trade_data.append(
            {
                "price": price,
                "qty": qty,
                "time": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
            }
        )
        n_trades += 1

    return trade_data