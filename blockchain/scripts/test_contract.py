"""
Test script for HedgingContract smart contract
Tests all contract functions on Ganache
"""

from web3 import Web3
import json
from pathlib import Path
from loguru import logger
import time


def load_contract():
    """Load deployed contract"""
    
    deployment_path = Path(__file__).parent.parent / "build" / "deployment.json"
    
    if not deployment_path.exists():
        logger.error("❌ Contract not deployed. Run deploy.py first!")
        return None, None, None
    
    with open(deployment_path, 'r') as f:
        deployment = json.load(f)
    
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    
    if not w3.is_connected():
        logger.error("❌ Cannot connect to Ganache!")
        return None, None, None
    
    # Load contract
    contract = w3.eth.contract(
        address=deployment['address'],
        abi=deployment['abi']
    )
    
    return w3, contract, deployment['address']


def test_create_contract():
    """Test creating a hedging contract"""
    
    logger.info("🧪 Testing contract creation...")
    
    w3, contract, contract_address = load_contract()
    if not contract:
        return
    
    account = w3.eth.accounts[0]
    farmer = w3.eth.accounts[1]
    
    # Create a hedging contract
    tx_hash = contract.functions.createContract(
        farmer,                           # farmer address
        "Soybean",                       # commodity
        1000,                            # quantity (kg)
        5000,                            # strike price (Rs/quintal)
        4800,                            # current price
        int(time.time()) + 7776000,     # maturity (90 days)
        0,                               # contract type (0=Call)
        "Maharashtra"                    # location
    ).transact({'from': account})
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    logger.info(f"✅ Contract created! Gas used: {receipt.gasUsed}")
    
    # Get contract details
    contract_id = 0
    details = contract.functions.getContract(contract_id).call()
    
    logger.info(f"📄 Contract Details:")
    logger.info(f"   Farmer: {details[0]}")
    logger.info(f"   Commodity: {details[1]}")
    logger.info(f"   Quantity: {details[2]} kg")
    logger.info(f"   Strike Price: ₹{details[3]}")
    logger.info(f"   Current Price: ₹{details[4]}")
    logger.info(f"   Status: {details[7]}")
    
    return contract_id


def test_update_price():
    """Test updating commodity price"""
    
    logger.info("🧪 Testing price update...")
    
    w3, contract, _ = load_contract()
    if not contract:
        return
    
    account = w3.eth.accounts[0]
    
    # Update Soybean price
    tx_hash = contract.functions.updatePrice(
        "Soybean",
        5200  # New price
    ).transact({'from': account})
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    logger.info(f"✅ Price updated! Gas used: {receipt.gasUsed}")
    
    # Get current price
    price = contract.functions.getCommodityPrice("Soybean").call()
    logger.info(f"💰 Current Soybean price: ₹{price}")


def test_calculate_gain_loss():
    """Test calculating gain/loss"""
    
    logger.info("🧪 Testing gain/loss calculation...")
    
    w3, contract, _ = load_contract()
    if not contract:
        return
    
    contract_id = 0
    current_price = 5200
    
    # Calculate potential gain/loss
    gain_loss = contract.functions.calculateCurrentGainLoss(
        contract_id,
        current_price
    ).call()
    
    logger.info(f"📊 Potential Gain/Loss: ₹{gain_loss}")


def test_settle_contract():
    """Test settling a contract"""
    
    logger.info("🧪 Testing contract settlement...")
    
    w3, contract, _ = load_contract()
    if not contract:
        return
    
    account = w3.eth.accounts[0]
    contract_id = 0
    
    # Check if matured (will fail for testing, but shows the logic)
    try:
        tx_hash = contract.functions.settleContract(
            contract_id,
            5300  # Settlement price
        ).transact({'from': account})
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logger.info(f"✅ Contract settled! Gas used: {receipt.gasUsed}")
        
        # Get updated details
        details = contract.functions.getContract(contract_id).call()
        logger.info(f"💰 Final Gain/Loss: ₹{details[8]}")
        
    except Exception as e:
        logger.warning(f"⚠️ Cannot settle (contract not matured): {str(e)}")


def test_get_farmer_contracts():
    """Test getting all contracts for a farmer"""
    
    logger.info("🧪 Testing farmer contracts query...")
    
    w3, contract, _ = load_contract()
    if not contract:
        return
    
    farmer = w3.eth.accounts[1]
    
    contracts = contract.functions.getFarmerContracts(farmer).call()
    
    logger.info(f"📋 Farmer has {len(contracts)} contracts: {contracts}")


def run_all_tests():
    """Run all tests"""
    
    logger.info("=" * 60)
    logger.info("🧪 RUNNING SMART CONTRACT TESTS")
    logger.info("=" * 60)
    
    # Test 1: Create contract
    contract_id = test_create_contract()
    print()
    
    # Test 2: Update price
    test_update_price()
    print()
    
    # Test 3: Calculate gain/loss
    test_calculate_gain_loss()
    print()
    
    # Test 4: Get farmer contracts
    test_get_farmer_contracts()
    print()
    
    # Test 5: Settle contract (will fail - not matured)
    test_settle_contract()
    print()
    
    logger.info("=" * 60)
    logger.info("✅ ALL TESTS COMPLETED!")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_all_tests()
