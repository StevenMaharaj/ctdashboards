import psycopg2
from psycopg2 import Error

# PostgreSQL connection parameters
host = "localhost"
database = "mydb"
user = "myuser"
password = "mypassword"

# Sample trade data
trades_data = [
    {"price": 60000.50, "qty": 0.5, "time": "2025-04-08 10:30:00", "symbol": "BTCUSDT"},
    {"price": 3000.25, "qty": 1.2, "time": "2025-04-08 11:15:00", "symbol": "ETHUSDT"}
]

# SQL statements
create_table_query = """
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    price NUMERIC,
    qty NUMERIC,
    time TIMESTAMP,
    symbol VARCHAR(20)
)
"""

insert_query = """
INSERT INTO trades (price, qty, time, symbol) VALUES (%s, %s, %s, %s)
"""

try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(host=host, database=database, user=user, password=password)

    # Create a cursor object
    cursor = connection.cursor()

    # Create trades table if it doesn't exist
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'trades' created successfully.")

    # Insert sample trade data
    for trade in trades_data:
        cursor.execute(insert_query, (trade["price"], trade["qty"], trade["time"], trade["symbol"]))
        connection.commit()
    print("Sample trade data inserted successfully.")

except (Exception, Error) as error:
    print("Error while working with PostgreSQL:", error)

finally:
    # Close cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")
