from pydantic import BaseModel, Field, ConfigDict

class Deposit(BaseModel):
    value: float = Field(gt=0)
    
    model_config = ConfigDict(
        extra="forbid",
        frozen=True  
    )