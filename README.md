# E-Commerce API

A simplified e-commerce application with a FastAPI backend and React frontend. Users can register, browse products, add credits, purchase items, and view order history.

## Setup & Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python seed.py          # populates 5 products into the database
python -m uvicorn app.main:app --reload
```
The API runs at **http://localhost:8000**.  
Interactive API docs (Swagger UI) at **http://localhost:8000/docs**.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
The app runs at **http://localhost:5173**.

## Architecture

```
frontend/           React SPA (Vite)
  src/
    api.js          Centralized axios HTTP client with token interceptor
    App.jsx         Root component — auth state, routing between views
    components/
      AuthForm.jsx      Login / Register form
      ProductList.jsx   Product catalog + buy + add credits
      OrderHistory.jsx  Past purchases table

backend/            FastAPI (Python)
  app/
    main.py         App entry point, CORS, router registration
    database.py     SQLAlchemy engine + session factory (SQLite)
    models.py       ORM models: User, Product, Order
    schemas.py      Pydantic request/response validation
    dependencies.py Shared deps: DB session per request, auth guard
    routes/
      auth.py       POST /auth/register, POST /auth/login
      products.py   GET /products/
      credits.py    POST /credits/add, GET /credits/
      orders.py     POST /orders/, GET /orders/
  seed.py           Populates the product catalog
```

### API Endpoints

| Method | Path             | Auth? | Description              |
|--------|------------------|-------|--------------------------|
| POST   | /auth/register   | No    | Create a new account     |
| POST   | /auth/login      | No    | Login, get session token |
| GET    | /products/       | No    | List all products        |
| POST   | /credits/add     | Yes   | Add 5 credits to balance |
| GET    | /credits/        | Yes   | Get current balance      |
| POST   | /orders/         | Yes   | Purchase a product       |
| GET    | /orders/         | Yes   | View order history       |

## Design Decisions

- **Session tokens over JWT**: A random token stored on the user row is simpler for this scope. No signing keys, no expiry logic, no refresh flow. Trade-off: tokens don't expire and require a DB lookup on every request. For a production app, JWT with refresh tokens would be preferable.
- **`price_paid` stored on orders**: Captures the price at purchase time. If a product's price changes later, order history still shows what the user actually paid — a standard e-commerce pattern.
- **Pydantic schemas separate from ORM models**: Models describe the database; schemas describe the API contract. This prevents internal fields (e.g. `password_hash`) from leaking into responses.
- **Single DB transaction for purchases**: The credit debit and order creation happen in one `commit()`. If anything fails, both roll back — no risk of debiting credits without creating the order.
- **bcrypt for password hashing**: Passwords are never stored in plain text. bcrypt is intentionally slow, making brute-force attacks expensive.

## Improvements (prioritized)

1. **JWT with refresh tokens + token expiry** — session tokens never expire currently; JWT would add stateless auth with configurable TTL
2. **Proper test suite** — pytest for backend (unit + integration), React Testing Library for frontend
3. **PostgreSQL for production** — SQLAlchemy makes this a one-line config change (`DATABASE_URL`)
4. **Input validation hardening** — minimum password length, username format constraints
5. **Rate limiting on auth endpoints** — prevent brute-force login attempts
6. **Pagination on product list and order history** — needed once data grows
7. **Admin panel** — manage products, view all orders
8. **Real payment integration** (Stripe) — replace the "add 5 credits" button with actual payments
9. **Logout endpoint** — server-side token invalidation (currently only client-side)
10. **CSS framework or styled components** — current inline styles are minimal; a proper design system would improve UX