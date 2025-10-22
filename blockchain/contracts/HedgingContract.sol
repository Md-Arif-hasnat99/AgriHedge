// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title HedgingContract
 * @dev Smart contract for oilseed price hedging and risk management
 * Records hedging contracts on blockchain for transparency
 */
contract HedgingContract {
    
    // Contract status enum
    enum ContractStatus { Active, Settled, Cancelled }
    
    // Contract type enum
    enum ContractType { Call, Put }
    
    // Hedging contract structure
    struct Hedge {
        uint256 contractId;
        address farmer;
        string commodity;
        uint256 quantity;
        uint256 strikePrice;
        uint256 currentPrice;
        uint256 startDate;
        uint256 maturityDate;
        ContractType contractType;
        ContractStatus status;
        int256 gainLoss;
        string location;
        bool settled;
    }
    
    // State variables
    mapping(uint256 => Hedge) public hedges;
    mapping(address => uint256[]) public farmerContracts;
    uint256 public contractCounter;
    address public owner;
    
    // Price oracle mapping (in real implementation, use Chainlink)
    mapping(string => uint256) public commodityPrices;
    
    // Events
    event ContractCreated(
        uint256 indexed contractId,
        address indexed farmer,
        string commodity,
        uint256 strikePrice,
        uint256 maturityDate
    );
    
    event ContractSettled(
        uint256 indexed contractId,
        address indexed farmer,
        int256 gainLoss,
        uint256 settlementDate
    );
    
    event PriceUpdated(
        string indexed commodity,
        uint256 newPrice,
        uint256 timestamp
    );
    
    event ContractCancelled(
        uint256 indexed contractId,
        address indexed farmer,
        uint256 timestamp
    );
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier contractExists(uint256 _contractId) {
        require(_contractId < contractCounter, "Contract does not exist");
        _;
    }
    
    modifier onlyFarmer(uint256 _contractId) {
        require(
            hedges[_contractId].farmer == msg.sender,
            "Only contract owner can perform this action"
        );
        _;
    }
    
    // Constructor
    constructor() {
        owner = msg.sender;
        contractCounter = 0;
    }
    
    /**
     * @dev Create a new hedging contract
     */
    function createContract(
        address _farmer,
        string memory _commodity,
        uint256 _quantity,
        uint256 _strikePrice,
        uint256 _currentPrice,
        uint256 _maturityDate,
        uint8 _contractType,
        string memory _location
    ) public onlyOwner returns (uint256) {
        require(_maturityDate > block.timestamp, "Maturity date must be in future");
        require(_quantity > 0, "Quantity must be greater than zero");
        require(_strikePrice > 0, "Strike price must be greater than zero");
        
        uint256 contractId = contractCounter;
        
        hedges[contractId] = Hedge({
            contractId: contractId,
            farmer: _farmer,
            commodity: _commodity,
            quantity: _quantity,
            strikePrice: _strikePrice,
            currentPrice: _currentPrice,
            startDate: block.timestamp,
            maturityDate: _maturityDate,
            contractType: ContractType(_contractType),
            status: ContractStatus.Active,
            gainLoss: 0,
            location: _location,
            settled: false
        });
        
        farmerContracts[_farmer].push(contractId);
        contractCounter++;
        
        emit ContractCreated(
            contractId,
            _farmer,
            _commodity,
            _strikePrice,
            _maturityDate
        );
        
        return contractId;
    }
    
    /**
     * @dev Settle a hedging contract
     */
    function settleContract(
        uint256 _contractId,
        uint256 _settlementPrice
    ) public onlyOwner contractExists(_contractId) {
        Hedge storage hedge = hedges[_contractId];
        
        require(hedge.status == ContractStatus.Active, "Contract is not active");
        require(!hedge.settled, "Contract already settled");
        require(block.timestamp >= hedge.maturityDate, "Contract not yet matured");
        
        // Calculate gain/loss
        int256 priceDiff = int256(_settlementPrice) - int256(hedge.strikePrice);
        int256 gainLoss;
        
        if (hedge.contractType == ContractType.Call) {
            // Call option: profit when price goes up
            gainLoss = priceDiff * int256(hedge.quantity);
        } else {
            // Put option: profit when price goes down
            gainLoss = -priceDiff * int256(hedge.quantity);
        }
        
        hedge.gainLoss = gainLoss;
        hedge.currentPrice = _settlementPrice;
        hedge.status = ContractStatus.Settled;
        hedge.settled = true;
        
        emit ContractSettled(_contractId, hedge.farmer, gainLoss, block.timestamp);
    }
    
    /**
     * @dev Cancel a contract before maturity
     */
    function cancelContract(uint256 _contractId) 
        public 
        onlyOwner 
        contractExists(_contractId) 
    {
        Hedge storage hedge = hedges[_contractId];
        
        require(hedge.status == ContractStatus.Active, "Contract is not active");
        require(!hedge.settled, "Contract already settled");
        
        hedge.status = ContractStatus.Cancelled;
        
        emit ContractCancelled(_contractId, hedge.farmer, block.timestamp);
    }
    
    /**
     * @dev Update commodity price (Oracle function)
     */
    function updatePrice(string memory _commodity, uint256 _price) 
        public 
        onlyOwner 
    {
        require(_price > 0, "Price must be greater than zero");
        commodityPrices[_commodity] = _price;
        
        emit PriceUpdated(_commodity, _price, block.timestamp);
    }
    
    /**
     * @dev Get contract details
     */
    function getContract(uint256 _contractId) 
        public 
        view 
        contractExists(_contractId)
        returns (
            address farmer,
            string memory commodity,
            uint256 quantity,
            uint256 strikePrice,
            uint256 currentPrice,
            uint256 maturityDate,
            ContractType contractType,
            ContractStatus status,
            int256 gainLoss,
            bool settled
        ) 
    {
        Hedge memory hedge = hedges[_contractId];
        return (
            hedge.farmer,
            hedge.commodity,
            hedge.quantity,
            hedge.strikePrice,
            hedge.currentPrice,
            hedge.maturityDate,
            hedge.contractType,
            hedge.status,
            hedge.gainLoss,
            hedge.settled
        );
    }
    
    /**
     * @dev Get all contracts for a farmer
     */
    function getFarmerContracts(address _farmer) 
        public 
        view 
        returns (uint256[] memory) 
    {
        return farmerContracts[_farmer];
    }
    
    /**
     * @dev Get current price of commodity
     */
    function getCommodityPrice(string memory _commodity) 
        public 
        view 
        returns (uint256) 
    {
        return commodityPrices[_commodity];
    }
    
    /**
     * @dev Get total number of contracts
     */
    function getTotalContracts() public view returns (uint256) {
        return contractCounter;
    }
    
    /**
     * @dev Check if contract is matured
     */
    function isContractMatured(uint256 _contractId) 
        public 
        view 
        contractExists(_contractId)
        returns (bool) 
    {
        return block.timestamp >= hedges[_contractId].maturityDate;
    }
    
    /**
     * @dev Get contract gain/loss without settling
     */
    function calculateCurrentGainLoss(uint256 _contractId, uint256 _currentPrice) 
        public 
        view 
        contractExists(_contractId)
        returns (int256) 
    {
        Hedge memory hedge = hedges[_contractId];
        int256 priceDiff = int256(_currentPrice) - int256(hedge.strikePrice);
        
        if (hedge.contractType == ContractType.Call) {
            return priceDiff * int256(hedge.quantity);
        } else {
            return -priceDiff * int256(hedge.quantity);
        }
    }
}
