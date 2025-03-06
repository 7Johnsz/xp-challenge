from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....utils.token import generate_uuid
from ...config.database import redis_conn
from ...config.database import database
from ....utils.token import get_token
from ....models.user import Client
from ...config.api import router

import datetime
import psycopg2

@router.post("/login", response_class=ORJSONResponse)
async def signup(request: Request, response: Response, login: Client):
    """
    Endpoint to log in a client using their email and password.

    Args:
    - request (Request): The request object from FastAPI.
    - response (Response): The response object from FastAPI.
    - login (Client): Client model containing the user's email and password.

    Returns:
    - ORJSONResponse: A JSON response containing either a success message with access data
                      (refresh token and time-to-live) or an error message.

    Success Response (with access data):
    - {
        "status": "success",
        "message": "Client logged in successfully",
        "acess_data": {
            "refresh_token": "some_generated_token",
            "ttl": 6000
        },
        "datetime": "2025-03-06 12:34:56"
    }

    Error Responses:
    - 404 Not Found (Client unknown or password incorrect):
      {
          "status": "error",
          "message": "Client unknown or password incorrect",
          "datetime": "2025-03-06 12:34:56"
      }

    - 409 Conflict (Email address already exists):
      {
          "status": "error",
          "message": "Email address already exists",
          "datetime": "2025-03-06 12:34:56"
      }

    - 500 Internal Server Error (General error):
      {
          "status": "error",
          "message": "Internal server error",
          "datetime": "2025-03-06 12:34:56"
      }
    """
    try:
        user_Data = database.query(
            "SELECT * FROM client WHERE email = %s AND password = %s",
            (login.email, login.password))
                
        if user_Data != []:
            if redis_conn.exists(login.email):
                return {
                    "status": "success",
                    "message": "Client logged in successfully",
                    "acess_data": {
                        "refresh_token": redis_conn.get(login.email),
                        "ttl": redis_conn.ttl(login.email)},
                    "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            if not redis_conn.exists(login.email):
                redis_conn.set(login.email, generate_uuid(), ex=60 * 100)
                value = redis_conn.get(login.email)
                return {
                    "status": "success",
                    "message": "Client logged in successfully",
                    "acess_data": {
                        "refresh_token": value,
                        "ttl": redis_conn.ttl(value)},
                    "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        if user_Data == []:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "Client unknown or password incorrect",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
    except psycopg2.errors.UniqueViolation:
        database.conn.rollback()
        response.status_code = status.HTTP_409_CONFLICT
        return {
            "status": "error",
            "message": "Email address already exists",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}