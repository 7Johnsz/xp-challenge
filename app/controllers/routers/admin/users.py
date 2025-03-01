from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....services.admin import AdminAuthService
from ...config.database import database
from ....services.auth import find_key
from ...config.api import router

import datetime

@router.get("/admin/users", response_class=ORJSONResponse)
@AdminAuthService
async def all_deposit_history(request: Request, response: Response):
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