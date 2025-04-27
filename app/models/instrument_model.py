
from pydantic import BaseModel, Field
from typing import Optional

class Instrument(BaseModel):
    name: str = Field(...)
    type: str = Field(...)
    brand: str = Field(...)
    price: float = Field(...)

class UpdateInstrument(BaseModel):
    name: Optional[str]
    type: Optional[str]
    brand: Optional[str]
    price: Optional[float]
