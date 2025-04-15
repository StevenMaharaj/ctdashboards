import psycopg2

class DBConnection:
    def __init__(self, host="127.0.0.1", database="grafana", user="admin", password="admin_password"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            # Connect to PostgreSQL
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connection to PostgreSQL DB successful")
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection is closed")