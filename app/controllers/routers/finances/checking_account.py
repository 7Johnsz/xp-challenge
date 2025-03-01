from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....services.auth import AuthService
from ...config.database import database
from ....services.auth import find_key
from ...config.api import router

import datetime

@router.get("/account", response_class=ORJSONResponse)
@AuthService
async def checking_account(request: Request, response: Response):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
                
        balance = database.query("SELECT balance FROM client WHERE email = %s", (user_key,))[0][0]
        created_at = database.query("SELECT created_at FROM client WHERE email = %s", (user_key,))[0][0]

        deposit_results = database.query("SELECT * FROM deposit_history WHERE CodClient = %s", (id_user,))
        withdraw_results = database.query("SELECT * FROM withdraw_history WHERE CodClient = %s", (id_user,))
        
        deposit_history = []
        for deposit in deposit_results:
            deposit_history.append({
                "id": deposit[0],
                "amount": deposit[2],
                "transaction_at": deposit[3]
            })
            
        withdraw_history = []
        for withdraw in withdraw_results:
            withdraw_history.append({
                "id": withdraw[0],
                "amount": withdraw[2],
                "transaction_at": withdraw[3]
            })
        
        return {
            "status": "success",
            "message": "Account details fetched successfully.",
            "account_details": {
                "email": user_key,
                "balance": balance,
                "created_at": created_at
            },
            "deposit_history": deposit_history,
            "withdraw_history": withdraw_history,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}