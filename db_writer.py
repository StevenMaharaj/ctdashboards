from db_conn import DBConnection
class DBWriter:
    def __init__(self,):
        self.conn = DBConnection()
        self.conn.connect()
        # Initialize database connection here

    def write(self, table:str,data:list[dict]):
        # Check if table exists, if not create it
        assert table in ["order_book", "trades"], "Invalid table name"
        self.check_table_if_not_create(table)
        # Write data to the database
        for entry in data:
            try:
                # Assuming 'data' is a list of dictionaries
                columns = ', '.join(entry.keys())
                values = ', '.join(f"%({key})s" for key in entry.keys())
                insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values}) ON CONFLICT DO NOTHING"
                self.conn.cursor.execute(insert_query, entry)
                self.conn.connection.commit()
            except Exception as e:
                print(f"Error inserting data: {e}")
                self.conn.connection.rollback()

    def close(self):
        # Close the database connection
        self.conn.close()

    def check_table_if_not_create(self,table:str):
        if table == "order_book":
            create_table_query = """
            CREATE TABLE IF NOT EXISTS order_book (
                id SERIAL PRIMARY KEY,
                bid NUMERIC,
                ask NUMERIC,
                time TIMESTAMP,
                symbol VARCHAR(20)
            )
            """
        elif table == "trades":
            create_table_query = """
            CREATE TABLE IF NOT EXISTS trades (
                id SERIAL PRIMARY KEY,
                price NUMERIC,
                qty NUMERIC,
                time TIMESTAMP,
                symbol VARCHAR(20)
            )
            """
        else:
            raise ValueError("Unknown table name")
        try:
            self.conn.cursor.execute(create_table_query)
            self.conn.connection.commit()
        except Exception as e:
            print(f"Error creating table: {e}")
            self.conn.connection.rollback()
