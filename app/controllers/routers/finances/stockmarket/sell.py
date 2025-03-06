from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from .....services.auth import AuthService
from ....config.database import database
from .....services.auth import find_key
from ....config.api import router
from .....models.buy_schema import BuyandSell

import datetime

@router.post("/stockmarket/sell", response_class=ORJSONResponse)
@AuthService
async def sell_asset(request: Request, response: Response, sell_asset: BuyandSell):
    """
    Endpoint to sell an asset in the stock market.
    
    This endpoint allows authenticated users to sell an asset by specifying its ticker and quantity. 
    It checks if the asset exists, if the user owns the asset in the specified quantity, and records the transaction.
    
    Parameters:
    - **request** (Request): The incoming HTTP request containing authorization headers.
    - **response** (Response): The response object to modify HTTP status codes.
    - **sell_asset** (BuyandSell): A Pydantic model containing the ticker and quantity of the asset to be sold.
    
    Returns:
    - **200 OK**: If the sale is successful.
    - **400 Bad Request**: If the user does not own enough of the asset or if other validation fails.
    - **404 Not Found**: If the asset or the user's ownership of the asset is not found.
    - **500 Internal Server Error**: If an unexpected error occurs.
    
    Response Structure:
    ```json
    {
        "status": "success",
        "message": "Asset sold successfully",
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

        if database.query("SELECT * FROM asset WHERE ticker = %s", (sell_asset.ticker,)) == []:
            database.conn.rollback()
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "Asset not found",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        asset_price = database.query("SELECT price FROM asset WHERE ticker = %s", (sell_asset.ticker,))[0][0]
        asset_name = database.query("SELECT name FROM asset WHERE ticker = %s", (sell_asset.ticker,))[0][0]
                
        if database.query("SELECT quantity FROM asset_client WHERE ticker = %s", (sell_asset.ticker,)) == []:
            database.conn.rollback()
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "You don't own this asset",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        if sell_asset.quantity > database.query("SELECT quantity FROM asset_client WHERE ticker = %s AND CodClient = %s", (sell_asset.ticker, id_user))[0][0]:
            database.conn.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "You don't own enough of this asset",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        database.execute("UPDATE asset SET quantity = quantity + %s WHERE ticker = %s", (sell_asset.quantity, sell_asset.ticker))
        database.execute("UPDATE asset_client SET quantity = quantity - %s WHERE ticker = %s AND CodClient = %s",
                        (sell_asset.quantity, sell_asset.ticker, id_user))
        database.execute("INSERT INTO transaction (CodClient, ticker, quantity, price, transaction_type) VALUES (%s, %s, %s, %s, %s)",
                        (id_user, sell_asset.ticker, sell_asset.quantity, asset_price, "SELL"))
        database.execute("UPDATE client SET balance = balance + %s WHERE email = %s", (asset_price * sell_asset.quantity, user_key))
        
        return {
            "status": "success",
            "message": "Asset sold successfully",
            "email": user_key,
            "stockmarket": {
                "name": asset_name,
                "ticker": sell_asset.ticker,
                "quantity": sell_asset.quantity},
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
         
    except Exception as e:
        database.conn.rollback()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
