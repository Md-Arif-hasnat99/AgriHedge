"""
Pydantic models for price data and forecasting
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum


class CommodityType(str, Enum):
    """Supported commodity types"""
    SOYBEAN = "soybean"
    MUSTARD = "mustard"
    GROUNDNUT = "groundnut"
    SUNFLOWER = "sunflower"


class MarketType(str, Enum):
    """Market types"""
    MANDI = "mandi"
    NCDEX = "ncdex"
    FUTURES = "futures"


class PriceData(BaseModel):
    """Historical price data point"""
    date: date
    price: float = Field(..., gt=0, description="Price per quintal in INR")
    commodity: CommodityType
    market: Optional[str] = None
    market_type: MarketType = MarketType.MANDI
    volume: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-10-15",
                "price": 4500.0,
                "commodity": "soybean",
                "market": "Indore",
                "market_type": "mandi",
                "volume": 1000.0
            }
        }


class PriceForecast(BaseModel):
    """Price forecast for a single day"""
    date: date
    predicted_price: float
    lower_bound: float
    upper_bound: float
    confidence_level: float


class ForecastRequest(BaseModel):
    """Request for price forecast"""
    commodity: CommodityType
    forecast_days: int = Field(default=30, ge=1, le=90)
    confidence_level: float = Field(default=0.95, ge=0.8, le=0.99)


class ForecastResponse(BaseModel):
    """Price forecast response"""
    commodity: CommodityType
    forecast_horizon_days: int
    generated_at: datetime
    forecasts: List[PriceForecast]
    model_info: dict


class VolatilityAlert(BaseModel):
    """Price volatility alert"""
    commodity: CommodityType
    current_price: float
    current_volatility: float
    average_volatility: float
    trend: str
    trend_strength: float
    alert_level: str
    checked_at: datetime


class PriceAlert(BaseModel):
    """Price alert configuration"""
    user_id: str
    commodity: CommodityType
    target_price: float
    alert_type: str = Field(..., description="above or below")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PriceComparison(BaseModel):
    """Compare current price with historical data"""
    commodity: CommodityType
    current_price: float
    yesterday_price: float
    last_week_price: float
    last_month_price: float
    percent_change_daily: float
    percent_change_weekly: float
    percent_change_monthly: float
