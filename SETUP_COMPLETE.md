# 🚀 FOOD SHOP - Complete Setup & Launch Guide

## Overview

Your Food Shop application now has a **complete multi-service launcher** that starts everything with a single command:

- ✅ **Frontend** on port 3000
- ✅ **API** on port 8001  
- ✅ **Database** (SQLite)

All running independently but communicating seamlessly!

---

## 🎯 Quick Start (Choose Your OS)

### **Windows PowerShell** (Recommended)
```powershell
.\start.ps1
```

### **Windows Command Prompt**
```cmd
start.bat
```

### **Linux / macOS**
```bash
chmod +x start.sh
./start.sh
```

---

## 📊 Service Architecture

```
┌─────────────────────────────────────────────────┐
│          USER'S BROWSER                         │
│     http://localhost:3000/index.html            │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│      FRONTEND SERVER (Port 3000)                │
│   Static HTTP Server (Python's http.server)     │
│                                                  │
│  - Serves index.html                            │
│  - Serves CSS & JavaScript                      │
│  - Handles user interactions                    │
└─────────────────────────────────────────────────┘
                     ↓
         HTTP Requests/Responses
                     ↓
┌─────────────────────────────────────────────────┐
│       API SERVER (Port 8001)                    │
│   FastAPI with Auto-Reload                      │
│                                                  │
│  - GET /api/v1/foods - List menu items          │
│  - POST /api/v1/orders - Create orders          │
│  - POST /api/v1/payments - Process payments     │
└─────────────────────────────────────────────────┘
                     ↓
         SQL Queries/Results
                     ↓
┌─────────────────────────────────────────────────┐
│        SQLITE DATABASE (food_shop.db)           │
│                                                  │
│  - foods table (12 items pre-loaded)            │
│  - orders table                                 │
│  - payments table                               │
└─────────────────────────────────────────────────┘
```

---

## 📋 File Structure

```
FOOD/
├── run.py                      ← Main launcher script
├── start.ps1                   ← Windows PowerShell launcher
├── start.bat                   ← Windows Batch launcher
├── start.sh                    ← Linux/Mac launcher
├── index.html                  ← Frontend (HTML/CSS/JS)
├── main.py                     ← FastAPI application
├── seed_foods.py               ← Database seeder
├── food_shop.db                ← SQLite database (auto-created)
│
├── LAUNCHER_GUIDE.md           ← Detailed launcher docs
├── FRONTEND_README.md          ← Frontend detailed guide
│
└── app/                        ← Application code
    ├── routes/                 ← API endpoints
    ├── models/                 ← Database models
    ├── schemas/                ← Request/response schemas
    ├── services/               ← Business logic
    ├── repositories/           ← Data access
    └── core/                   ← Config & database
```

---

## 🔄 How Everything Works Together

### User Places an Order:

1. **Frontend (Port 3000)**
   - User browses menu (loaded from API)
   - User selects items and adds to cart
   - User fills in order form

2. **Communication**
   ```
   Browser → POST http://localhost:8001/api/v1/orders
   ```

3. **API (Port 8001)**
   - Receives order request
   - Validates data
   - Queries database

4. **Database**
   - Stores order
   - Updates food stock
   - Records payment

5. **Response**
   ```
   Database → API → Browser → Success Modal
   ```

---

## 🎮 Using the Application

### Step 1: Start Everything
```powershell
.\start.ps1
```

Wait for this message:
```
✨ All Services Started Successfully!
```

### Step 2: Open Frontend
```
http://localhost:3000/index.html
```

### Step 3: Browse & Order
1. View all food items in a beautiful grid
2. Filter by category (Burgers, Pizza, Salads, etc.)
3. Add items to cart with quantity
4. Enter your name and email
5. Select payment method
6. Click "Place Order"
7. See confirmation with order ID

### Step 4: Stop Services
Press **`Ctrl+C`** in the terminal

---

## 🛠️ Port Configuration

### Default Ports
- **Frontend**: 3000
- **API**: 8001
- **Database**: sqlite (no port)

### Custom Ports

Edit `run.py`:

```python
FRONTEND_PORT = 3000  # Change to 3001, 3002, etc.
API_PORT = 8001       # Change to 8002, 8003, etc.
```

Update `index.html` API URL:

```javascript
const API_PORT = 8001;  // Change to your custom API port
```

---

## 📚 API Documentation

### While Services Are Running

Access interactive API docs:
```
http://localhost:8001/docs
```

Try requests directly from the browser!

### Food Endpoints
```
GET  /api/v1/foods              - Get all foods
GET  /api/v1/foods?category=Burgers
POST /api/v1/foods              - Create new food
PUT  /api/v1/foods/{id}         - Update food
DELETE /api/v1/foods/{id}       - Delete food
```

### Order Endpoints
```
POST /api/v1/orders             - Create order
GET  /api/v1/orders             - List all orders
GET  /api/v1/orders/{id}        - Get specific order
PATCH /api/v1/orders/{id}/confirm
PATCH /api/v1/orders/{id}/deliver
```

