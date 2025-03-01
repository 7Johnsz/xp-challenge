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

        assets_results = database.query("SELECT * FROM asset_client WHERE CodClient = %s", (id_user,))

        if len(assets_results) == 0:
            return {
                "status": "success",
                "message": "Account details fetched successfully.",
                "account_details": {
                    "email": user_key,
                    "balance": balance,
                    "created_at": created_at
                },
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        assets_info = []
        for asset in assets_results:
            assets_info.append({
                "ticker": asset[0],
                "quantity": asset[1]
            })
        
        return {
            "status": "success",
            "message": "Account details fetched successfully.",
            "account_details": {
                "email": user_key,
                "balance": balance,
                "created_at": created_at
            },
            "assets": assets_info,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}