from dotenv import load_dotenv

import psycopg2
import redis
import os

load_dotenv()

class Database:
    def __init__(self) -> None:
        try:
            self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
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

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

if not redis_host or not redis_port:
    raise ValueError("REDIS_HOST and REDIS_PORT environment variables must be set")

redis_conn = redis.StrictRedis(host=redis_host,
                         port=int(redis_port),
                         db=0,
                         decode_responses=True)

database = Database()

