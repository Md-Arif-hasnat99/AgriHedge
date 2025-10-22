# AgriHedge Blockchain Smart Contract

## 📋 Overview

Solidity smart contract for transparent and immutable hedging contract management on blockchain.

## 🏗️ Contract Features

### HedgingContract.sol

- **Create Hedging Contracts**: Record virtual hedging contracts on-chain
- **Settle Contracts**: Calculate and record gain/loss at maturity
- **Price Oracle**: Update commodity prices (can integrate Chainlink)
- **Query Functions**: Get contract details, farmer contracts, prices
- **Events**: Track all contract lifecycle events
- **Security**: Owner-only functions, validation checks

### Contract Structure

```solidity
struct Hedge {
    uint256 contractId;
    address farmer;
    string commodity;
    uint256 quantity;
    uint256 strikePrice;
    uint256 currentPrice;
    uint256 startDate;
    uint256 maturityDate;
    ContractType contractType;  // Call or Put
    ContractStatus status;       // Active, Settled, Cancelled
    int256 gainLoss;
    string location;
    bool settled;
}
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install web3 py-solc-x
```

### Start Ganache (Local Blockchain)

```bash
# Option 1: Using Docker
docker-compose up ganache

# Option 2: Using Ganache CLI
npm install -g ganache
ganache --port 8545 --chainId 1337
```

### Deploy Contract

```bash
cd blockchain/scripts
python deploy.py
```

Output:
```
✅ Contract deployed at address: 0x1234...
```

### Test Contract

```bash
python test_contract.py
```

## 📝 Contract Functions

### Owner Functions

```solidity
// Create a new hedging contract
createContract(
    address farmer,
    string commodity,
    uint256 quantity,
    uint256 strikePrice,
    uint256 currentPrice,
    uint256 maturityDate,
    uint8 contractType,
    string location
) returns (uint256)

// Settle a matured contract
settleContract(uint256 contractId, uint256 settlementPrice)

// Cancel a contract
cancelContract(uint256 contractId)

// Update commodity price
updatePrice(string commodity, uint256 price)
```

### Public View Functions

```solidity
// Get contract details
getContract(uint256 contractId) returns (...)

// Get all contracts for a farmer
getFarmerContracts(address farmer) returns (uint256[])

// Get commodity price
getCommodityPrice(string commodity) returns (uint256)

// Calculate current gain/loss
calculateCurrentGainLoss(uint256 contractId, uint256 currentPrice) returns (int256)

// Check if contract is matured
isContractMatured(uint256 contractId) returns (bool)
```

## 🔗 Integration with Backend

The backend service (`app/services/blockchain.py`) integrates with this contract:

```python
from app.services.blockchain import Web3BlockchainService

# Initialize service
blockchain = Web3BlockchainService(
    provider_url="http://127.0.0.1:8545",
    contract_address="0x...",
    private_key="0x..."
)

# Create contract on blockchain
contract_id = await blockchain.create_contract(
    farmer_address="0x...",
    commodity="Soybean",
    quantity=1000,
    strike_price=5000,
    current_price=4800,
    maturity_date=1234567890,
    contract_type=0
)

# Settle contract
await blockchain.settle_contract(contract_id, settlement_price=5200)
```

## 🌐 Networks

### Ganache (Local Development)
- **URL**: http://127.0.0.1:8545
- **Chain ID**: 1337
- **Used for**: Development and testing

### Polygon Mumbai (Testnet)
- **URL**: https://rpc-mumbai.maticvigil.com
- **Chain ID**: 80001
- **Used for**: Testing with real network conditions
- **Faucet**: https://faucet.polygon.technology/

### Polygon Mainnet (Production)
- **URL**: https://polygon-rpc.com
- **Chain ID**: 137
- **Used for**: Production deployment
- **Low gas fees**: ~$0.01 per transaction

## 📊 Events

The contract emits events for tracking:

```solidity
event ContractCreated(uint256 contractId, address farmer, string commodity, uint256 strikePrice, uint256 maturityDate);
event ContractSettled(uint256 contractId, address farmer, int256 gainLoss, uint256 settlementDate);
event PriceUpdated(string commodity, uint256 newPrice, uint256 timestamp);
event ContractCancelled(uint256 contractId, address farmer, uint256 timestamp);
```

## 🔒 Security

- **Access Control**: Owner-only functions for critical operations
- **Validation**: Input validation on all functions
- **Immutability**: Contract state changes are permanent
- **Events**: Full audit trail of all operations

## 🛠️ Testing

Run comprehensive tests:

```bash
# Deploy and test
python scripts/deploy.py
python scripts/test_contract.py
```

Tests include:
- ✅ Contract creation
- ✅ Price updates
- ✅ Gain/loss calculation
- ✅ Contract settlement
- ✅ Query functions

## 📈 Future Enhancements

1. **Chainlink Oracle Integration**: Real-time price feeds
2. **Multi-signature**: Require multiple approvals
3. **Automated Settlement**: Use Chainlink Keepers
4. **NFT Certificates**: Mint NFTs for contracts
5. **Layer 2**: Deploy on Polygon zkEVM for lower fees

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

See CONTRIBUTING.md for contribution guidelines
