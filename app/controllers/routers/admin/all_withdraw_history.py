from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....services.admin import AdminAuthService
from ...config.database import database
from ....services.auth import find_key
from ...config.api import router

import datetime

@router.get("/admin/withdraw-history", response_class=ORJSONResponse)
@AdminAuthService
async def all_withdraw_history(request: Request, response: Response):
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