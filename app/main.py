# from fastapi.middleware.gzip import GZipMiddleware
from .controllers.routers.account.finances import checking_account as account
from .controllers.routers.account.finances.stockmarket import transactions
from .controllers.routers.account.finances.history import withdraw_history
from .controllers.routers.account.finances.history import deposit_history
from .controllers.routers.account.finances.stockmarket import asset
from .controllers.routers.account.finances.stockmarket import buy
from .controllers.routers.account.finances import withdraw
from .controllers.routers.account.finances import deposit
from .controllers.routers.account import signup
from .controllers.routers.account import login
from fastapi import FastAPI

app = FastAPI(docs="/docs")

# app.add_middleware(GZipMiddleware)
app.include_router(withdraw_history.router)
app.include_router(deposit_history.router)
app.include_router(transactions.router)
app.include_router(withdraw.router)
app.include_router(deposit.router)
app.include_router(account.router)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(asset.router)
app.include_router(buy.router)

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/ping")
async def ping():
    return "Pong!"
