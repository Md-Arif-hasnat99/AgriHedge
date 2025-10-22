"""
Main API Router
Aggregates all API endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, prices, contracts, forecasts, blockchain, users, alerts


api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(prices.router, prefix="/prices", tags=["Prices"])
api_router.include_router(forecasts.router, prefix="/forecasts", tags=["Forecasting"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
api_router.include_router(blockchain.router, prefix="/blockchain", tags=["Blockchain"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
