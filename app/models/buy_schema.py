from pydantic import BaseModel, Field, ConfigDict

class BuyandSell(BaseModel):
    ticker: str
    quantity: int = Field(gt=0)
    
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )