from .....models.buy_schema import BuyandSell
from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ....config.api import router, limiter
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key

import datetime

@router.post("/stockmarket/buy", response_class=ORJSONResponse)
@limiter.limit("30/minute")
@AuthService
async def buy_asset(request: Request, response: Response, buy_asset: BuyandSell):
    """
    Endpoint to buy an asset in the stock market.
    
    This endpoint allows authenticated users to buy an asset by specifying its ticker and quantity. 
    It checks the availability, user's balance, and records the transaction.
    
    Parameters:
    - **request** (Request): The incoming HTTP request containing authorization headers.
    - **response** (Response): The response object to modify HTTP status codes.
    - **buy_asset** (BuyandSell): A Pydantic model containing the ticker and quantity of the asset to be bought.
    
    Returns:
    - **200 OK**: If the purchase is successful.
    - **400 Bad Request**: If the asset does not exist or if the user has insufficient balance.
    - **500 Internal Server Error**: If an unexpected error occurs.
    
    Response Structure:
    ```json
    {
        "status": "success",
        "message": "Asset bought successfully",
        "email": "user@example.com",
        "stockmarket": {
            "name": "Company XYZ",
            "ticker": "XYZ",
            "quantity": 10
        },
        "datetime": "2025-03-06 12:34:56"
    }
    ```
    
    Raises:
    - **HTTPException**: If an unexpected error occurs during the transaction.
    """
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]

        asset_data = database.query("SELECT name, price, quantity FROM asset WHERE ticker = %s", (buy_asset.ticker,))
        if not asset_data:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "Asset does not exist",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        asset_name, asset_price, asset_available_quantity = asset_data[0]
                
        user_balance = database.query("SELECT balance FROM client WHERE email = %s", (user_key,))[0][0]
        total_price = asset_price * buy_asset.quantity

        if user_balance < total_price:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "Insufficient balance",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        if buy_asset.quantity > asset_available_quantity:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "Not enough assets available for purchase",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        database.execute("UPDATE asset SET quantity = quantity - %s WHERE ticker = %s", (buy_asset.quantity, buy_asset.ticker))
        database.execute("INSERT INTO asset_client (CodClient, ticker, quantity) VALUES (%s, %s, %s) ON CONFLICT (CodClient, ticker) DO UPDATE SET quantity = asset_client.quantity + EXCLUDED.quantity",
                        (id_user, buy_asset.ticker, buy_asset.quantity))
        database.execute("INSERT INTO transaction (CodClient, ticker, quantity, price, transaction_type) VALUES (%s, %s, %s, %s, %s)",
                        (id_user, buy_asset.ticker, buy_asset.quantity, asset_price, "BUY"))
        database.execute("UPDATE client SET balance = balance - %s WHERE email = %s", (total_price, user_key))
        
        return {
            "status": "success",
            "message": "Asset bought successfully",
            "email": user_key,
            "stockmarket": {
                "name": asset_name,
                "ticker": buy_asset.ticker,
                "quantity": buy_asset.quantity},
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
         
    except Exception as e:
        database.conn.rollback()
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
