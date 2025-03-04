from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Union
from uuid import uuid4

class CartItem(BaseModel):
    productId: str
    quantity: int

class Cart(BaseModel):
    userId: str  # UUID v4
    userEmail: EmailStr
    productsInCart: List[CartItem] = Field(default_factory=list)  # List of cart items

class RemoveCartItemRequest(BaseModel):
    userId: str
    productId: str