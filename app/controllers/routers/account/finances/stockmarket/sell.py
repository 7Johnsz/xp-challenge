from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ......services.auth import AuthService
from .....config.database import database
from ......services.auth import find_key
from .....config.api import router
from ......models.buy_schema import BuyandSell

import datetime

@router.post("/stockmarket/sell", response_class=ORJSONResponse)
@AuthService
async def sell_asset(request: Request, response: Response, sell_asset: BuyandSell):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]

        asset_price = database.query("SELECT price FROM asset WHERE ticker = %s", (sell_asset.ticker,))[0][0]
        asset_name = database.query("SELECT name FROM asset WHERE ticker = %s", (sell_asset.ticker,))[0][0]
        
        if sell_asset.quantity > database.query("SELECT quantity FROM asset_client WHERE ticker = %s AND CodClient = %s", (sell_asset.ticker, id_user))[0][0]:
            database.conn.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "error",
                "message": "You don't own enough of this asset",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        if database.query("SELECT * FROM asset_client WHERE ticker = %s AND CodClient = %s", (sell_asset.ticker, id_user)):
            database.execute("UPDATE asset SET quantity = quantity + %s WHERE ticker = %s", (sell_asset.quantity, sell_asset.ticker))
            database.execute("UPDATE asset_client SET quantity = quantity - %s WHERE ticker = %s AND CodClient = %s",
                            (sell_asset.quantity, sell_asset.ticker, id_user))
        else:
            return {
                "status": "error",
                "message": "You don't own this asset",
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        database.execute("INSERT INTO transaction (CodClient, ticker, quantity, price, transaction_type) VALUES (%s, %s, %s, %s, %s)",
                        (id_user, sell_asset.ticker, sell_asset.quantity, asset_price, "SELL"))
        
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
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}