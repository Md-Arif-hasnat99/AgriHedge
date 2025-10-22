"""
AI/ML Price Forecasting Module
Uses ARIMA and Linear Regression for oilseed price prediction
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
from loguru import logger

from app.core.config import settings


class PriceForecaster:
    """
    AI-powered price forecasting for oilseed commodities
    Implements ARIMA and Linear Regression models
    """
    
    def __init__(self, commodity: str):
        """
        Initialize forecaster for a specific commodity
        
        Args:
            commodity: Commodity name (e.g., 'soybean', 'mustard')
        """
        self.commodity = commodity
        self.model = None
        self.scaler = StandardScaler()
        self.last_trained = None
        
    def prepare_data(self, price_history: List[Dict]) -> pd.DataFrame:
        """
        Prepare historical price data for modeling
        
        Args:
            price_history: List of price records with date and price
            
        Returns:
            Prepared DataFrame with processed features
        """
        df = pd.DataFrame(price_history)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df.set_index('date', inplace=True)
        
        # Add time-based features
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        df['day_of_year'] = df.index.dayofyear
        
        # Add rolling statistics
        df['rolling_mean_7'] = df['price'].rolling(window=7).mean()
        df['rolling_std_7'] = df['price'].rolling(window=7).std()
        df['rolling_mean_30'] = df['price'].rolling(window=30).mean()
        
        # Forward fill missing values
        df = df.fillna(method='ffill')
        
        return df
    
    def train_arima_model(
        self,
        price_history: List[Dict],
        order: Tuple[int, int, int] = (5, 1, 0)
    ) -> Dict:
        """
        Train ARIMA model on historical price data
        
        Args:
            price_history: Historical price data
            order: ARIMA order (p, d, q)
            
        Returns:
            Training metrics and model info
        """
        try:
            df = self.prepare_data(price_history)
            
            # Train ARIMA model
            logger.info(f"Training ARIMA model for {self.commodity}...")
            model = ARIMA(df['price'], order=order)
            self.model = model.fit()
            self.last_trained = datetime.utcnow()
            
            # Calculate metrics
            predictions = self.model.predict(start=0, end=len(df)-1)
            mse = np.mean((df['price'] - predictions) ** 2)
            rmse = np.sqrt(mse)
            mape = np.mean(np.abs((df['price'] - predictions) / df['price'])) * 100
            
            logger.info(f"✅ ARIMA model trained - RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")
            
            return {
                "model_type": "ARIMA",
                "order": order,
                "rmse": float(rmse),
                "mape": float(mape),
                "trained_at": self.last_trained.isoformat(),
                "data_points": len(df)
            }
            
        except Exception as e:
            logger.error(f"❌ Error training ARIMA model: {str(e)}")
            raise
    
    def forecast(
        self,
        steps: int = 30,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Generate price forecast with confidence intervals
        
        Args:
            steps: Number of days to forecast
            confidence_level: Confidence level for intervals
            
        Returns:
            Forecast data with predictions and confidence intervals
        """
        try:
            if not self.model:
                raise ValueError("Model not trained. Please train the model first.")
            
            # Generate forecast
            logger.info(f"Generating {steps}-day forecast for {self.commodity}...")
            forecast_result = self.model.forecast(steps=steps)
            
            # Get confidence intervals
            forecast_df = self.model.get_forecast(steps=steps)
            confidence_intervals = forecast_df.conf_int(alpha=1-confidence_level)
            
            # Prepare response
            today = datetime.utcnow().date()
            forecasts = []
            
            for i in range(steps):
                forecast_date = today + timedelta(days=i+1)
                forecasts.append({
                    "date": forecast_date.isoformat(),
                    "predicted_price": float(forecast_result.iloc[i]),
                    "lower_bound": float(confidence_intervals.iloc[i, 0]),
                    "upper_bound": float(confidence_intervals.iloc[i, 1]),
                    "confidence_level": confidence_level
                })
            
            logger.info(f"✅ Forecast generated successfully")
            
            return {
                "commodity": self.commodity,
                "forecast_horizon_days": steps,
                "generated_at": datetime.utcnow().isoformat(),
                "forecasts": forecasts,
                "model_info": {
                    "type": "ARIMA",
                    "last_trained": self.last_trained.isoformat() if self.last_trained else None
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating forecast: {str(e)}")
            raise
    
    def detect_volatility(
        self,
        price_history: List[Dict],
        window: int = 7
    ) -> Dict:
        """
        Detect price volatility and trends
        
        Args:
            price_history: Historical price data
            window: Window size for volatility calculation
            
        Returns:
            Volatility metrics and alerts
        """
        try:
            df = self.prepare_data(price_history)
            
            # Calculate rolling volatility
            df['returns'] = df['price'].pct_change()
            df['volatility'] = df['returns'].rolling(window=window).std() * np.sqrt(252)
            
            current_volatility = df['volatility'].iloc[-1]
            avg_volatility = df['volatility'].mean()
            
            # Detect trend
            recent_prices = df['price'].tail(window).values
            trend_slope = np.polyfit(range(len(recent_prices)), recent_prices, 1)[0]
            
            # Determine alert level
            alert_level = "normal"
            if current_volatility > avg_volatility * 1.5:
                alert_level = "high"
            elif current_volatility > avg_volatility * 1.2:
                alert_level = "moderate"
            
            return {
                "commodity": self.commodity,
                "current_price": float(df['price'].iloc[-1]),
                "current_volatility": float(current_volatility),
                "average_volatility": float(avg_volatility),
                "trend": "upward" if trend_slope > 0 else "downward",
                "trend_strength": float(abs(trend_slope)),
                "alert_level": alert_level,
                "checked_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error detecting volatility: {str(e)}")
            raise
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if self.model:
            joblib.dump({
                'model': self.model,
                'commodity': self.commodity,
                'last_trained': self.last_trained
            }, filepath)
            logger.info(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.commodity = data['commodity']
        self.last_trained = data['last_trained']
        logger.info(f"✅ Model loaded from {filepath}")


# Singleton forecaster instances
_forecasters = {}


def get_forecaster(commodity: str) -> PriceForecaster:
    """
    Get or create a forecaster instance for a commodity
    
    Args:
        commodity: Commodity name
        
    Returns:
        PriceForecaster instance
    """
    if commodity not in _forecasters:
        _forecasters[commodity] = PriceForecaster(commodity)
    return _forecasters[commodity]
