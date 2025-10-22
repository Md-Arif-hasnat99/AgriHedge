"""
Database connection and management for MongoDB
"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from loguru import logger

from app.core.config import settings


class Database:
    """MongoDB database manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    
    
db = Database()


async def connect_to_mongo():
    """Connect to MongoDB database"""
    try:
        logger.info("🔌 Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(settings.MONGODB_URI)
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info("✅ Connected to MongoDB successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    try:
        logger.info("🔌 Closing MongoDB connection...")
        if db.client:
            db.client.close()
        logger.info("✅ MongoDB connection closed!")
        
    except Exception as e:
        logger.error(f"❌ Error closing MongoDB connection: {str(e)}")


def get_database():
    """Get database instance"""
    return db.client[settings.DATABASE_NAME]


def get_collection(collection_name: str):
    """Get collection from database"""
    database = get_database()
    return database[collection_name]
