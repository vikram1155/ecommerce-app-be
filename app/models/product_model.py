from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime

class Product(BaseModel):
    productId: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    weight: str
    category: str
    price: float
    favorited: bool = False
    inCart: bool = False
    ratings: float
    no_of_ratings: int
    description: str
    offer: int
    features: str
    protein: int
    carbs: int
    fat: int
    veg_nonveg: str
    etd: float
    type: str
    image: str
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    favorited: bool = False
    inCart: bool = False
    ratings: Optional[float] = None
    no_of_ratings: Optional[int] = None
    description: Optional[str] = None
    offer: Optional[float] = None
    features: Optional[str] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    veg_nonveg: Optional[str] = None
    etd: Optional[int] = None
    type: Optional[str] = None
    image: Optional[str] = None
