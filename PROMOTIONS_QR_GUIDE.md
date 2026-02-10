# 🎉 Promotions & QR Codes - Complete Feature Guide

## Overview

Your Food Shop now includes two powerful features:
- 🎟️ **Promotional Codes & Discounts** - Apply coupon codes for special offers
- 📱 **QR Codes** - Scan to order food items directly

---

## 🎟️ Promotions System

### What Are Promotions?

Promotions are discount codes that customers can apply to their orders to save money. Each promotion has:
- **Unique Code** - The coupon code (e.g., `WELCOME10`)
- **Discount Type** - Percentage (%) or fixed dollar amount ($)
- **Minimum Order** - Minimum order amount required to use
- **Usage Limits** - How many times the code can be used
- **Expiration Date** - When the promotion expires

### Sample Promotions

| Code | Offer | Min Order | Limit | Expires |
|------|-------|-----------|-------|---------|
| **WELCOME10** | 10% off | $0 | Unlimited | 30 days |
| **PIZZA15** | 15% off pizza | $15 | 100 uses | 60 days |
| **SAVE5** | $5 off | $25 | Unlimited | 45 days |
| **WEEKEND20** | 20% off (max $10) | $20 | Unlimited | 7 days |
| **BUNDLE25** | 25% off 3+ items | $30 | Unlimited | 90 days |

### How to Use Promotions in Frontend

#### Method 1: Click on Active Promotions
1. Browse the menu and add items to cart
2. Look at the right sidebar "🎉 Active Promotions" section
3. Click on any promotion code you want to apply
4. Code is automatically entered and applied
5. See the discount in the cart total

#### Method 2: Manual Code Entry
1. Enter your promo code in the "Promo Code" input field
2. Click the "Apply" button
3. If valid, you'll see:
   - ✓ Success message
   - Discount amount displayed
   - Updated total

#### What Happens When You Apply a Code
```
Enter Code: WELCOME10
↓
Order Total: $50.00
Discount: -$5.00 (10% off)
↓
Final Total: $45.00
```

### Promotion Validation Rules

A promotion is **valid** only if ALL of these are true:
- ✅ Code exists in database
- ✅ Promotion is marked as "active"
- ✅ Current time is within valid dates
- ✅ Order total meets minimum amount
- ✅ Haven't exceeded usage limit
- ✅ No other expired codes

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Code not found" | Typo in code | Check spelling |
| "Promotion is inactive" | Code disabled | Wait for reactivation |
| "Not yet valid" | Before start date | Code not active yet |
| "Has expired" | After expiration | Used too late |
| "Reached usage limit" | Used too many times | Code sold out |
| "Minimum order required" | Order too small | Add more items |

### Using Promotions in Checkout

1. **Add items to cart** with intended quantity
2. **Apply promotion code** before checkout
3. **See updated total** with discount applied
4. **Fill in customer details** (name, email)
5. **Choose payment method** (card, PayPal, etc.)
6. **Click "Place Order"** - discount is applied to payment

After successful order:
- ✓ You'll see order confirmation
- ✓ Shows applied promo code
- ✓ Displays final total with discount
- ✓ Payment reflects the discounted amount

### Managing Promotions (Admin)

#### Create New Promotion
```bash
POST /api/v1/promotions
{
  "code": "NEWCODE",
  "title": "New Offer",
  "discount_type": "percentage",  # or "fixed"
  "discount_value": 15,            # 15% or $15
  "min_order_amount": 20,
  "usage_limit": 100,
  "valid_until": "2026-03-31T23:59:59"
}
```

#### Get Active Promotions
```bash
GET /api/v1/promotions/active/all
```
Returns all currently valid, active promotions

#### Apply Promotion to Order
```bash
POST /api/v1/promotions/apply
{
  "code": "WELCOME10",
  "order_total": 50.00
}
```

#### Update Promotion
```bash
PUT /api/v1/promotions/{id}
{
  "is_active": false,  # Disable code
  "discount_value": 20  # Change discount
}
```

#### Delete Promotion
```bash
DELETE /api/v1/promotions/{id}
```

---

## 📱 QR Code Features

### What Are QR Codes?

QR codes (Quick Response codes) are:
- 2D barcodes that encode information
- Scannable with any smartphone camera
- Links to your food shop ordering system
- Great for:
  - In-store displays
  - Menu cards
  - Social media promotion
  - Restaurant tables
  - Delivery packages

### QR Code Implementation

