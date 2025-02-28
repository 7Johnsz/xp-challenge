from ..controllers.config.database import redis_conn
import uuid
def generate_uuid() -> str:
    return str(uuid.uuid4())

def get_token(token: str):
    if redis_conn.get(token):
        return generate_uuid()
    return token
    