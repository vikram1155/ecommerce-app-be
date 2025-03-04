from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.routes.user_routes import router as user_router
from app.routes.order_routes import router as order_router
from app.routes.cart_routes import router as cart_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    # allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["GET", "POST", "OPTIONS", "PUT"], 
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(product_router, prefix="/api", tags=["Products"])
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(order_router, prefix="/api", tags=["Orders"])
app.include_router(cart_router, prefix="/api", tags=["Cart"])

@app.get("/")
async def root():
    return {"message": "Welcome to Supplement Store API"}