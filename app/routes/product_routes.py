from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.database import products_collection
from app.utils.response import success_response, error_response
from app.models.product_model import Product, ProductUpdate
import logging

logging.basicConfig(level=logging.ERROR)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize router
router = APIRouter()

# GET all products
@router.get("/products")
async def get_products():
    products = await products_collection.find({}, {"_id": 0}).to_list(100)

    # Return an empty list if no products are found instead of an error
    return success_response(products, "Successfully fetched products")

# CREATE a new product
@router.post("/products")
async def create_product(product: Product):
    existing_product = await products_collection.find_one({"productId": product.productId})
    
    if existing_product:
        return error_response("Product ID already exists", 409)
    
    await products_collection.insert_one(product.dict())
    return success_response(product.dict(), "Product added successfully", 201)

# UPDATE an existing product
@router.put("/products/{productId}")
async def update_product(productId: str, updated_product: ProductUpdate):
    existing_product = await products_collection.find_one({"productId": productId})
    
    if not existing_product:
        return error_response("Product not found", 404)
    
    update_data = {k: v for k, v in updated_product.dict().items() if v is not None}
    
    if not update_data:
        return error_response("No valid fields provided for update", 400)
    
    await products_collection.update_one({"productId": productId}, {"$set": update_data})
    return success_response(update_data, "Product updated successfully")

# DELETE a product
@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    deleted_product = await products_collection.find_one_and_delete({"productId": product_id})
    
    if not deleted_product:
        return error_response("Product not found", 404)
    
    return success_response("Product deleted successfully")

# Include router
app.include_router(router, prefix="/api")
