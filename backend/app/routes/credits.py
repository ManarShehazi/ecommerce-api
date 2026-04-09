"""
Credits routes — manage user credit balance.

Credits are the virtual currency used to purchase products.
In a real app this would integrate with a payment provider (e.g. Stripe).
For this project, a simple "add 5 credits" endpoint is sufficient.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from ..models import User
from ..schemas import CreditResponse

# Router setup
router = APIRouter(prefix="/credits", tags=["credits"])

# Fixed amount added per request (simulates a top-up)
CREDIT_TOP_UP_AMOUNT = 5.0


@router.post("/add", response_model=CreditResponse)
def add_credits(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add credits to the authenticated user's balance.

    Adds a fixed amount (5 credits) per request.
    Returns the updated balance.
    """
    user.credits += CREDIT_TOP_UP_AMOUNT
    db.commit()
    db.refresh(user)
    return CreditResponse(credits=user.credits)


@router.get("/", response_model=CreditResponse)
def get_balance(user: User = Depends(get_current_user)):
    """Return the authenticated user's current credit balance."""
    return CreditResponse(credits=user.credits)
