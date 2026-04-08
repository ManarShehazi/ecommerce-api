"""
Seed script — populates the products table with sample catalog items.

Run once before starting the server:
    python seed.py

Safe to re-run: skips seeding if products already exist.
"""

from app.database import engine, SessionLocal, Base
from app.models import Product


# Sample product catalog from the challenge spec
PRODUCTS = [
    {
        "name": "Mechanical Keyboard",
        "description": "Cherry MX Brown switches, white backlight, TKL layout",
        "price": 15,
    },
    {
        "name": "Wireless Mouse",
        "description": "Ergonomic design, 4000 DPI, USB-C charging",
        "price": 8,
    },
    {
        "name": "USB-C Hub",
        "description": "7-in-1: HDMI, USB-A x3, SD card, ethernet, USB-C passthrough",
        "price": 6,
    },
    {
        "name": "Monitor Light Bar",
        "description": "Screen-mounted LED bar, adjustable color temperature",
        "price": 10,
    },
    {
        "name": "Cable Management Kit",
        "description": "Velcro ties, cable clips, and under-desk tray",
        "price": 3,
    },
]


def seed():
    # Create all tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Only seed if the products table is empty (safe to re-run)
        if db.query(Product).count() == 0:
            for item in PRODUCTS:
                db.add(Product(**item))
            db.commit()
            print(f"Seeded {len(PRODUCTS)} products.")
        else:
            print("Products already exist, skipping seed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