### Payment Endpoints
```
POST /api/v1/payments           - Create payment
POST /api/v1/payments/{id}/confirm - Confirm payment
GET  /api/v1/payments           - List payments
```

---

## 🐛 Troubleshooting

### Problem: Port Already in Use

**Windows:**
```powershell
# Kill process on port 8001
Get-Process | Where-Object {$_.Handles -like '*8001*'} | Stop-Process -Force

# Or change ports in run.py
```

**Linux/Mac:**
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9
```

### Problem: Virtual Environment Not Activating

**Windows PowerShell:**
```powershell
# Create fresh venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Then run
python run.py
```

### Problem: Database Issues

```bash
# Delete old database
rm food_shop.db  # or del food_shop.db on Windows

# Restart launcher - will auto-create and seed
```

### Problem: API Returns 404

Make sure:
1. API is running on port 8001
2. Frontend is configured with correct API_PORT in index.html
3. Check browser console for errors (F12)

### Problem: CORS Errors

Already handled! But if you see CORS errors:
1. API has CORS enabled for all origins
2. Check if API is actually running
3. Check if port numbers match

---

## 💾 Database Info

### Auto-Setup
- **Filename**: `food_shop.db`
- **Location**: Project root directory
- **Type**: SQLite3
- **Auto-created**: Yes
- **Auto-seeded**: Yes (12 food items)

### Reset Database
```bash
rm food_shop.db     # Remove database
python run.py       # Launcher will recreate and seed
```

### Sample Data (Pre-loaded)
| Food | Price | Stock | Category |
|------|-------|-------|----------|
| Classic Hamburger | $8.99 | 50 | Burgers |
| Pepperoni Pizza | $12.99 | 30 | Pizza |
| Caesar Salad | $9.99 | 40 | Salads |
| Crispy Chicken Wings | $7.99 | 60 | Appetizers |
| French Fries | $3.49 | 100 | Sides |
| Chocolate Cake | $4.99 | 20 | Desserts |
| *...and 6 more items* | | | |

---

## 🚀 Advanced Usage

### Run Services Separately (Development)

**Terminal 1 - API Server:**
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

**Terminal 2 - Frontend Server:**
```bash
python -m http.server 3000 --bind 127.0.0.1
```

### View Live Logs

The launcher shows real-time output from all services.

### Modify Frontend Code

Edit `index.html` → Save → Browser auto-refreshes (if livereload enabled)

### Add New Foods

Use the API endpoint:
```bash
curl -X POST http://localhost:8001/api/v1/foods \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita Pizza",
    "description": "Classic pizza",
    "price": 11.99,
    "category": "Pizza",
    "stock": 25
  }'
```

---

## 📱 Features Summary

| Feature | Frontend | API | Database |
|---------|----------|-----|----------|
| Browse Menu | ✅ | ✅ | ✅ |
| Add to Cart | ✅ | - | - |
| Create Order | ✅ | ✅ | ✅ |
| Process Payment | ✅ | ✅ | ✅ |
| View History | - | ✅ | ✅ |
| Update Stock | - | ✅ | ✅ |
| Filter Foods | ✅ | ✅ | ✅ |

---

## 🎨 Technology Stack

### Frontend
- HTML5
- CSS3 (Responsive)
- Vanilla JavaScript (No frameworks)
- Fetch API

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy ORM
- SQLite Database

### Infrastructure
- Uvicorn (ASGI Server)
- Python HTTP Server
- Cross-Origin Resource Sharing (CORS)

---

## 📞 Support

### Check Logs
The launcher displays real-time logs for all services. Look for errors there.

### Common Messages
```
✓ Database tables created     - Good!
✓ Database already has X foods - Good!
✓ API server starting         - Good!
✓ Frontend server starting    - Good!
⚠ Port X already in use       - May need to kill process
```

### Debug Mode
Edit `main.py` and change:
```python
app = FastAPI(debug=True)
```

---

## 🎯 Next Steps

1. **Run the launcher**: `.\start.ps1`
2. **Open browser**: `http://localhost:3000/index.html`
3. **Place an order**: Fill form → Click "Place Order"
4. **Check API docs**: `http://localhost:8001/docs`
5. **Explore the code**: Check `app/` folder

---

## ✨ You're All Set!

Everything is configured and ready to use. The launcher handles:
- ✅ Virtual environment activation
- ✅ Database initialization
- ✅ Data seeding
- ✅ Service startup
- ✅ Port management
- ✅ Graceful shutdown (Ctrl+C)

Just run `.\start.ps1` and start building! 🍔🚀

---

**Questions?** Check the detailed guides:
- [LAUNCHER_GUIDE.md](LAUNCHER_GUIDE.md) - Launcher details
- [FRONTEND_README.md](FRONTEND_README.md) - Frontend details
- API Docs: http://localhost:8001/docs (while running)
