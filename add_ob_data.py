import random
from datetime import datetime, timedelta
import argparse
from db_writer import DBWriter


def generate_ob_data(n=1000):
    """
    Generate order book data with random prices, quantities, and timestamps.
    """

    # Generate random order book data
    ask = 50
    ob_data = []
    dt = datetime.now()
    for i in range(n):
        ask += random.uniform(-0.1, 0.1)
        spread = random.uniform(0.01, 0.1)
        bid = ask - spread
        dt = dt- timedelta(seconds=1)
        symbol = "ETHUSDT"
        ob_data.append(
            {
                "bid": bid,
                "ask": ask,
                "time": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
            }
        )

    return ob_data

def main():
    # Set up argument parser
    wrt = DBWriter()
    parser = argparse.ArgumentParser(description="Generate order book data.")
    parser.add_argument(
        "-n", "--number", type=int, default=1000, help="Number of order book entries to generate."
    )
    parser.add_argument(
        "-l", "--live", type=bool, default=False, help="Generate real time data (True) or static data (False)."
    )
    args = parser.parse_args()
    # Check if live data generation is requested
    if args.live:
        print("Generating real-time data...")
        # Here you would implement the logic for generating real-time data
        # For now, we will just print a message
    else:
        print("Generating static data...")
        ob_data = generate_ob_data(n=args.number)
        wrt.write("order_book", ob_data)




if __name__ == "__main__":
    main()