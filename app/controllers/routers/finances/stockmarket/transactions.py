from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key
from ....config.api import router

import datetime

@router.get("/transactions", response_class=ORJSONResponse)
@AuthService
async def transactions(request: Request, response: Response):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        transactions_results = database.query("SELECT * FROM transaction WHERE CodClient = %s", (id_user,))
        
        transactions_history = []
        for transaction in transactions_results:
            transactions_history.append({
                "id": transaction[0],
                "id_client": transaction[1],
                "ticker": transaction[2],
                "quantity": transaction[3],
                "price": transaction[4],
                "transaction_type": transaction[5],
                "created_at": transaction[6]})
        
        return {
            "status": "success",
            "message": "Transactions retrieved successfully",
            "email": user_key,
            "history": transactions_history,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}