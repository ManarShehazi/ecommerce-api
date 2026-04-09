"""
Shared dependencies injected into route handlers via FastAPI's Depends().

Two key dependencies:
- get_db: provides a database session per request, auto-closed afterward
- get_current_user: extracts the session token from the Authorization header,
  looks up the user, and returns the User object (or 401 if invalid)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

# Tells FastAPI to expect "Authorization: Bearer <token>" header
bearer_scheme = HTTPBearer()


def get_db():
    """
    Yield a database session for one request, then close it.

    FastAPI's dependency injection calls this as a generator:
    - before the route runs: opens a session
    - after the route returns (or raises): closes the session
    This guarantees we never leak open DB connections.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Auth dependency — look up the user by their session token.

    Any route that includes `user = Depends(get_current_user)` in its
    parameters will automatically require a valid token. If the token
    is missing or doesn't match any user, FastAPI returns 401.
    """
    token = credentials.credentials
    user = db.query(User).filter(User.session_token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token",
        )
    return user
