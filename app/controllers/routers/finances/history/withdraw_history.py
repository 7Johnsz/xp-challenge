from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key
from ....config.api import router

import datetime

@router.get("/withdraw-history", response_class=ORJSONResponse)
@AuthService
async def withdraw_history(request: Request, response: Response):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        withdraw_results = database.query("SELECT * FROM withdraw_history WHERE CodClient = %s", (id_user,))
        
        withdraw_results = []
        for withdraw in withdraw_results:
            withdraw_results.append({
                "id": withdraw[0],
                "amount": withdraw[2],
                "transaction_at": withdraw[3]})
        
        return {
            "status": "success",
            "message": "Withdraw history fetched successfully.",
            "email": user_key,
            "withdraw_history": withdraw_results,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}