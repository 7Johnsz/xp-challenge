from fastapi import Request, status, Response
from ....models.withdraw_schema import Withdraw
from fastapi.responses import ORJSONResponse
from ....services.auth import AuthService
from ...config.database import redis_conn  
from ...config.database import database
from ...config.api import router
from ....services.auth import find_key

import datetime

@router.patch("/withdraw", response_class=ORJSONResponse)
@AuthService
async def withdraw(request: Request, response: Response, withdraw_data: Withdraw):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]                
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        balance = database.query("SELECT balance FROM client WHERE email = %s", (user_key,))[0][0]
       
        if withdraw_data.value > balance:
            database.conn.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "Insufficient balance.",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        else:
            database.execute("UPDATE client SET balance = balance - %s WHERE CodClient = %s", (withdraw_data.value, id_user))
            database.execute("INSERT INTO withdraw_history (CodClient, value) VALUES (%s, %s)", (id_user, withdraw_data.value))
                        
        return {
            "status": "success",
            "message": "Deposit processed successfully.",
            "deposit_details": {
                "email": user_key,
                "amount": withdraw_data.value},
            "account_summary": {
                "new_balance": database.query("SELECT balance FROM client WHERE email = %s",
                                              (user_key,))[0][0],
                "previous_balance": balance},
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}