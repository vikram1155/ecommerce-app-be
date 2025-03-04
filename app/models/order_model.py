from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from datetime import datetime
from typing import List


class OrderItem(BaseModel):
    orderId: str = Field(default_factory=lambda: str(uuid4()))  # UUID v4
    status: str
    orderedOnDate: datetime = Field(default_factory=datetime.utcnow)
    costWhenOrdered: float
    productId: str
    quantity: float
    productName: str

class Order(BaseModel):
    userId: str  # Unique user identifier
    ordersList: List[OrderItem] = []  # List of orders per user


class OrderStatus(str, Enum):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderedByUser(BaseModel):
    userId: str  # UUID v4
    userEmail: EmailStr
    quantity: int
    status: OrderStatus = OrderStatus.PROCESSING  # Default to "Processing"
    orderedOnDate: datetime = Field(default_factory=datetime.utcnow)

class OrderUpdate(BaseModel):
    orderId: str
    newStatus: OrderStatus
