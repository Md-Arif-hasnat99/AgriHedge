"""
Pydantic models for virtual hedging contracts
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum

from app.models.price import CommodityType


class ContractType(str, Enum):
    """Types of hedging contracts"""
    FORWARD = "forward"
    FUTURES = "futures"
    OPTIONS_CALL = "options_call"
    OPTIONS_PUT = "options_put"


class ContractStatus(str, Enum):
    """Contract status"""
    ACTIVE = "active"
    SETTLED = "settled"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ContractCreate(BaseModel):
    """Create new hedging contract"""
    commodity: CommodityType
    contract_type: ContractType
    quantity: float = Field(..., gt=0, description="Quantity in quintals")
    locked_price: float = Field(..., gt=0, description="Price locked per quintal")
    settlement_date: date
    
    class Config:
        json_schema_extra = {
            "example": {
                "commodity": "soybean",
                "contract_type": "forward",
                "quantity": 100,
                "locked_price": 4500.0,
                "settlement_date": "2025-01-15"
            }
        }


class Contract(BaseModel):
    """Virtual hedging contract"""
    id: str = Field(alias="_id")
    user_id: str
    commodity: CommodityType
    contract_type: ContractType
    quantity: float
    locked_price: float
    current_market_price: Optional[float] = None
    settlement_date: date
    status: ContractStatus = ContractStatus.ACTIVE
    
    # Financial calculations
    potential_gain_loss: Optional[float] = None
    actual_gain_loss: Optional[float] = None
    
    # Blockchain tracking
    blockchain_tx_hash: Optional[str] = None
    blockchain_block_number: Optional[int] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    settled_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "commodity": "soybean",
                "contract_type": "forward",
                "quantity": 100,
                "locked_price": 4500.0,
                "current_market_price": 4700.0,
                "settlement_date": "2025-01-15",
                "status": "active",
                "potential_gain_loss": 20000.0,
                "blockchain_tx_hash": "0xabc123..."
            }
        }


class ContractSettlement(BaseModel):
    """Settle a contract"""
    contract_id: str
    final_market_price: float
    settlement_notes: Optional[str] = None


class ContractSummary(BaseModel):
    """Summary of user's contracts"""
    total_contracts: int
    active_contracts: int
    settled_contracts: int
    total_quantity: float
    total_locked_value: float
    total_potential_gain_loss: float
    contracts_by_commodity: dict


class GainLossCalculation(BaseModel):
    """Calculate gain/loss for a contract"""
    contract_id: str
    locked_price: float
    current_price: float
    quantity: float
    potential_gain_loss: float
    percentage_change: float
    is_profitable: bool


class BlockchainRecord(BaseModel):
    """Blockchain transaction record"""
    contract_id: str
    transaction_hash: str
    block_number: int
    timestamp: datetime
    contract_data: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "contract_id": "507f1f77bcf86cd799439011",
                "transaction_hash": "0xabc123def456...",
                "block_number": 12345678,
                "timestamp": "2024-10-22T10:30:00",
                "contract_data": {
                    "commodity": "soybean",
                    "quantity": 100,
                    "locked_price": 4500.0
                }
            }
        }
