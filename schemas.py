from typing import Optional
from pydantic import BaseModel, PositiveFloat

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: PositiveFloat
    tax: Optional[PositiveFloat] = None

    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    tax: Optional[PositiveFloat] = None

    class Config:
        from_attributes = True
        
