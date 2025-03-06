from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key
from ....config.api import router

import datetime

@router.get("/stockmarket", response_class=ORJSONResponse)
@AuthService
async def stockmarket(request: Request, response: Response):
    """
    Endpoint to retrieve the current stock market data.

    This endpoint allows authenticated users to view the full list of available assets in the stock market, including 
    their name, ticker symbol, price, quantity, and creation date.

    Parameters:
    - **request** (Request): The incoming HTTP request containing authorization headers.
    - **response** (Response): The response object to modify HTTP status codes.

    Returns:
    - **200 OK**: If the stock market data is retrieved successfully.
    - **500 Internal Server Error**: If an unexpected error occurs.

    Response Structure:
    ```json
    {
        "status": "success",
        "message": "Current stock market successfully obtained.",
        "email": "user@example.com",
        "stockmarket": [
            {
                "id": 1,
                "name": "Company ABC",
                "ticker": "ABC",
                "price": 100.50,
                "quantity": 500,
                "created_at": "2025-03-06 12:34:56"
            },
            {
                "id": 2,
                "name": "Company XYZ",
                "ticker": "XYZ",
                "price": 75.25,
                "quantity": 300,
                "created_at": "2025-03-06 12:34:56"
            }
        ],
        "datetime": "2025-03-06 12:34:56"
    }
    ```

    Raises:
    - **HTTPException**: If an unexpected error occurs during the retrieval of stock market data.
    """
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
