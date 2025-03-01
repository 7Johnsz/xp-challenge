from fastapi import Request, status, Response
from fastapi.responses import ORJSONResponse
from ......services.auth import AuthService
from .....config.database import database
from ......services.auth import find_key
from .....config.api import router
from ......models.buy_schema import Buy

import datetime

@router.post("/stockmarket/buy", response_class=ORJSONResponse)
@AuthService
async def buy_asset(request: Request, response: Response, buy_asset: Buy):
    try:
        user_key = find_key(request.headers.get('Authorization').split()[1])[0]
        id_user = database.query("SELECT CodClient FROM client WHERE email = %s", (user_key,))[0][0]

        asset_price = database.query("SELECT price FROM asset WHERE ticker = %s", (buy_asset.ticker,))[0][0]
        asset_name = database.query("SELECT name FROM asset WHERE ticker = %s", (buy_asset.ticker,))[0][0]
        
        database.execute("UPDATE asset SET quantity = quantity - %s WHERE ticker = %s",
                        (buy_asset.quantity, buy_asset.ticker))

        if database.query("SELECT * FROM asset_client WHERE ticker = %s AND CodClient = %s", (buy_asset.ticker, id_user)):
            database.execute("UPDATE asset_client SET quantity = quantity + %s WHERE ticker = %s AND CodClient = %s",
                            (buy_asset.quantity, buy_asset.ticker, id_user))
        else:
            database.execute("INSERT INTO asset_client (ticker, CodClient, quantity) VALUES (%s, %s, %s)",
                            (buy_asset.ticker, id_user, buy_asset.quantity))
        
        database.execute("INSERT INTO transaction (CodClient, ticker, quantity, price, transaction_type) VALUES (%s, %s, %s, %s, %s)",
                        (id_user, buy_asset.ticker, buy_asset.quantity, asset_price, "BUY"))
        
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