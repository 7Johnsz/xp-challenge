from pydantic import BaseModel, Field

class Deposit(BaseModel):
    value: float = Field(gt=0)
    
    class Config:
        extra = "forbid"