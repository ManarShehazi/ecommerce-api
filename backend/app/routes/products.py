"""
Product routes — public catalog endpoint.

No authentication required. Any visitor can browse the product list.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import Product
from ..schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """Return all products in the catalog."""
    return db.query(Product).all()
