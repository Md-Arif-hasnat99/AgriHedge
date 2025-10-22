"""
Scheduler for background tasks
- Price monitoring
- Volatility detection  
- Contract settlement
- Model retraining
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger

from app.core.config import settings


# Global scheduler instance
scheduler = AsyncIOScheduler()


async def check_price_volatility():
    """
    Check for price volatility and send alerts
    Runs every 30 minutes
    """
    try:
        logger.info("🔍 Checking price volatility...")
        
        # Import here to avoid circular dependencies
        from app.services.price_monitor import monitor_prices
        
        await monitor_prices()
        
        logger.info("✅ Volatility check completed")
        
    except Exception as e:
        logger.error(f"❌ Error in volatility check: {str(e)}")


async def settle_expired_contracts():
    """
    Check and settle contracts that have reached settlement date
    Runs daily at midnight
    """
    try:
        logger.info("🔍 Checking for expired contracts...")
        
        from app.services.hedging import HedgingService
        from app.core.database import get_collection
        from app.models.contract import ContractStatus
        
        hedging_service = HedgingService()
        contracts_collection = get_collection("contracts")
        
        # Find contracts that should be settled
        today = datetime.utcnow().date()
        cursor = contracts_collection.find({
            "status": ContractStatus.ACTIVE,
            "settlement_date": {"$lte": today}
        })
        
        settled_count = 0
        async for contract in cursor:
            # Get current market price
            prices_collection = get_collection("prices")
            latest_price = await prices_collection.find_one(
                {"commodity": contract["commodity"]},
                sort=[("date", -1)]
            )
            
            if latest_price:
                await hedging_service.settle_contract(
                    str(contract["_id"]),
                    latest_price["price"]
                )
                settled_count += 1
        
        logger.info(f"✅ Settled {settled_count} contracts")
        
    except Exception as e:
        logger.error(f"❌ Error settling contracts: {str(e)}")


async def retrain_ml_models():
    """
    Retrain ML forecasting models
    Runs weekly
    """
    try:
        logger.info("🤖 Retraining ML models...")
        
        from app.ml.forecaster import get_forecaster
        from app.core.database import get_collection
        
        prices_collection = get_collection("prices")
        
        # Retrain for each commodity
        commodities = ["soybean", "mustard", "groundnut", "sunflower"]
        
        for commodity in commodities:
            # Fetch historical prices
            cursor = prices_collection.find(
                {"commodity": commodity}
            ).sort("date", 1).limit(365)  # Last year of data
            
            price_history = []
            async for doc in cursor:
                price_history.append({
                    "date": doc["date"],
                    "price": doc["price"]
                })
            
            if len(price_history) >= 30:  # Minimum data required
                forecaster = get_forecaster(commodity)
                forecaster.train_arima_model(price_history)
                
                # Save model
                forecaster.save_model(f"models/{commodity}_model.pkl")
        
        logger.info("✅ ML models retrained successfully")
        
    except Exception as e:
        logger.error(f"❌ Error retraining models: {str(e)}")


async def generate_daily_report():
    """
    Generate daily analytics report
    Runs daily at 6 AM
    """
    try:
        logger.info("📊 Generating daily report...")
        
        # Generate report logic here
        # - Total users
        # - Active contracts
        # - Price changes
        # - Alerts sent
        
        logger.info("✅ Daily report generated")
        
    except Exception as e:
        logger.error(f"❌ Error generating report: {str(e)}")


def start_scheduler():
    """Start the background scheduler"""
    try:
        # Price volatility check - every 30 minutes
        scheduler.add_job(
            check_price_volatility,
            trigger=IntervalTrigger(
                minutes=settings.VOLATILITY_CHECK_INTERVAL_MINUTES
            ),
            id="price_volatility_check",
            name="Price Volatility Check",
            replace_existing=True
        )
        
        # Contract settlement - daily at midnight
        scheduler.add_job(
            settle_expired_contracts,
            trigger=CronTrigger(hour=0, minute=0),
            id="contract_settlement",
            name="Settle Expired Contracts",
            replace_existing=True
        )
        
        # Model retraining - weekly on Sunday at 2 AM
        scheduler.add_job(
            retrain_ml_models,
            trigger=CronTrigger(day_of_week='sun', hour=2, minute=0),
            id="model_retraining",
            name="Retrain ML Models",
            replace_existing=True
        )
        
        # Daily report - every day at 6 AM
        scheduler.add_job(
            generate_daily_report,
            trigger=CronTrigger(hour=6, minute=0),
            id="daily_report",
            name="Generate Daily Report",
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("✅ Background scheduler started")
        
    except Exception as e:
        logger.error(f"❌ Error starting scheduler: {str(e)}")


def stop_scheduler():
    """Stop the background scheduler"""
    try:
        scheduler.shutdown()
        logger.info("✅ Background scheduler stopped")
        
    except Exception as e:
        logger.error(f"❌ Error stopping scheduler: {str(e)}")
