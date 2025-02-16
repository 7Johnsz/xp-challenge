from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ...config.database import database
from ....models.user import Client
from ...config.api import router

import datetime
import psycopg2

@router.post("/signup", response_class=ORJSONResponse)
async def signup(request: Request, client: Client, response: Response):
    try:
        database.execute(
            "INSERT INTO client (email, password, balance) VALUES (%s, %s, 0)",
            (client.email, client.password))

        response.status_code = status.HTTP_201_CREATED
        return {
                "status": "success",
                "message": "Client signed up successfully",
                "client_data": {
                    "email": client.email, "balance": 0},
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    except psycopg2.errors.UniqueViolation:
        database.conn.rollback()
        response.status_code = status.HTTP_409_CONFLICT
        return {
            "status": "error",
            "message": "Email address already exists",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except Exception as e:
        database.conn.rollback()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }