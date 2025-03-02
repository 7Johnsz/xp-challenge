from pydantic import BaseModel, ConfigDict

class Client(BaseModel):
    email: str
    password: str
    
    model_config = ConfigDict(
        extra="forbid",
        frozen=True  
    )