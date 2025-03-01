from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ......services.auth import AuthService
from .....config.database import database
from ......services.auth import find_key
from .....config.api import router

import datetime

@router.get("/stockmarket", response_class=ORJSONResponse)
@AuthService
async def stockmarket(request: Request, response: Response):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        stockmarket = database.query("SELECT * FROM asset")
        
        assets = []
        for stock in stockmarket:
            assets.append({
                "id": stock[0],
                "name": stock[1],
                "ticker": stock[2],
                "price": stock[3],
                "quantity": stock[4],
                "created_at": stock[5]})
    
        return {
            "status": "success",
            "message": "Current stock market successfully obtained.",
            "email": user_key,
            "stockmarket": assets,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}