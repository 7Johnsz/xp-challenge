# from fastapi.middleware.gzip import GZipMiddleware
from .controllers.routers.account import signup
from fastapi import FastAPI

app = FastAPI(docs="/docs")

# app.add_middleware(GZipMiddleware)
app.include_router(signup.router)

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/ping")
async def ping():
    return "Pong!"
