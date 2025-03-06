from pydantic import BaseModel, Field, ConfigDict, field_validator

class BuyandSell(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    quantity: int = Field(gt=0)
    
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )
    
    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, value: str) -> str:
        return value.upper()