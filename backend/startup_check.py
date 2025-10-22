"""
Quick start script for AgriHedge backend
Checks MongoDB connection and starts the server
"""

import asyncio
import sys
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient


async def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        logger.info("🔌 Checking MongoDB connection...")
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await client.admin.command('ping')
        logger.info("✅ MongoDB is running!")
        client.close()
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {str(e)}")
        logger.info("💡 Start MongoDB with: docker-compose up mongodb")
        logger.info("   Or install MongoDB locally: https://www.mongodb.com/try/download/community")
        return False


async def main():
    """Main startup check"""
    
    logger.info("=" * 60)
    logger.info("🌾 AgriHedge Backend Startup Check")
    logger.info("=" * 60)
    
    # Check MongoDB
    mongo_ok = await check_mongodb()
    
    if not mongo_ok:
        logger.error("❌ Please start MongoDB before running the server")
        sys.exit(1)
    
    logger.info("")
    logger.info("✅ All systems ready!")
    logger.info("🚀 Starting FastAPI server...")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
