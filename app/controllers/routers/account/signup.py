from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ...config.api import router, limiter
from ...config.database import database
from ....models.user import Client

import datetime
import psycopg2

@router.post("/signup", response_class=ORJSONResponse)
@limiter.limit("30/minute")
async def signup(request: Request, client: Client, response: Response):
    """
    Endpoint to sign up a new client.

    Args:
    - request (Request): The request object from FastAPI.
    - client (Client): The client model containing the user's email and password.
    - response (Response): The response object from FastAPI.

    Returns:
    - ORJSONResponse: A JSON response containing either a success message with client data (email and balance)
                      or an error message.

    Success Response:
    - 201 Created:
      {
          "status": "success",
          "message": "Client signed up successfully",
          "client_data": {
              "email": "client@example.com",
              "balance": 0
          },
          "datetime": "2025-03-06 12:34:56"
      }

    Error Responses:
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
        database.execute(
            "INSERT INTO client (email, password, balance) VALUES (%s, %s, 0)",
            (client.email, client.password))

        response.status_code = status.HTTP_201_CREATED
        return {
                "status": "success",
                "message": "Client signed up successfully",
                "client_data": {
                    "email": client.email, "balance": 0},
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
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}