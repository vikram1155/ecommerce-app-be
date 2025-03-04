from fastapi import APIRouter, HTTPException
from app.database import orders_collection
from app.models.order_model import Order, OrderItem
from bson.objectid import ObjectId
from datetime import datetime
from typing import List, Optional
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get("/orders")
async def get_all_orders():
    orders = await orders_collection.find({}, {"_id": 0}).to_list(length=None)
    message = "No Orders Found" if not orders else "Orders fetched successfully"
    return success_response(orders, message)

# 📌 Get Orders for a User
@router.get("/orders/user")
async def get_orders(userId: Optional[str] = None):
    if not userId:
        raise HTTPException(status_code=400, detail="userId is required")

    user_orders = await orders_collection.find_one({"userId": userId}, {"_id": 0})
    message = "No Orders Placed" if not user_orders else "Orders fetched successfully"
    return success_response(user_orders, message)

# # 📌 Get All Orders (For All Users)
# @router.get("/orders")
# async def get_all_orders():
#     orders = await orders_collection.find({}, {"_id": 0}).to_list(length=None)
#     return success_response(orders, "Orders fetched successfully")

# 📌 Create Orders (Add to User's Order List)
@router.post("/orders/create")
async def create_orders(order_data: Order):
    existing_order = await orders_collection.find_one({"userId": order_data.userId})

    if existing_order:
        # Append new orders to the existing order list
        new_orders = [order.dict() for order in order_data.ordersList]
        await orders_collection.update_one(
            {"userId": order_data.userId},
            {"$push": {"ordersList": {"$each": new_orders}}}
        )
        message = "Orders added successfully"
    else:
        # Create a new order document for the user
        await orders_collection.insert_one(order_data.dict())
        message = "Order created successfully"

    return success_response(order_data.dict(), message)

# 📌 Update an Existing Order in User's Order List
@router.put("/orders/{userId}/{orderId}")
async def update_order(userId: str, orderId: str, updated_order: OrderItem):
    result = await orders_collection.update_one(
        {"userId": userId, "ordersList.orderId": orderId},
        {"$set": {"ordersList.$": updated_order.dict()}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return success_response({}, "Order updated successfully")

# 📌 Delete an Order from User's Order List
@router.delete("/orders/{userId}/{orderId}")
async def delete_order(userId: str, orderId: str):
    result = await orders_collection.update_one(
        {"userId": userId},
        {"$pull": {"ordersList": {"orderId": orderId}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return success_response({}, "Order deleted successfully")
