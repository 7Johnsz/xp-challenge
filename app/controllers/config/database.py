from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

class Database:
    def __init__(self) -> None:
        try:
            self.config = {
                'database': os.getenv('DATABASE'),
                'user': os.getenv('DATABASE_USER'), 
                'password': os.getenv('DATABASE_PASSWORD'),
                'host': os.getenv('DATABASE_HOST'),
                'port': os.getenv('DATABASE_PORT')}
            
            self.conn = psycopg2.connect(**self.config)
            self.conn.autocommit = False
             
        except Exception as e:
            raise Exception(f"Database connection failed: {e}")

    def __del__(self) -> None:
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def query(self, sql: str, params: tuple = ()) -> list:
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute(self, sql: str, params: tuple = ()) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            self.conn.commit()


database = Database()
