from ..controllers.config.database import redis_conn
from fastapi import Request, HTTPException, status
from typing import Optional, List
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps

import os

load_dotenv()

api_key = os.getenv('ADMIN_KEY')

def AdminAuthService(func):
    """
    A decorator to ensure that the request has the correct Authorization header.
    This decorator checks if the Authorization header in the request matches the expected value.
    If it does, it proceeds to execute the wrapped function. Otherwise, it raises an HTTPException with a status code of 401.

    Returns:
    Callable: The wrapped function with Authorization header check.

    Raises:
    HTTPException: If the Authorization header does not match the expected value.
    """
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        now = datetime.now().isoformat()

        if auth_header == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "You don't have permission to access this page",
                    "timestamp": now
                })
            
        auth_result = auth_header.split()[1]

        if auth_result != api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "You don't have permission to access this page",
                    "timestamp": now
                })
            
        return await func(request, *args, **kwargs)
    return wrapper