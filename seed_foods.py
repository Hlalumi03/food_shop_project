"""Script to seed the database with sample food items and promotions."""
import sys
sys.path.insert(0, 'c:\\Users\\sabas\\Desktop\\FOOD')

from app.core.database import SessionLocal, create_tables
from app.models.food import Food
from app.models.promotion import Promotion
from datetime import datetime, timedelta

def seed_foods():
    """Seed the database with sample foods."""
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Clear existing foods
        db.query(Food).delete()
        db.commit()
        
        # Sample food items
        foods = [
            Food(
                name="Classic Hamburger",
                description="Juicy beef patty with lettuce, tomato, and cheese",
                price=8.99,
                category="Burgers",
                stock=50
            ),
            Food(
                name="Caesar Salad",
                description="Fresh romaine lettuce with parmesan and croutons",
                price=9.99,
                category="Salads",
                stock=40
            ),
            Food(
                name="Pepperoni Pizza",
                description="Classic pizza with mozzarella and pepperoni",
                price=12.99,
                category="Pizza",
                stock=30
            ),
            Food(
                name="Margherita Pizza",
                description="Fresh mozzarella, basil, and tomato sauce",
                price=11.99,
                category="Pizza",
                stock=25
            ),
            Food(
                name="Grilled Chicken Burger",
                description="Tender grilled chicken breast with avocado",
                price=10.99,
                category="Burgers",
                stock=45
            ),
            Food(
                name="Vegetarian Wrap",
                description="Hummus, veggies, and feta in a spinach wrap",
                price=8.99,
                category="Wraps",
                stock=35
            ),
            Food(
                name="Greek Salad",
                description="Tomatoes, cucumbers, olives, and feta cheese",
                price=9.99,
                category="Salads",
                stock=40
            ),
            Food(
                name="Crispy Chicken Wings",
                description="Six wings with your choice of sauce",
                price=7.99,
                category="Appetizers",
                stock=60
            ),
            Food(
                name="Garlic Bread",
                description="Toasted bread with butter and garlic",
                price=3.99,
                category="Sides",
                stock=80
            ),
            Food(
                name="French Fries",
                description="Crispy golden fries",
                price=3.49,
                category="Sides",
                stock=100
            ),
            Food(
                name="Chocolate Cake",
                description="Rich chocolate layer cake with frosting",
                price=4.99,
                category="Desserts",
                stock=20
            ),
            Food(
                name="Cheesecake",
                description="Classic New York style cheesecake",
                price=5.99,
                category="Desserts",
                stock=15
            ),
        ]
        
        db.add_all(foods)
        db.commit()
        
        print(f"✅ Successfully seeded {len(foods)} food items!")
        for food in foods:
            print(f"   - {food.name} (${food.price}) - Stock: {food.stock}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def seed_promotions():
    """Seed the database with sample promotions."""
    db = SessionLocal()
    
    try:
        # Clear existing promotions
        db.query(Promotion).delete()
        db.commit()
        
        # Sample promotions
        promotions = [
            Promotion(
                code="WELCOME10",
                title="Welcome Discount",
                description="10% off for new customers",
                discount_type="percentage",
                discount_value=10,
                min_order_amount=0,
                is_active=True,
                usage_limit=None,
                valid_until=datetime.utcnow() + timedelta(days=30)
            ),
            Promotion(
                code="PIZZA15",
                title="Pizza Special",
                description="15% off on pizza orders",
                discount_type="percentage",
                discount_value=15,
                min_order_amount=15,
                applicable_categories="Pizza",
                is_active=True,
                usage_limit=100,
                valid_until=datetime.utcnow() + timedelta(days=60)
            ),
            Promotion(
                code="SAVE5",
                title="Flat $5 Off",
                description="Save $5 on orders over $25",
                discount_type="fixed",
                discount_value=5,
                min_order_amount=25,
                is_active=True,
                usage_limit=None,
                valid_until=datetime.utcnow() + timedelta(days=45)
            ),
            Promotion(
                code="WEEKEND20",
                title="Weekend Special",
                description="20% off (max $10 discount)",
                discount_type="percentage",
                discount_value=20,
                min_order_amount=20,
                max_discount_amount=10,
                is_active=True,
                usage_limit=None,
                valid_until=datetime.utcnow() + timedelta(days=7)
            ),
            Promotion(
                code="BUNDLE25",
                title="Bundle Deal",
                description="25% off when ordering 3+ items",
                discount_type="percentage",
                discount_value=25,
                min_order_amount=30,
                is_active=True,
                usage_limit=None,
                valid_until=datetime.utcnow() + timedelta(days=90)
            ),
        ]
        
        db.add_all(promotions)
        db.commit()
        
        print(f"\n✅ Successfully seeded {len(promotions)} promotions!")
        for promo in promotions:
            print(f"   - {promo.code}: {promo.title} ({promo.discount_value}% off)" if promo.discount_type == "percentage" else f"   - {promo.code}: {promo.title} (${promo.discount_value} off)")
        
    except Exception as e:
        print(f"❌ Error seeding promotions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_foods()
    seed_promotions()
