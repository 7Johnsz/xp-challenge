from ..controllers.config.database import redis_conn
from fastapi import Request, HTTPException, status
from typing import Optional, List
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps

load_dotenv()

def find_key(value: str) -> List[str]:
    """
    Find all keys in Redis that have a specific value
    Returns a list of keys that match the value
    """
    matching_keys = []
    for key in redis_conn.scan_iter():
        if redis_conn.get(key) == value:
            matching_keys.append(key)
    return matching_keys

def check_redis_value(value: str):
    """
    Check if a specific value exists in Redis database
    Returns a tuple of (exists: bool, keys: List[str])
    """
    matching_keys = find_key(value)
    return bool(matching_keys), matching_keys

def AuthService(func):
    """
    A decorator to ensure that the request has the correct Authorization header.
    """
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        now = datetime.now().isoformat()

        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "You don't have permission to access this page",
                    "timestamp": now
                }
            )

        try:
            auth_result = auth_header.split()[1]
            auth_response = check_redis_value(auth_result)

            if not auth_response[0]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "msg": "You don't have permission to access this page",
                        "timestamp": now
                    }
                )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "You don't have permission to access this page",
                    "timestamp": now
                }
            )

        return await func(request, *args, **kwargs)
    return wrapper
