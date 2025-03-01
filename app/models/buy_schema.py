from pydantic import BaseModel, Field

class BuyandSell(BaseModel):
    ticker: str
    quantity: int = Field(gt=0)
    
    class Config:
        extra = "forbid"
        