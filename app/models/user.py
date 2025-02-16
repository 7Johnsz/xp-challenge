from pydantic import BaseModel

class Client(BaseModel):
    email: str
    password: str
    
    class Config:
        extra = "forbid"