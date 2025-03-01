from pydantic import BaseModel, Field

class Buy(BaseModel):
    ticker: str
    quantity: int = Field(gt=0)
    
    class Config:
        extra = "forbid"
        