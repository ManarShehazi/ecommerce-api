# E-Commerce API

## Setup & Run
### Backend
cd backend && pip install -r requirements.txt
python seed.py   # loads products
uvicorn app.main:app --reload

### Frontend
cd frontend && npm install && npm run dev

## Architecture
[Brief description of the layered structure]

## Design Decisions
- Session tokens over JWT: simpler for this scope; JWT tradeoffs discussed below
- price_paid stored on orders: historical accuracy
- Pydantic schemas separate from ORM models: clean serialization boundary
- Single DB transaction for purchases: atomicity

## Improvements (prioritized)
1. JWT with refresh tokens + token expiry
2. Proper test suite (pytest for backend, React Testing Library)
3. PostgreSQL for production (SQLAlchemy makes this a one-line config change)
4. Rate limiting on auth endpoints
5. Admin panel for managing products
6. Pagination on order history
7. Real payment integration (Stripe)