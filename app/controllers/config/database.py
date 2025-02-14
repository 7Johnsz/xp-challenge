from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            'database': os.getenv('DATABASE'),
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
            'host': os.getenv('HOST'),
            'port': os.getenv('PORT')
        }
        self.conn = psycopg2.connect(**self.config)

    def __del__(self):
        self.conn.close()

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor
    
database = Database()