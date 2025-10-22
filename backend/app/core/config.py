"""
Configuration settings for AgriHedge application
Loads environment variables and provides application settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "AgriHedge"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database
    MONGODB_URI: str = "mongodb://localhost:27017/agrihedge"
    DATABASE_NAME: str = "agrihedge"
    
    # Firebase (alternative)
    USE_FIREBASE: bool = False
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8081",
        "http://localhost:19006"
    ]
    
    # Blockchain
    BLOCKCHAIN_PROVIDER: str = "ganache"
    BLOCKCHAIN_RPC_URL: str = "http://localhost:8545"
    CONTRACT_ADDRESS: Optional[str] = None
    PRIVATE_KEY: Optional[str] = None
    GAS_LIMIT: int = 3000000
    
    # Polygon
    POLYGON_RPC_URL: str = "https://rpc-mumbai.maticvigil.com"
    POLYGON_CHAIN_ID: int = 80001
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Firebase Cloud Messaging
    FCM_SERVER_KEY: Optional[str] = None
    
    # External APIs
    AGMARKNET_API_URL: str = "https://api.data.gov.in/resource/"
    AGMARKNET_API_KEY: Optional[str] = None
    NCDEX_API_URL: str = "https://www.ncdex.com/"
    NCDEX_API_KEY: Optional[str] = None
    
    # Price Alerts
    PRICE_ALERT_THRESHOLD_PERCENTAGE: float = 5.0
    VOLATILITY_CHECK_INTERVAL_MINUTES: int = 30
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # ML Model
    MODEL_RETRAIN_INTERVAL_DAYS: int = 7
    FORECAST_HORIZON_DAYS: int = 30
    CONFIDENCE_LEVEL: float = 0.95
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/agrihedge.log"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    
    # SMS
    SMS_ENABLED: bool = True
    PRICE_CHANGE_SMS_THRESHOLD: float = 5.0
    
    # Chatbot
    CHATBOT_MODEL: str = "gpt-3.5-turbo"
    OPENAI_API_KEY: Optional[str] = None
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = [
        "en", "hi", "mr", "gu", "pa", "ta", "te", "kn", "ml", "bn"
    ]
    
    # Admin
    ADMIN_EMAIL: str = "admin@agrihedge.com"
    ADMIN_PASSWORD: str = "change-this-password"
    ADMIN_PHONE: str = "+919876543210"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to ensure settings are loaded only once
    """
    return Settings()


# Global settings instance
settings = get_settings()
