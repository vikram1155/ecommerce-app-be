from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4
from typing import List

class User(BaseModel):
    userId: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    email: EmailStr
    phone: str 
    age: int
    password: str  
    admin: bool = False
    favorites: List[str] = [] 

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class UpdateFavoritesRequest(BaseModel):
    favorite_products: List[str] 