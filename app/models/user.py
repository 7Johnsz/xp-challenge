from pydantic import BaseModel, ConfigDict, Field, EmailStr

class Client(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )