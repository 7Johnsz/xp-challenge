# from fastapi.middleware.gzip import GZipMiddleware
from .controllers.routers.account.finances import checking_account as account
from .controllers.routers.account.finances import deposit_history
from .controllers.routers.account.finances import deposit
from .controllers.routers.account import signup
from .controllers.routers.account import login
from fastapi import FastAPI

app = FastAPI(docs="/docs")

# app.add_middleware(GZipMiddleware)
app.include_router(deposit_history.router)
app.include_router(deposit.router)
app.include_router(account.router)
app.include_router(signup.router)
app.include_router(login.router)

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/ping")
async def ping():
    return "Pong!"
