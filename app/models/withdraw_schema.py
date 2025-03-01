from pydantic import BaseModel, Field

class Withdraw(BaseModel):
    value: float = Field(gt=0)
    
    class Config:
        extra = "forbid"