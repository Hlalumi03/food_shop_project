# Food Shop API

A professional FastAPI application for a food shop with clean architecture, SQLAlchemy ORM, SQLite database, and DTOs.

## Project Structure

```
FOOD/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── app/
    ├── __init__.py
    ├── core/              # Configuration and database setup
    │   ├── config.py      # Settings and configuration
    │   └── database.py    # SQLAlchemy setup and session management
    ├── models/            # SQLAlchemy ORM models
    │   ├── food.py        # Food model
    │   ├── order.py       # Order model
    │   └── payment.py     # Payment model
    ├── schemas/           # Pydantic DTOs (Data Transfer Objects)
    │   ├── food.py        # Food request/response schemas
    │   ├── order.py       # Order request/response schemas
    │   └── payment.py     # Payment request/response schemas
    ├── repositories/      # Data access layer
    │   ├── food_repository.py    # Food CRUD operations
    │   ├── order_repository.py   # Order CRUD operations
    │   └── payment_repository.py # Payment CRUD operations
    ├── services/          # Business logic layer
    │   ├── food_service.py       # Food business logic
    │   ├── order_service.py      # Order business logic
    │   └── payment_service.py    # Payment business logic
    └── routes/            # API endpoints (Route handlers)
        ├── food.py        # Food endpoints
        ├── order.py       # Order endpoints
        └── payment.py     # Payment endpoints
```

## Architecture Overview

### Clean Architecture Layers

1. **Routes Layer** (`app/routes/`)
   - HTTP request/response handling
   - Request validation using DTOs
   - Error handling

2. **Services Layer** (`app/services/`)
   - Business logic implementation
   - Validation and processing
   - Transaction management

3. **Repositories Layer** (`app/repositories/`)
   - Data access abstraction
   - Database query execution
   - CRUD operations

4. **Models Layer** (`app/models/`)
   - SQLAlchemy ORM models
   - Database schema definition

5. **Schemas Layer** (`app/schemas/`)
   - Pydantic DTOs
   - Request/response validation
   - Type hints

6. **Core Layer** (`app/core/`)
   - Database configuration
   - Application settings
   - Database session management

## Installation

1. Install Python 3.8+

2. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## API Endpoints

### Food Management

- `POST /api/v1/foods` - Create a new food item
- `GET /api/v1/foods` - Get all foods (with pagination and category filter)
- `GET /api/v1/foods/{food_id}` - Get a specific food item
- `PUT /api/v1/foods/{food_id}` - Update a food item
- `DELETE /api/v1/foods/{food_id}` - Delete a food item

### Order Management

- `POST /api/v1/orders` - Create a new order
- `GET /api/v1/orders` - Get all orders (with pagination and filters)
- `GET /api/v1/orders/{order_id}` - Get a specific order
- `PUT /api/v1/orders/{order_id}` - Update an order
- `PATCH /api/v1/orders/{order_id}/confirm` - Confirm an order
- `PATCH /api/v1/orders/{order_id}/deliver` - Mark as delivered
- `PATCH /api/v1/orders/{order_id}/pay` - Mark as paid
- `DELETE /api/v1/orders/{order_id}` - Delete an order

### Payment Management

- `POST /api/v1/payments` - Create a new payment
- `GET /api/v1/payments` - Get all payments (with pagination and filters)
- `GET /api/v1/payments/{payment_id}` - Get a specific payment
- `PUT /api/v1/payments/{payment_id}` - Update a payment
- `POST /api/v1/payments/{payment_id}/confirm` - Confirm/complete a payment
- `POST /api/v1/payments/{payment_id}/fail` - Mark payment as failed
- `POST /api/v1/payments/{payment_id}/refund` - Refund a completed payment
- `DELETE /api/v1/payments/{payment_id}` - Delete a payment
- `GET /api/v1/payments/statistics/overview` - Get payment statistics

## Payment Methods

The API supports the following payment methods:

- Credit Card
- Debit Card
- PayPal
- Apple Pay
- Google Pay
- Bank Transfer
- Cash

## Payment Status

Payment lifecycle:

- **Pending** - Payment created, awaiting confirmation
- **Processing** - Payment is being processed
- **Completed** - Payment successfully completed
- **Failed** - Payment transaction failed
- **Refunded** - Completed payment has been refunded

## Example Usage

### Create a Food Item

```bash
curl -X POST "http://localhost:8000/api/v1/foods" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita Pizza",
    "description": "Classic pizza with tomato, mozzarella, and basil",
    "price": 12.99,
    "category": "Pizza",
    "stock": 50
  }'
```

### Create an Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
      {
        "food_id": 1,
        "quantity": 2
      }
    ]
  }'
```

### Create a Payment

```bash
curl -X POST "http://localhost:8000/api/v1/payments" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "payment_method": "credit_card",
    "amount": 25.98,
    "card_last_four": "4242"
  }'
```

### Confirm a Payment

```bash
curl -X POST "http://localhost:8000/api/v1/payments/1/confirm" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_12345678"
  }'
```

### Get Payments by Status

```bash
curl "http://localhost:8000/api/v1/payments?status=completed"
```

### Get Payments by Method

```bash
curl "http://localhost:8000/api/v1/payments?method=credit_card"
```

### Refund a Payment

```bash
curl -X POST "http://localhost:8000/api/v1/payments/1/refund"
```

### Get Payment Statistics

```bash
curl "http://localhost:8000/api/v1/payments/statistics/overview"
```

## Database

The application uses SQLite database stored in `food_shop.db`. The database is automatically created on first run with the following tables:

- **foods** - Stores food items with price, category, and stock info
- **orders** - Stores customer orders with status and payment info
- **payments** - Stores payment transactions with method and status

## Key Features

1. **Clean Architecture** - Clear separation of concerns with distinct layers
2. **SQLAlchemy ORM** - Type-safe database operations
3. **Pydantic DTOs** - Request/response validation
4. **Repository Pattern** - Abstracted data access
5. **Service Pattern** - Centralized business logic
6. **Automatic Validation** - Built-in request validation
7. **Stock Management** - Automatic stock reduction on order creation
8. **Order Status Tracking** - Pending, confirmed, delivered states
9. **Payment System** - Multiple payment methods with status tracking
10. **Payment Refunds** - Support for refunding completed payments
11. **Payment Statistics** - Detailed payment analytics
12. **Error Handling** - Comprehensive error responses
13. **API Documentation** - Auto-generated interactive docs

## Configuration

Configuration is managed in `app/core/config.py`. You can override settings using environment variables:

```bash
export DATABASE_URL="sqlite:///./custom.db"
export ECHO_SQL="true"
```

Or create a `.env` file:

```
DATABASE_URL=sqlite:///./food_shop.db
ECHO_SQL=false
```
