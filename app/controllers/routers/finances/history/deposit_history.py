from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....config.api import router, limiter
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key

import datetime

@router.get("/deposit-history", response_class=ORJSONResponse)
@limiter.limit("30/minute")
@AuthService
async def deposit_history(request: Request, response: Response):
    """
    Endpoint to fetch deposit history of a user.

    Args:
    - request (Request): The request object from FastAPI.
    - response (Response): The response object from FastAPI.

    Returns:
    - ORJSONResponse: A JSON response object containing the deposit history of the user.
    """
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        deposit_results = database.query("SELECT * FROM deposit_history WHERE CodClient = %s", (id_user,))
        
        if deposit_results is None:
            database.conn.rollback()
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "Deposit history not found.",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        if not deposit_results:
            database.conn.rollback()
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "Deposit history not found.",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        deposit_history = []
        for deposit in deposit_results:
            deposit_history.append({
                "id": deposit[0],
                "amount": deposit[2],
                "transaction_at": deposit[3]})
        
        return {
            "status": "success",
            "message": "Deposit history fetched successfully.",
            "email": user_key,
            "deposit_history": deposit_history,
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