#### 1. Food Item QR Codes
**What it does:** Each food item has a unique QR code that customers can scan to:
- View food details
- Image showing ordered from specific food ID
- Useful for in-restaurant signage

**How to access:**
```
GET /api/v1/qr/foods/{food_id}/qr
```
Returns PNG image of the QR code

**Usage in Frontend:**
- Click the 📱 button on any food card
- Modal opens showing the QR code
- Share or print the code

#### 2. In Frontend
In the web interface:
1. **On each food card** there's a 📱 **QR Code button** (top right)
2. **Click the button** → Modal displays QR code
3. **Can be:**
   - Printed for physical signage
   - Screenshot for social media
   - Shared with customers

### QR Code Data Structure

Each food QR code encodes:
```
{
  "food_id": 1,
  "name": "Classic Hamburger",
  "price": 8.99,
  "timestamp": "2026-02-10T12:00:00Z"
}
```

### Using QR Codes in Your Business

#### In-Restaurant
- Print QR codes for each menu item
- Place on table menu cards
- Customers scan → View item → Add to order
- Speeds up ordering process

#### On Delivery Packages
- Include QR code on receipt
- Customers can re-order the same items
- Links directly to their previous order

#### Social Media
- Screenshot QR code on Instagram
- "Scan to order" posts on Facebook
- Twitter promotions

#### Marketing Materials
- Menu boards with QR codes
- Business cards with special items
- Loyalty program QR codes (future)

---

## 💾 Database Schema

### Promotions Table

```sql
CREATE TABLE promotions (
  id INTEGER PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  discount_type VARCHAR(20),  -- "percentage" or "fixed"
  discount_value FLOAT NOT NULL,
  min_order_amount FLOAT DEFAULT 0,
  max_discount_amount FLOAT,  -- Cap on percentage discounts
  applicable_categories VARCHAR(500),  -- Pizza, Burgers, etc
  is_active BOOLEAN DEFAULT TRUE,
  usage_limit INTEGER,  -- Max times usable
  usage_count INTEGER DEFAULT 0,  -- Current uses
  valid_from DATETIME,
  valid_until DATETIME,  -- Expiration
  created_at DATETIME,
  updated_at DATETIME
)
```

### Example Records

```
id=1, code='WELCOME10', discount_type='percentage', discount_value=10
id=2, code='SAVE5', discount_type='fixed', discount_value=5
id=3, code='PIZZA15', applicable_categories='Pizza', usage_limit=100
```

---

## API Endpoints Reference

### Promotions Endpoints

```
GET    /api/v1/promotions/active/all
       Get all currently valid promotions
       Returns: List[PromotionResponse]

GET    /api/v1/promotions
       Get all promotions with filters
       Params: skip, limit, active_only
       Returns: List[PromotionResponse]

GET    /api/v1/promotions/{id}
       Get specific promotion
       Returns: PromotionResponse

POST   /api/v1/promotions
       Create new promotion
       Body: PromotionCreate
       Returns: PromotionResponse (201)

PUT    /api/v1/promotions/{id}
       Update promotion
       Body: PromotionUpdate
       Returns: PromotionResponse

DELETE /api/v1/promotions/{id}
       Delete promotion
       Returns: 204 No Content

POST   /api/v1/promotions/apply
       Apply code to order
       Body: { "code": "WELCOME10", "order_total": 50.00 }
       Returns: PromotionResult with discount info
```

### QR Code Endpoints

```
GET    /api/v1/qr/foods/{food_id}/qr
       Get QR code image (PNG)
       Returns: PNG image bytes

GET    /api/v1/qr/foods/{food_id}/qr/page
       Get HTML page with QR code
       Returns: HTML page
```

---

## 🎯 Real-World Examples

### Example 1: Restaurant Uses Promotions

**Scenario:** Italian restaurant offers "PIZZA15" promotion

```
Customer visits website
↓
Sees: "PIZZA15 - 15% off pizza orders"
↓
Adds pizza items to cart
Cart total: $40.00
↓
Applies "PIZZA15" code
Discount: -$6.00
New total: $34.00
↓
Places order → Saves $6!
```

### Example 2: QR Code on Menu

```
Physical menu card:
┌─────────────────────┐
│  Classic Hamburger  │
│       $8.99         │
│  [QR CODE IMAGE]    │  ← Scan me!
└─────────────────────┘
                    ↓
          Customer scans with phone
                    ↓
          Sees item details
                    ↓
          Adds to online order
                    ↓
          Gets 10% off with WELCOME10
```

### Example 3: Loyalty Promotion

