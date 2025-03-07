from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....config.api import router, limiter
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key

import datetime

@router.get("/withdraw-history", response_class=ORJSONResponse)
@limiter.limit("30/minute")
@AuthService
async def withdraw_history(request: Request, response: Response):
    """
    Endpoint to fetch the withdraw history of a user.

    Args:
    - request (Request): The request object from FastAPI.
    - response (Response): The response object from FastAPI.

    Returns:
    - ORJSONResponse: A JSON response object containing the withdraw history of the user.
    """
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        withdraw_results = database.query("SELECT * FROM withdraw_history WHERE CodClient = %s", (id_user,))
                
        if not withdraw_results or len(withdraw_results) == 0:
            database.conn.rollback()
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "Withdraw history not found.",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        withdraw_info = []
        for withdraw in withdraw_results:
            withdraw_info.append({
                "id": withdraw[0],
                "amount": withdraw[2],
                "transaction_at": withdraw[3]})
                
        return {
            "status": "success",
            "message": "Withdraw history fetched successfully.",
            "email": user_key,
            "withdraw_history": withdraw_info,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
