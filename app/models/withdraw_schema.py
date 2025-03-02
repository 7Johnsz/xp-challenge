from pydantic import BaseModel, Field, ConfigDict

class Withdraw(BaseModel):
    value: float = Field(gt=0)

    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )