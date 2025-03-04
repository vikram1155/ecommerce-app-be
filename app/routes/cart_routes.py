from fastapi import APIRouter, HTTPException
from app.database import carts_collection
from app.models.cart_model import Cart, CartItem, RemoveCartItemRequest
from app.utils.response import success_response, error_response
from typing import Optional, List
from bson import ObjectId

router = APIRouter()

# 📌 Get cart values for a user
@router.get("/cart")
async def get_cart(userId: str):
    cart = await carts_collection.find_one({"userId": userId}, {"_id": 0})
    message = "No products added in Cart" if not cart else "Cart details fetched successfully"
    return success_response(cart, message)

# 📌 Create or Update Cart
@router.post("/cart")
async def update_cart(cart_data: Cart):
    existing_cart = await carts_collection.find_one({"userId": cart_data.userId})

    if existing_cart:
        # If empty cart is received, clear the cart
        if not cart_data.productsInCart:
            await carts_collection.update_one(
                {"userId": cart_data.userId},
                {"$set": {"productsInCart": []}}
            )
            return success_response({}, "Cart emptied successfully")

        # Update existing cart
        product_map = {item["productId"]: item for item in existing_cart.get("productsInCart", [])}

        for new_item in cart_data.productsInCart:
            if new_item.productId in product_map:
                product_map[new_item.productId]["quantity"] = new_item.quantity  
            else:
                product_map[new_item.productId] = new_item.dict()

        await carts_collection.update_one(
            {"userId": cart_data.userId},
            {"$set": {"productsInCart": list(product_map.values())}}
        )
        message = "Cart updated successfully"
    else:
        await carts_collection.insert_one(cart_data.dict())
        message = "Cart created successfully"

    return success_response(cart_data.dict(), message)

# 📌 Empty Cart for a User
@router.delete("/cart/{userId}")
async def empty_cart(userId: str):
    result = await carts_collection.update_one(
        {"userId": userId},
        {"$set": {"productsInCart": []}}
    )

    if result.modified_count == 0:
        return error_response({}, "Cart cannot be emptied")


    return success_response({}, "Cart emptied successfully")

# 📌 Delete a specific product from the cart
@router.post("/cart/remove")
async def remove_cart_item(request: RemoveCartItemRequest):
    existing_cart = await carts_collection.find_one({"userId": request.userId})

    if not existing_cart:
        return error_response("Cart not found")

    updated_products = [
        item for item in existing_cart["productsInCart"] if item["productId"] != request.productId
    ]

    await carts_collection.update_one(
        {"userId": request.userId},
        {"$set": {"productsInCart": updated_products}}
    )

    return success_response({}, "Item removed from cart successfully")