from pydantic import BaseModel
from typing import Optional

class RestaurantCreate(BaseModel):
    name: str
    address: str
    hours_of_operation: str
    owner_id: int

class RestaurantUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    hours_of_operation: Optional[str]

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    available: bool = True

class MenuItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    available: Optional[bool]

class OrderUpdate(BaseModel):
    status: str
