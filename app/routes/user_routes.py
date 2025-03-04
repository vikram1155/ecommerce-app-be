from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.database import users_collection
from app.utils.response import success_response, error_response
from app.models.user_model import User, LoginRequest, UpdateFavoritesRequest
import logging
from passlib.context import CryptContext
from typing import List

logging.basicConfig(level=logging.ERROR)

# Logn/Signup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


# GET all users
@router.get("/users")
async def get_users():
    users = await users_collection.find({}, {"_id": 0}).to_list(100)
    return success_response(users, "Successfully fetched users")
 
# Login API
@router.post("/login")
async def login(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(request.password, user["password"]):
        print("Error here",request.password)
        raise HTTPException(status_code=401, detail="Invalid password")
    print("useruseruseruseruseruseruser",user)
    return success_response({"userDetails": {"userId":user["userId"], "name": user["name"], "email": user["email"], "admin": user["admin"], "phone":user["phone"], "age": user["age"], "favorites": user["favorites"]}}, "User Logged in")


# CREATE a new user
@router.post("/users")
async def create_user(user: User):
    user_mail_exists = await users_collection.find_one({"email": user.email})
    if user_mail_exists:
        raise HTTPException(status_code=400, detail="Email is already in use")
    
    user_phone_exists = await users_collection.find_one({"phone": user.phone})
    if user_phone_exists:
        raise HTTPException(status_code=400, detail="Phone number is already in use")
    
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user_dict["password"])  # Hash before saving

    result = await users_collection.insert_one(user_dict)

    # Convert ObjectId to string - to abvoid objectID array error
    user_dict["_id"] = str(result.inserted_id)
    
    return success_response(user_dict, "User created successfully", 201)

@router.post("/users/{user_id}/favorites")
async def update_favorites(user_id: str, request: UpdateFavoritesRequest):
    user = await users_collection.find_one({"userId": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's favorites list in the database
    await users_collection.update_one(
        {"userId": user_id}, {"$set": {"favorites": request.favorite_products}}
    )

    return success_response({"favorites": request.favorite_products}, "Favorites updated successfully")


@router.get("/users/{user_id}/favorites")
async def get_favorites(user_id: str):
    user = await users_collection.find_one({"userId": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's favorites list in the database
    await users_collection.find_one(
        {"userId": user_id}
    )

    return success_response({"favorites": user.get("favorites", [])}, "Favorites fetched successfully")

