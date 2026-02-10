# Food Shop Frontend - Getting Started

## Overview
A fully functional web-based food ordering system that integrates with your FastAPI backend.

## Features

### 🍽️ Menu Management
- Browse all available food items with beautiful cards
- Filter menu items by category
- View food details: name, description, price, and stock
- See real-time availability of items

### 🛒 Shopping Cart
- Add items to cart with adjustable quantities
- Remove items from cart
- Real-time total price calculation
- Cart persists during your browsing session

### 📋 Order Management
- Enter customer name and email
- View detailed order summary
- Create orders with your cart items

### 💳 Payment Processing
- Multiple payment methods supported:
  - Credit Card
  - Debit Card
  - PayPal
  - Apple Pay
  - Google Pay
  - Bank Transfer
  - Cash
- Card last 4 digits validation
- Automatic transaction ID generation
- Payment confirmation with reference number

### ✅ Order Confirmation
- Success modal with order ID and total
- Order details summary
- Easy continuation to shop again

## How to Use

### 1. Start the API Server
```bash
cd c:\Users\sabas\Desktop\FOOD
source .venv/Scripts/activate  # or activate.bat on Windows
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

### 2. Seed Sample Data (if needed)
```bash
python seed_foods.py
```

### 3. Access the Frontend
Open your browser and navigate to:
```
http://localhost:8001/
```

## Using the Frontend

### Browse Menu
1. All food items are displayed in a grid layout
2. Each card shows:
   - Food name
   - Description
   - Price
   - Stock availability
   - Add to cart button

### Filter by Category
- Click category buttons at the top to filter items
- "All Categories" shows all items
- Categories are dynamically generated from database

### Add to Cart
1. Select the quantity using the input field
2. Click "Add" button
3. Item appears in the cart sidebar
4. Continue shopping or proceed to checkout

### Place an Order
1. Enter your name
2. Enter your email address
3. Choose a payment method
4. If paying by card, enter the last 4 digits
5. Click "Place Order"
6. See your order confirmation with:
   - Order ID
   - Total amount
   - Payment status

## API Endpoints Used

### Foods
- `GET /api/v1/foods` - Get all foods with optional category filter

### Orders
- `POST /api/v1/orders` - Create a new order

### Payments
- `POST /api/v1/payments` - Create a payment
- `POST /api/v1/payments/{id}/confirm` - Confirm payment

## Frontend Technology Stack
- **HTML5** - Structure
- **CSS3** - Modern responsive styling with gradients and animations
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - For API communication

## Design Features
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI/UX** - Purple gradient background with clean cards
- **Loading States** - Visual feedback during API calls
- **Error Handling** - User-friendly error messages
- **Form Validation** - Real-time input validation
- **Accessibility** - Semantic HTML and proper ARIA labels

## Database
- Automatically uses SQLite database from `./food_shop.db`
- Schema created on server startup
- 12 sample food items pre-populated

## Troubleshooting

### Port already in use
If port 8001 is already in use:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8002
```
Then update the API_BASE URL in index.html to port 8002.

### CORS Errors
The API is configured with CORS enabled for all origins, so cross-origin requests should work.

### Database Issues
To reset the database:
1. Delete `food_shop.db` file
2. Restart the server
3. Run `python seed_foods.py`

## Sample Foods Included
1. Classic Hamburger - $8.99
2. Caesar Salad - $9.99
3. Pepperoni Pizza - $12.99
4. Margherita Pizza - $11.99
5. Grilled Chicken Burger - $10.99
6. Vegetarian Wrap - $8.99
7. Greek Salad - $9.99
8. Crispy Chicken Wings - $7.99
9. Garlic Bread - $3.99
10. French Fries - $3.49
11. Chocolate Cake - $4.99
12. Cheesecake - $5.99

## Future Enhancements
- Order history tracking
- User accounts and authentication
- Admin panel for managing menu
- Real payment gateway integration
- Order tracking with status updates
- Search functionality
- Favorites/wishlist feature
- Coupon/discount codes

---

**Status**: ✅ Fully Functional and Ready to Use!
