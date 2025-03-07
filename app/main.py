from .controllers.routers.finances import withdraw, deposit, checking_account as account
from .controllers.routers.admin import all_withdraw_history, all_deposit_history, users
from .controllers.routers.finances.stockmarket import asset, sell, buy, transactions
from .controllers.routers.finances.history import withdraw_history, deposit_history
from .controllers.routers.account import signup, login

from fastapi.middleware.gzip import GZipMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

app = FastAPI(docs="/docs", openapi_url="/openapi.json")

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(all_withdraw_history.router)
app.include_router(all_deposit_history.router)
app.include_router(withdraw_history.router)
app.include_router(deposit_history.router)
app.include_router(transactions.router)
app.include_router(withdraw.router)
app.include_router(deposit.router)
app.include_router(account.router)
app.include_router(signup.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(asset.router)
app.include_router(sell.router)
app.include_router(buy.router)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "message": "Rate limit exceeded. Try again later."})

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/ping")
async def ping():
    return "Pong!"
