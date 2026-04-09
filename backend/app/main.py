"""
FastAPI application entry point.

Creates the app, configures CORS for the frontend, registers all routers,
and ensures database tables exist on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routes import auth, products, credits, orders

# Create all database tables on startup (safe if tables already exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="A simplified e-commerce API with credits-based purchasing",
    version="1.0.0",
)

# Allow the React frontend (Vite dev server) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route groups — each handles a specific domain
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(credits.router)
app.include_router(orders.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "E-Commerce API is running"}
