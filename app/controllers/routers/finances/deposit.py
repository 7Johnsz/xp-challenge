from fastapi import Request, status, Response
from ....models.deposit_schema import Deposit
from fastapi.responses import ORJSONResponse
from ....services.auth import AuthService
from ...config.database import redis_conn  
from ...config.database import database
from ...config.api import router, limiter
from ....services.auth import find_key

import datetime

@router.patch("/deposit", response_class=ORJSONResponse)
@limiter.limit("30/minute")
@AuthService
async def deposit(request: Request, response: Response, deposit_data: Deposit):
    """
    Endpoint to process a deposit into the user's account.

    This endpoint allows authenticated users to deposit an amount into their account. It updates the user's balance
    and records the deposit in the deposit history.

    Parameters:
    - **request** (Request): The incoming HTTP request containing authorization headers.
    - **response** (Response): The response object to modify HTTP status codes.
    - **deposit_data** (Deposit): The data containing the deposit amount.

    Returns:
    - **200 OK**: If the deposit is processed successfully.
    - **500 Internal Server Error**: If an unexpected error occurs.

    Response Structure:
    ```json
    {
        "status": "success",
        "message": "Deposit processed successfully.",
        "deposit_details": {
            "email": "user@example.com",
            "amount": 1000.00
        },
        "account_summary": {
            "new_balance": 2000.00,
            "previous_balance": 1000.00
        },
        "datetime": "2025-03-06 12:34:56"
    }
    ```

    Raises:
    - **HTTPException**: If an unexpected error occurs during the deposit process.
    """
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]                
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        balance = database.query("SELECT balance FROM client WHERE email = %s", (user_key,))[0][0]
        
        # Update balance and record the deposit history
        database.execute("UPDATE client SET balance = balance + %s WHERE CodClient = %s", (deposit_data.value, id_user))
        database.execute("INSERT INTO deposit_history (CodClient, value) VALUES (%s, %s)", (id_user, deposit_data.value))
        
        # Return success response
        return {
            "status": "success",
            "message": "Deposit processed successfully.",
            "deposit_details": {
                "email": user_key,
                "amount": deposit_data.value
            },
            "account_summary": {
                "new_balance": database.query("SELECT balance FROM client WHERE email = %s",
                                              (user_key,))[0][0],
                "previous_balance": balance
            },
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
            
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
