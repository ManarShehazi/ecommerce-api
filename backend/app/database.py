"""
Database connection and session setup.

Uses SQLite for simplicity (single-file DB, no server needed).
SQLAlchemy handles the connection pooling and ORM layer.
Swapping to PostgreSQL later only requires changing the URL below.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database stored as a file in the backend directory
DATABASE_URL = "sqlite:///./ecommerce.db"

# Engine: manages the actual database connection
# check_same_thread=False is required for SQLite with FastAPI's async handling
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory: each call to SessionLocal() opens a new DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models — every model inherits from this
Base = declarative_base()
