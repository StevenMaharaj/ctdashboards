from datetime import datetime, timedelta
import random
import argparse
from db_writer import DBWriter

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
        dt = dt - timedelta(seconds=1)
        if qty == 0:
            continue
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


def generate_trade_data_live(n=1000, symbol="ETHUSDT"):
    """
    Generate trade data with random prices, quantities, and timestamps.
    """

    # Generate random trade data
    price = 500
    n_trades = 0
    dt = datetime.now()

    # Define possible quantities and their probabilities
    qty_values = [1, -1, 2, -2, 3, -3, 4, -4]
    qty_probabilities = [0.1, 0.1, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]

    while n_trades < n:
        price += random.uniform(-0.1, 0.1)
        qty = random.choices(qty_values, weights=qty_probabilities, k=1)[0]
        if qty == 0:
            continue
        dt = datetime.now()
        yield [
            {
                "price": price,
                "qty": qty,
                "time": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
            }
        ]

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate trade data.")
    parser.add_argument(
        "-n", "--number", type=int, default=1000, help="Number of trades to generate."
    )
    args = parser.parse_args()

    # Generate trade data
    trade_data = generate_trade_data(n=args.number)

    # Write trade data to database
    wrt = DBWriter()
    wrt.write(table="trades", data=trade_data)

if __name__ == "__main__":
    main()