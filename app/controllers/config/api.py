from slowapi.util import get_remote_address
from fastapi import APIRouter
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()