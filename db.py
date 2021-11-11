import mysql.connector
from mysql.connector.errors import Error

class DB:
    """ Клас, який дозволяє зручно користуватись БД """

    def __init__(self,hostname = "localhost", db_username = "dbAdmin", db_password = "War123456", db_name = "mydb"):
        self.hostname = hostname
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.connection = None
    

    def create_connection(self):
        try:
            conn = mysql.connector.connect(
                host = self.hostname,
                user = self.db_username,
                passwd = self.db_password
            )
        except Error as e:
            print(f"[DB.py] [Error] {e}")
            self.connection = None
        else:
            print(f"[DB.py] [Success] Connected to database")
            self.connection = conn
            cursor = self.connection.cursor()
            cursor.execute("use mydb;")
            cursor.fetchall()
    
    

    def select(self,raw_rows : str or list,table : str):
        try:
            rows = ",".join(raw_rows) if isinstance(raw_rows,list) else raw_rows
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {rows} FROM {table}")
            output = cursor.fetchall()
            return output
        except Error as e:
            print(f"[DB.py] [Error] SELECT {e}")
    

    def insert(self,data : dict, table : str):
        try:
            cursor = self.connection.cursor()
            values = "','".join(data.values())
            query = f"INSERT INTO {table}({','.join(data.keys())}) VALUES ('{values}');"
            print(f"[DB.py] [INFO] query == {query}")
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"[DB.py] [Error] INSERT {e}")

        
        
    