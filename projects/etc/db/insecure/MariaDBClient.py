import mysql.connector
from mysql.connector import Error

class MariaDBClient:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> bool:
        """MariaDB 서버 연결"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"Connected to MariaDB - {self.database}")
            return True
        except Error as e:
            print(f"Connection failed: {e}")
            return False

    def execute_query(self, query: str, params: tuple = None):
        """쿼리 실행"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.lower().startswith('select'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.rowcount
                
        except Error as e:
            print(f"Query failed: {e}")
            return None
        finally:
            cursor.close()

    def disconnect(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            print("Disconnected from MariaDB")