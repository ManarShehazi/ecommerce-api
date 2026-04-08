"""
Pydantic schemas — define the shape of API requests and responses.

These are NOT database models. They validate incoming data and control
what gets serialized back to the client. This keeps internal fields
(like password_hash) from leaking into API responses.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime


# ──────────────────────────────────────────────
# Auth schemas
# ──────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    """Returned after successful login or register."""
    token: str
    user: "UserResponse"


# ──────────────────────────────────────────────
# User schemas
# ──────────────────────────────────────────────

class UserResponse(BaseModel):
    """Public-facing user data — never includes password or token."""
    id: int
    username: str
    credits: float

    # Allow Pydantic to read data from SQLAlchemy model attributes
    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────
# Product schemas
# ──────────────────────────────────────────────

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────
# Order schemas
# ──────────────────────────────────────────────

class OrderResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price_paid: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PurchaseRequest(BaseModel):
    product_id: int


# ──────────────────────────────────────────────
# Credits schemas
# ──────────────────────────────────────────────

class CreditResponse(BaseModel):
    """Returned after adding credits — shows the new balance."""
    credits: float
