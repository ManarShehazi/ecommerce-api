"""
Auth routes — register and login.

Both endpoints return a session token + user info on success.
Passwords are hashed with bcrypt before storage (never stored in plain text).
"""

import secrets

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import User
from ..schemas import RegisterRequest, LoginRequest, AuthResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _generate_token() -> str:
    """Generate a cryptographically secure random session token."""
    return secrets.token_hex(32)


def _hash_password(password: str) -> str:
    """Hash a plain-text password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, password_hash: str) -> bool:
    """Check a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - Checks that the username isn't already taken
    - Hashes the password with bcrypt
    - Generates a session token so the user is logged in immediately
    """
    # Check for duplicate username
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    token = _generate_token()
    user = User(
        username=data.username,
        password_hash=_hash_password(data.password),
        credits=0.0,
        session_token=token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # Reload to get the auto-generated id

    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate an existing user.

    - Looks up the user by username
    - Verifies the password against the stored bcrypt hash
    - Generates a new session token (invalidates any previous token)
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not _verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Issue a fresh token on every login
    user.session_token = _generate_token()
    db.commit()
    db.refresh(user)

    return AuthResponse(
        token=user.session_token,
        user=UserResponse.model_validate(user),
    )
