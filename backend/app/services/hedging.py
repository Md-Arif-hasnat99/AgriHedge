"""
Virtual Hedging Simulator Service
Manages creation, tracking, and settlement of simulated hedging contracts
"""

from typing import List, Dict, Optional
from datetime import datetime, date
from bson import ObjectId
from loguru import logger

from app.core.database import get_collection
from app.models.contract import (
    Contract,
    ContractCreate,
    ContractStatus,
    ContractSummary,
    GainLossCalculation
)


class HedgingService:
    """Service for managing virtual hedging contracts"""
    
    def __init__(self):
        self.contracts_collection = get_collection("contracts")
        self.prices_collection = get_collection("prices")
    
    async def create_contract(
        self,
        user_id: str,
        contract_data: ContractCreate
    ) -> Contract:
        """
        Create a new virtual hedging contract
        
        Args:
            user_id: User ID creating the contract
            contract_data: Contract details
            
        Returns:
            Created contract
        """
        try:
            # Create contract document
            contract_dict = {
                "user_id": user_id,
                "commodity": contract_data.commodity,
                "contract_type": contract_data.contract_type,
                "quantity": contract_data.quantity,
                "locked_price": contract_data.locked_price,
                "settlement_date": contract_data.settlement_date,
                "status": ContractStatus.ACTIVE,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert into database
            result = await self.contracts_collection.insert_one(contract_dict)
            contract_dict["_id"] = str(result.inserted_id)
            
            logger.info(f"✅ Created contract {contract_dict['_id']} for user {user_id}")
            
            return Contract(**contract_dict)
            
        except Exception as e:
            logger.error(f"❌ Error creating contract: {str(e)}")
            raise
    
    async def get_user_contracts(
        self,
        user_id: str,
        status: Optional[ContractStatus] = None
    ) -> List[Contract]:
        """
        Get all contracts for a user
        
        Args:
            user_id: User ID
            status: Optional filter by status
            
        Returns:
            List of contracts
        """
        try:
            query = {"user_id": user_id}
            if status:
                query["status"] = status
            
            cursor = self.contracts_collection.find(query)
            contracts = []
            
            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                
                # Calculate current gain/loss
                gain_loss = await self.calculate_gain_loss(doc["_id"])
                if gain_loss:
                    doc["current_market_price"] = gain_loss.current_price
                    doc["potential_gain_loss"] = gain_loss.potential_gain_loss
                
                contracts.append(Contract(**doc))
            
            return contracts
            
        except Exception as e:
            logger.error(f"❌ Error fetching user contracts: {str(e)}")
            raise
    
    async def get_contract_by_id(self, contract_id: str) -> Optional[Contract]:
        """
        Get a specific contract by ID
        
        Args:
            contract_id: Contract ID
            
        Returns:
            Contract or None
        """
        try:
            doc = await self.contracts_collection.find_one(
                {"_id": ObjectId(contract_id)}
            )
            
            if doc:
                doc["_id"] = str(doc["_id"])
                
                # Calculate current gain/loss
                gain_loss = await self.calculate_gain_loss(contract_id)
                if gain_loss:
                    doc["current_market_price"] = gain_loss.current_price
                    doc["potential_gain_loss"] = gain_loss.potential_gain_loss
                
                return Contract(**doc)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error fetching contract: {str(e)}")
            raise
    
    async def calculate_gain_loss(
        self,
        contract_id: str
    ) -> Optional[GainLossCalculation]:
        """
        Calculate potential gain/loss for a contract
        
        Args:
            contract_id: Contract ID
            
        Returns:
            Gain/loss calculation
        """
        try:
            contract = await self.contracts_collection.find_one(
                {"_id": ObjectId(contract_id)}
            )
            
            if not contract:
                return None
            
            # Get current market price
            latest_price = await self.prices_collection.find_one(
                {"commodity": contract["commodity"]},
                sort=[("date", -1)]
            )
            
            if not latest_price:
                logger.warning(f"No price data found for {contract['commodity']}")
                return None
            
            current_price = latest_price["price"]
            locked_price = contract["locked_price"]
            quantity = contract["quantity"]
            
            # Calculate gain/loss
            price_difference = current_price - locked_price
            potential_gain_loss = price_difference * quantity
            percentage_change = (price_difference / locked_price) * 100
            
            return GainLossCalculation(
                contract_id=str(contract["_id"]),
                locked_price=locked_price,
                current_price=current_price,
                quantity=quantity,
                potential_gain_loss=potential_gain_loss,
                percentage_change=percentage_change,
                is_profitable=potential_gain_loss > 0
            )
            
        except Exception as e:
            logger.error(f"❌ Error calculating gain/loss: {str(e)}")
            raise
    
    async def settle_contract(
        self,
        contract_id: str,
        final_price: float
    ) -> Contract:
        """
        Settle a contract
        
        Args:
            contract_id: Contract ID
            final_price: Final market price at settlement
            
        Returns:
            Settled contract
        """
        try:
            contract = await self.contracts_collection.find_one(
                {"_id": ObjectId(contract_id)}
            )
            
            if not contract:
                raise ValueError("Contract not found")
            
            # Calculate final gain/loss
            actual_gain_loss = (final_price - contract["locked_price"]) * contract["quantity"]
            
            # Update contract
            await self.contracts_collection.update_one(
                {"_id": ObjectId(contract_id)},
                {
                    "$set": {
                        "status": ContractStatus.SETTLED,
                        "actual_gain_loss": actual_gain_loss,
                        "settled_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            logger.info(f"✅ Settled contract {contract_id}")
            
            return await self.get_contract_by_id(contract_id)
            
        except Exception as e:
            logger.error(f"❌ Error settling contract: {str(e)}")
            raise
    
    async def get_user_summary(self, user_id: str) -> ContractSummary:
        """
        Get summary of user's contracts
        
        Args:
            user_id: User ID
            
        Returns:
            Contract summary
        """
        try:
            all_contracts = await self.get_user_contracts(user_id)
            
            active_contracts = [c for c in all_contracts if c.status == ContractStatus.ACTIVE]
            settled_contracts = [c for c in all_contracts if c.status == ContractStatus.SETTLED]
            
            total_quantity = sum(c.quantity for c in all_contracts)
            total_locked_value = sum(c.locked_price * c.quantity for c in all_contracts)
            total_potential_gain_loss = sum(
                c.potential_gain_loss for c in active_contracts if c.potential_gain_loss
            )
            
            # Group by commodity
            contracts_by_commodity = {}
            for contract in all_contracts:
                commodity = contract.commodity
                if commodity not in contracts_by_commodity:
                    contracts_by_commodity[commodity] = 0
                contracts_by_commodity[commodity] += 1
            
            return ContractSummary(
                total_contracts=len(all_contracts),
                active_contracts=len(active_contracts),
                settled_contracts=len(settled_contracts),
                total_quantity=total_quantity,
                total_locked_value=total_locked_value,
                total_potential_gain_loss=total_potential_gain_loss,
                contracts_by_commodity=contracts_by_commodity
            )
            
        except Exception as e:
            logger.error(f"❌ Error generating user summary: {str(e)}")
            raise
    
    async def update_contract_blockchain_info(
        self,
        contract_id: str,
        tx_hash: str,
        block_number: int
    ) -> bool:
        """
        Update contract with blockchain transaction information
        
        Args:
            contract_id: Contract ID
            tx_hash: Transaction hash
            block_number: Block number
            
        Returns:
            Success status
        """
        try:
            result = await self.contracts_collection.update_one(
                {"_id": ObjectId(contract_id)},
                {
                    "$set": {
                        "blockchain_tx_hash": tx_hash,
                        "blockchain_block_number": block_number,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error updating blockchain info: {str(e)}")
            raise
