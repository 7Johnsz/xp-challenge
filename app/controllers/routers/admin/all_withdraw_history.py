from ....services.admin import AdminAuthService
from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ...config.database import database
from ....services.auth import find_key
from ...config.api import router

import datetime

@router.get("/admin/withdraw-history", response_class=ORJSONResponse)
async def all_withdraw_history(request: Request, response: Response):
    """
    @AdminAuthService
    async def all_withdraw_history(request: Request, response: Response):
    Endpoint to fetch the withdraw history of all users.

    Args:
    - request (Request): The request object from FastAPI.
    - response (Response): The response object from FastAPI.

    Returns:
    - ORJSONResponse: A JSON response containing the withdraw history of all users or an error message if something goes wrong.

    Success Response:
    - {
        "status": "success",
        "message": "Withdraw history fetched successfully.",
        "withdraw_history": [
            {"id": 1, "id_user": 101, "amount": 100.00, "transaction_at": "2025-03-06 12:34:56"},
            {"id": 2, "id_user": 102, "amount": 200.00, "transaction_at": "2025-03-05 11:45:30"}
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
        withdraw_results = database.query("SELECT * FROM withdraw_history ORDER BY CodWithdraw DESC")
        
        withdraw_info = []
        for withdraw in withdraw_results:
            withdraw_info.append({
                "id": withdraw[0],
                "id_user": withdraw[1],
                "amount": withdraw[2],
                "transaction_at": withdraw[3]})
        
        return {
            "status": "success",
            "message": "Withdraw history fetched successfully.",
            "withdraw_history": withdraw_info,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
