"""
Mock Blockchain Service
Simulates blockchain functionality for contract transparency
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional
from loguru import logger
from web3 import Web3

from app.core.config import settings


class Block:
    """Blockchain block structure"""
    
    def __init__(
        self,
        index: int,
        timestamp: str,
        data: Dict,
        previous_hash: str
    ):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Mine block with proof of work"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class MockBlockchain:
    """
    Mock blockchain for transparent contract recording
    Simulates blockchain functionality without requiring actual blockchain
    """
    
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 2
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            data={"message": "AgriHedge Genesis Block"},
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        logger.info("🔗 Genesis block created")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_contract_block(self, contract_data: Dict) -> Block:
        """
        Add a new contract to the blockchain
        
        Args:
            contract_data: Contract information to record
            
        Returns:
            Created block
        """
        latest_block = self.get_latest_block()
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            data=contract_data,
            previous_hash=latest_block.hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        logger.info(f"🔗 Block {new_block.index} added to blockchain")
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Validate the blockchain integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """Get block by hash"""
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None
    
    def get_blocks_by_user(self, user_id: str) -> List[Block]:
        """Get all blocks for a specific user"""
        user_blocks = []
        for block in self.chain:
            if block.data.get("user_id") == user_id:
                user_blocks.append(block)
        return user_blocks
    
    def get_chain_info(self) -> Dict:
        """Get blockchain information"""
        return {
            "chain_length": len(self.chain),
            "difficulty": self.difficulty,
            "is_valid": self.is_chain_valid(),
            "latest_block": self.get_latest_block().to_dict()
        }
    
    def export_chain(self) -> List[Dict]:
        """Export entire blockchain"""
        return [block.to_dict() for block in self.chain]


class Web3BlockchainService:
    """
    Web3 Blockchain Service for Ganache/Polygon integration
    """
    
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.account = None
        self.initialize_connection()
    
    def initialize_connection(self):
        """Initialize connection to blockchain"""
        try:
            self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
            
            if self.w3.is_connected():
                logger.info(f"✅ Connected to blockchain at {settings.BLOCKCHAIN_RPC_URL}")
                
                # Load contract if address is provided
                if settings.CONTRACT_ADDRESS:
                    self.load_contract()
            else:
                logger.warning("⚠️ Failed to connect to blockchain")
                
        except Exception as e:
            logger.error(f"❌ Blockchain connection error: {str(e)}")
    
    def load_contract(self):
        """Load smart contract"""
        # Contract ABI would be loaded here
        # For MVP, we'll use the mock blockchain
        pass
    
    async def record_contract(self, contract_data: Dict) -> Dict:
        """
        Record contract on blockchain
        
        Args:
            contract_data: Contract information
            
        Returns:
            Transaction details
        """
        try:
            if self.w3 and self.w3.is_connected():
                # Send transaction to smart contract
                # For MVP, returning mock data
                tx_hash = self.w3.keccak(text=json.dumps(contract_data))
                
                return {
                    "tx_hash": tx_hash.hex(),
                    "block_number": self.w3.eth.block_number,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                logger.warning("⚠️ Blockchain not connected, using mock")
                return {
                    "tx_hash": hashlib.sha256(
                        json.dumps(contract_data).encode()
                    ).hexdigest(),
                    "block_number": 0,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Error recording contract: {str(e)}")
            raise


# Singleton instances
_mock_blockchain = None
_web3_service = None


def get_mock_blockchain() -> MockBlockchain:
    """Get mock blockchain instance"""
    global _mock_blockchain
    if _mock_blockchain is None:
        _mock_blockchain = MockBlockchain()
    return _mock_blockchain


def get_blockchain_service() -> Web3BlockchainService:
    """Get Web3 blockchain service"""
    global _web3_service
    if _web3_service is None:
        _web3_service = Web3BlockchainService()
    return _web3_service
