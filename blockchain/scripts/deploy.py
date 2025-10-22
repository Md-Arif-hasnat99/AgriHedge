"""
Blockchain deployment script for Ganache local testnet
Compiles and deploys the HedgingContract smart contract
"""

from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os
from pathlib import Path
from loguru import logger


# Install Solidity compiler
install_solc('0.8.19')


def compile_contract():
    """Compile the Solidity smart contract"""
    
    logger.info("📝 Compiling smart contract...")
    
    # Read the contract
    contract_path = Path(__file__).parent.parent / "contracts" / "HedgingContract.sol"
    with open(contract_path, 'r') as f:
        contract_source = f.read()
    
    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"HedgingContract.sol": {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.19",
    )
    
    logger.info("✅ Contract compiled successfully!")
    
    # Save compiled contract
    compiled_path = Path(__file__).parent.parent / "build" / "HedgingContract.json"
    compiled_path.parent.mkdir(exist_ok=True)
    
    with open(compiled_path, 'w') as f:
        json.dump(compiled_sol, f, indent=2)
    
    return compiled_sol


def deploy_contract(w3, account, private_key):
    """Deploy the contract to Ganache"""
    
    logger.info("🚀 Deploying contract to Ganache...")
    
    # Compile the contract
    compiled_sol = compile_contract()
    
    # Get contract interface
    contract_interface = compiled_sol['contracts']['HedgingContract.sol']['HedgingContract']
    bytecode = contract_interface['evm']['bytecode']['object']
    abi = contract_interface['abi']
    
    # Create contract instance
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build transaction
    nonce = w3.eth.get_transaction_count(account)
    
    transaction = Contract.constructor().build_transaction({
        'chainId': 1337,  # Ganache chain ID
        'gas': 3000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    logger.info(f"📤 Transaction sent: {tx_hash.hex()}")
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    logger.info(f"✅ Contract deployed at address: {tx_receipt.contractAddress}")
    
    # Save contract address and ABI
    deployment_info = {
        "address": tx_receipt.contractAddress,
        "abi": abi,
        "transaction_hash": tx_hash.hex(),
        "block_number": tx_receipt.blockNumber
    }
    
    deployment_path = Path(__file__).parent.parent / "build" / "deployment.json"
    with open(deployment_path, 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    return tx_receipt.contractAddress, abi


def main():
    """Main deployment function"""
    
    # Connect to Ganache
    GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:8545")
    
    logger.info(f"🔌 Connecting to Ganache at {GANACHE_URL}...")
    
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    
    if not w3.is_connected():
        logger.error("❌ Failed to connect to Ganache. Make sure it's running!")
        logger.info("💡 Start Ganache with: docker-compose up ganache")
        return
    
    logger.info("✅ Connected to Ganache!")
    
    # Get account from Ganache (first account)
    accounts = w3.eth.accounts
    account = accounts[0]
    
    # For Ganache, we can use a default private key (ONLY FOR DEVELOPMENT!)
    # In production, use environment variables
    private_key = os.getenv(
        "PRIVATE_KEY",
        "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
    )
    
    logger.info(f"🔑 Using account: {account}")
    
    # Deploy contract
    contract_address, abi = deploy_contract(w3, account, private_key)
    
    logger.info("=" * 60)
    logger.info("🎉 DEPLOYMENT SUCCESSFUL!")
    logger.info("=" * 60)
    logger.info(f"Contract Address: {contract_address}")
    logger.info(f"Network: Ganache (chainId: 1337)")
    logger.info(f"Account: {account}")
    logger.info("=" * 60)
    
    return contract_address, abi


if __name__ == "__main__":
    main()
