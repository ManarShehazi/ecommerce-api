"""
Order routes — purchase products and view order history.

The purchase endpoint is the most critical business logic:
it must debit credits and create an order atomically.
If anything fails, the transaction rolls back and no data is corrupted.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from ..models import User, Product, Order
from ..schemas import PurchaseRequest, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def purchase_product(
    data: PurchaseRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Purchase a product using credits.

    Flow:
    1. Look up the product (404 if not found)
    2. Check the user has enough credits (400 if insufficient)
    3. Debit the user's balance
    4. Create an order record with price_paid snapshot
    5. Commit everything in a single transaction

    If the commit fails, SQLAlchemy rolls back both the debit and the order.
    """
    # 1. Find the product
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # 2. Check sufficient credits
    if user.credits < product.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient credits. Need {product.price}, have {user.credits}",
        )

    # 3. Debit balance
    user.credits -= product.price

    # 4. Create order with price snapshot
    order = Order(
        user_id=user.id,
        product_id=product.id,
        price_paid=product.price,
    )
    db.add(order)

    # 5. Single commit — atomic: both debit and order succeed or both fail
    db.commit()
    db.refresh(order)

    return OrderResponse(
        id=order.id,
        product_id=order.product_id,
        product_name=product.name,
        price_paid=order.price_paid,
        created_at=order.created_at,
    )


@router.get("/", response_model=list[OrderResponse])
def get_order_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return the authenticated user's purchase history, newest first.

    Joins with the product table to include the product name in each order.
    """
    orders = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        OrderResponse(
            id=order.id,
            product_id=order.product_id,
            product_name=order.product.name,
            price_paid=order.price_paid,
            created_at=order.created_at,
        )
        for order in orders
    ]

