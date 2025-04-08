# Filler Data
`generate_data.py` connects to a PostgreSQL database, creates a table named `trades`, and inserts sample trade data for BTCUSDT and ETHUSDT:

### Explanation:

1. **Connection Parameters**: Replace `host`, `database`, `user`, and `password` with your PostgreSQL server details.

2. **Sample Trade Data**: `trades_data` contains dictionaries with trade information for BTCUSDT and ETHUSDT.

3. **SQL Statements**:
   - `create_table_query`: Defines the `trades` table schema with columns for `price`, `qty`, `time`, and `symbol`.
   - `insert_query`: Inserts data into the `trades` table using parameters.

4. **Execution**:
   - Connects to PostgreSQL using `psycopg2`.
   - Creates the `trades` table if it doesn't exist.
   - Inserts sample trade data into the table.

5. **Error Handling**: Catches and prints any errors that occur during execution.

### Usage:

- Save this script as `create_trades_table.py`.
- Make sure to install `psycopg2` using `pip install psycopg2` if you haven't already.
- Run the script using `python create_trades_table.py` to create the table and insert the sample trade data into your PostgreSQL database.