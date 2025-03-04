import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("DATABASE_URL")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["ECommerceDB"]  # Change the database name as needed

# Collections
products_collection = db.get_collection("products")
users_collection = db.get_collection("users")
orders_collection = db.get_collection("orders")
carts_collection=db.get_collection("cart")
