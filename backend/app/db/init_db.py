"""
Database initialization and seeding script
Run this to create initial data and indexes
"""

import asyncio
from datetime import datetime, timedelta
import random
from loguru import logger

from app.core.database import connect_to_mongo, get_collection
from app.core.security import get_password_hash
from app.core.config import settings


async def create_indexes():
    """Create database indexes"""
    logger.info("📊 Creating database indexes...")
    
    # Users collection indexes
    users = get_collection("users")
    await users.create_index("email", unique=True, sparse=True)
    await users.create_index("phone", unique=True)
    await users.create_index("role")
    
    # Prices collection indexes
    prices = get_collection("prices")
    await prices.create_index([("commodity", 1), ("date", -1)])
    await prices.create_index("date")
    
    # Contracts collection indexes
    contracts = get_collection("contracts")
    await contracts.create_index("user_id")
    await contracts.create_index("status")
    await contracts.create_index("settlement_date")
    await contracts.create_index([("user_id", 1), ("status", 1)])
    
    logger.info("✅ Indexes created")


async def create_admin_user():
    """Create initial admin user"""
    logger.info("👤 Creating admin user...")
    
    users = get_collection("users")
    
    # Check if admin exists
    existing_admin = await users.find_one({"email": settings.ADMIN_EMAIL})
    if existing_admin:
        logger.info("⚠️  Admin user already exists")
        return
    
    admin_user = {
        "email": settings.ADMIN_EMAIL,
        "phone": settings.ADMIN_PHONE,
        "full_name": "AgriHedge Admin",
        "role": "admin",
        "preferred_language": "en",
        "hashed_password": get_password_hash(settings.ADMIN_PASSWORD),
        "is_active": True,
        "is_verified": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await users.insert_one(admin_user)
    logger.info("✅ Admin user created")
    logger.info(f"   Email: {settings.ADMIN_EMAIL}")
    logger.info(f"   Password: {settings.ADMIN_PASSWORD}")


async def seed_price_data():
    """Seed initial price data"""
    logger.info("💰 Seeding price data...")
    
    prices = get_collection("prices")
    
    # Check if data exists
    existing_count = await prices.count_documents({})
    if existing_count > 0:
        logger.info(f"⚠️  Price data already exists ({existing_count} records)")
        return
    
    commodities = ["soybean", "mustard", "groundnut", "sunflower"]
    base_prices = {
        "soybean": 4500,
        "mustard": 5200,
        "groundnut": 5800,
        "sunflower": 6000
    }
    
    # Generate 90 days of historical data
    today = datetime.utcnow().date()
    price_data = []
    
    for commodity in commodities:
        base_price = base_prices[commodity]
        
        for i in range(90, 0, -1):
            date = today - timedelta(days=i)
            
            # Add some random variation
            variation = random.uniform(-0.05, 0.05)
            price = base_price * (1 + variation)
            
            price_data.append({
                "date": date,
                "price": round(price, 2),
                "commodity": commodity,
                "market": "Sample Mandi",
                "market_type": "mandi",
                "volume": round(random.uniform(500, 2000), 2),
                "created_at": datetime.utcnow()
            })
    
    await prices.insert_many(price_data)
    logger.info(f"✅ Seeded {len(price_data)} price records")


async def seed_sample_users():
    """Create sample farmer and FPO users"""
    logger.info("👥 Creating sample users...")
    
    users = get_collection("users")
    
    sample_users = [
        {
            "email": "farmer1@example.com",
            "phone": "+919876543211",
            "full_name": "Ramesh Kumar",
            "role": "farmer",
            "preferred_language": "hi",
            "hashed_password": get_password_hash("demo123"),
            "farmer_profile": {
                "farm_size": 5.0,
                "crops": ["soybean"],
                "state": "Madhya Pradesh",
                "district": "Indore",
                "village": "Sample Village",
                "pincode": "452001",
                "fpo_member": False
            },
            "is_active": True,
            "is_verified": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "fpo1@example.com",
            "phone": "+919876543212",
            "full_name": "Green FPO Representative",
            "role": "fpo",
            "preferred_language": "en",
            "hashed_password": get_password_hash("demo123"),
            "fpo_profile": {
                "fpo_name": "Green Farmers Producer Organization",
                "registration_number": "FPO123456",
                "member_count": 150,
                "state": "Maharashtra",
                "district": "Pune",
                "primary_crops": ["soybean", "mustard"],
                "total_acreage": 750.0
            },
            "is_active": True,
            "is_verified": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for user in sample_users:
        existing = await users.find_one({"phone": user["phone"]})
        if not existing:
            await users.insert_one(user)
            logger.info(f"   Created user: {user['full_name']}")
    
    logger.info("✅ Sample users created")


async def main():
    """Main initialization function"""
    logger.info("🚀 Starting database initialization...")
    
    await connect_to_mongo()
    
    await create_indexes()
    await create_admin_user()
    await seed_price_data()
    await seed_sample_users()
    
    logger.info("✅ Database initialization complete!")
    logger.info("")
    logger.info("Sample Login Credentials:")
    logger.info("=" * 50)
    logger.info(f"Admin: {settings.ADMIN_EMAIL} / {settings.ADMIN_PASSWORD}")
    logger.info("Farmer: +919876543211 / demo123")
    logger.info("FPO: +919876543212 / demo123")
    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
