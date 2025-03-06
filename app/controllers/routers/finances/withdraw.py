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
    """
    Endpoint to process a withdrawal from the user's account.

    This endpoint allows authenticated users to withdraw an amount from their account, ensuring that the balance is sufficient.
    If the withdrawal is successful, the balance is updated, and the withdrawal is recorded in the withdrawal history.

    Parameters:
    - **request** (Request): The incoming HTTP request containing authorization headers.
    - **response** (Response): The response object to modify HTTP status codes.
    - **withdraw_data** (Withdraw): The data containing the withdrawal amount.

    Returns:
    - **200 OK**: If the withdrawal is processed successfully.
    - **400 Bad Request**: If the withdrawal exceeds the available balance.
    - **500 Internal Server Error**: If an unexpected error occurs.

    Response Structure:
    ```json
    {
        "status": "success",
        "message": "Withdrawal processed successfully.",
        "withdrawal_details": {
            "email": "user@example.com",
            "amount": 500.00
        },
        "account_summary": {
            "new_balance": 1500.00,
            "previous_balance": 2000.00
        },
        "datetime": "2025-03-06 12:34:56"
    }
    ```

    Raises:
    - **HTTPException**: If an unexpected error occurs during the withdrawal process.
    """
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]                
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]
        balance = database.query("SELECT balance FROM client WHERE email = %s", (user_key,))[0][0]
        
        # Check if the user has sufficient balance
        if withdraw_data.value > balance:
            database.conn.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "Insufficient balance.",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # Process the withdrawal
        database.execute("UPDATE client SET balance = balance - %s WHERE CodClient = %s", (withdraw_data.value, id_user))
        database.execute("INSERT INTO withdraw_history (CodClient, value) VALUES (%s, %s)", (id_user, withdraw_data.value))
        
        # Return success response
        return {
            "status": "success",
            "message": "Withdrawal processed successfully.",
            "withdrawal_details": {
                "email": user_key,
                "amount": withdraw_data.value
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