```
Regular customer:
- Gets "REGULAR20" code for 20% off
- Can use unlimited times
- Valid for 1 year
- Minimum $15 order
- Keeps coming back!
```

---

## 🛠️ Customization

### Add Your Own Promotion

Using Postman or API client:

```bash
POST http://localhost:8001/api/v1/promotions
Content-Type: application/json

{
  "code": "SPRING2026",
  "title": "Spring Special - 25% Off",
  "description": "Celebrate spring with our special offer!",
  "discount_type": "percentage",
  "discount_value": 25,
  "min_order_amount": 30,
  "max_discount_amount": 15,
  "is_active": true,
  "usage_limit": 500,
  "valid_until": "2026-06-30T23:59:59"
}
```

### Disable Expired Promotion

```bash
PUT http://localhost:8001/api/v1/promotions/1
Content-Type: application/json

{
  "is_active": false
}
```

### Change Discount Amount

```bash
PUT http://localhost:8001/api/v1/promotions/1
Content-Type: application/json

{
  "discount_value": 20
}
```

---

## 📊 Analytics & Reports

### Track Promotion Usage

```bash
GET http://localhost:8001/api/v1/promotions
```

Returns all promotions with `usage_count`:

```json
[
  {
    "code": "WELCOME10",
    "usage_limit": null,
    "usage_count": 47,  ← Used 47 times
    "is_active": true
  }
]
```

### Monitor by Expiration

- Promotions expire automatically
- 24-hour pre-expiry notification system (future)
- Archive old promotions (keep for records)

---

## 🔐 Best Practices

### For Business Owners

✅ **Do:**
- Set reasonable discount amounts (5-25%)
- Use percentage discounts for big-spender appeal
- Use fixed discounts for small-ticket items
- Monitor usage counts
- Refresh old codes regularly
- Target specific categories
- Time promotions strategically

❌ **Don't:**
- Create unlimited discounts for all items
- Keep expired codes active
- Forget to update `valid_until` dates
- Accumulate too many active codes
- Discount items that are already popular

### For Developers

✅ **Do:**
- Cache active promotions (reload hourly)
- Validate codes before checkout
- Log promotion usage
- Monitor database for orphaned codes
- Use UTC for all times

❌ **Don't:**
- Apply promotions multiple times
- Skip expiration date checks
- Allow negative final totals
- Hard-code promotion codes

---

## 🐛 Troubleshooting

### Promotion Not Appearing
1. Check if `is_active = true`
2. Check if `valid_from <= now <= valid_until`
3. Verify no usage limit reached
4. Check API: `GET /api/v1/promotions/active/all`

### QR Code Not Scanning

Check:
1. Image quality (minimum 150x150 pixels)
2. Camera is in focus
3. Adequate lighting
4. Not zoomed in too much
5. Try rotating phone

### Discount Not Applied

Verify:
1. Code spelling is correct
2. Code is active
3. Order meets minimum amount
4. No typos in code
5. Code hasn't expired
6. Usage limit not reached

---

## 📈 Future Enhancements

Planned features:
- 🎯 Usage analytics dashboard
- 📅 Scheduled promotions
- 👥 User-specific codes
- 🔄 Automatic re-application of past promotions
- 📧 Email promotion notifications
- 🎁 Referral code system
- ⏰ Time-limited flash sales
- 🌍 Regional promotions

---

## 📚 Integration with Orders

### Order-Promotion Link

When order is placed with promotion:

```
Order Created:
├── items: [food_id, quantity...]
├── customer: name, email
├── promotion_id: 1 (WELCOME10)
├── subtotal: $50.00
├── discount: -$5.00
└── total: $45.00
```

The discount is automatically:
- Calculated based on promotion rules
- Applied to order total
- Reflected in payment amount
- Stored in order history

---

## 🎓 Learning Resources

### API Documentation
While the system is running:
- Visit: `http://localhost:8001/docs`
- Interactive Swagger UI
- Try out endpoints live

### Database Inspection
```bash
sqlite3 food_shop.db
SELECT * FROM promotions;
SELECT * FROM orders;
```

---

## ✨ Summary

Your Food Shop now has:
- 🎟️ **5 sample promotions** ready to use
- 📱 **QR codes** for each food item
- 🎯 **Full promotion management** via API
- 💳 **Automatic discount application** at checkout
- 📊 **Usage tracking** for each promotion

Everything is integrated and ready to boost your sales! 🚀

---

**Questions?** Check the API docs at `http://localhost:8001/docs` while the server is running!
