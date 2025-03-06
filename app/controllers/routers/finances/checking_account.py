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
    """
    Endpoint to retrieve the account details and assets of a user.

    This endpoint allows authenticated users to retrieve their account details, including balance and the date the 
    account was created, as well as a list of their assets (stocks they own).

    Parameters:
    - **request** (Request): The incoming HTTP request containing authorization headers.
    - **response** (Response): The response object to modify HTTP status codes.

    Returns:
    - **200 OK**: If the account details are retrieved successfully.
    - **500 Internal Server Error**: If an unexpected error occurs.

    Response Structure:
    ```json
    {
        "status": "success",
        "message": "Account details fetched successfully.",
        "account_details": {
            "email": "user@example.com",
            "balance": 1000.50,
            "created_at": "2025-03-06 12:34:56"
        },
        "assets": [
            {
                "ticker": "ABC",
                "quantity": 100
            },
            {
                "ticker": "XYZ",
                "quantity": 50
            }
        ],
        "datetime": "2025-03-06 12:34:56"
    }
    ```

    Raises:
    - **HTTPException**: If an unexpected error occurs during the retrieval of the account details or assets.
    """
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
                
        balance = database.query("SELECT balance FROM client WHERE email = %s", (user_key,))[0][0]
        created_at = database.query("SELECT created_at FROM client WHERE email = %s", (user_key,))[0][0]

        assets_results = database.query("SELECT * FROM asset_client WHERE CodClient = %s", (id_user,))

        print(assets_results)

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
                "quantity": asset[2]
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
