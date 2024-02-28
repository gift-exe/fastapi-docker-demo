from typing import Optional
from pydantic import BaseModel, PositiveFloat
from models import Item as MItem

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: PositiveFloat
    tax: Optional[float] = None

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, db_item: MItem) -> "Item":
        return cls (
            name = db_item.name,
            description = db_item.description,
            price = db_item.price,
            tax = db_item.tax
        )
        

class ItemUpdate(BaseModel):
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    tax: Optional[float] = None

    class Config:
        from_attributes = True
        
