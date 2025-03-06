from ....services.admin import AdminAuthService
from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ...config.database import database
from ....services.auth import find_key
from ...config.api import router

import datetime

@router.get("/admin/users", response_class=ORJSONResponse)
@AdminAuthService
async def users(request: Request, response: Response):
    """
    Endpoint to fetch the list of all clients, ordered by their creation date.

    Args:
    - request (Request): The request object from FastAPI.
    - response (Response): The response object from FastAPI.

    Returns:
    - ORJSONResponse: A JSON response containing the client information or an error message if something goes wrong.

    Success Response:
    - {
        "status": "success",
        "message": "Client history fetched successfully.",
        "client": [
            {"id": 1, "email": "user1@example.com", "balance": 1000.00, "created_at": "2025-03-06 12:34:56"},
            {"id": 2, "email": "user2@example.com", "balance": 2000.00, "created_at": "2025-03-05 11:45:30"}
        ],
        "datetime": "2025-03-06 12:34:56"
    }

    Error Response:
    - {
        "status": "error",
        "message": "Internal server error",
        "datetime": "2025-03-06 12:34:56"
    }
    """
    try:
        client_results = database.query("SELECT * FROM client ORDER BY created_at DESC")
        
        client_info = []
        for client in client_results:
            client_info.append({
                "id": client[0],
                "email": client[1],
                "balance": client[3],
                "created_at": client[4]
            })
        
        return {
            "status": "success",
            "message": "Client history fetched successfully.",
            "client": client_info,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
