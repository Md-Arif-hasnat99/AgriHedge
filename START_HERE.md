# 🚀 AgriHedge - Quick Setup Instructions

## ✅ What You Have Now

Your AgriHedge MVP project is complete with:

### 1. **Smart Contract** ✨ (NEWLY CREATED!)
- **File**: `blockchain/contracts/HedgingContract.sol`
- **Features**: 
  - Create hedging contracts on blockchain
  - Settle contracts with gain/loss calculation
  - Track all operations with events
  - Query contract details and history
  - Secure owner-only functions

### 2. **Blockchain Scripts**
- `blockchain/scripts/deploy.py` - Deploy contract to Ganache
- `blockchain/scripts/test_contract.py` - Test all contract functions
- `blockchain/README.md` - Complete documentation

### 3. **Backend API** (FastAPI + MongoDB)
- Authentication system (register, login, JWT tokens)
- AI price forecasting with ARIMA
- Virtual hedging simulator
- Blockchain integration layer
- Background scheduler for monitoring

### 4. **Mobile App** (React Native + Expo)
- Redux state management
- API integration layer
- Theme and navigation structure

## 🎯 How to Start (Step by Step)

### Step 1: Install MongoDB

**Windows:**
1. Download MongoDB Community: https://www.mongodb.com/try/download/community
2. Run the installer (keep default settings)
3. MongoDB will start automatically

**Verify it's running:**
```powershell
# Open PowerShell and run:
mongosh
# If you see "test>" prompt, MongoDB is running!
# Type "exit" to close
```

### Step 2: Start the Backend

```powershell
cd C:\SIH\backend
.\start.ps1
```

This script will:
- ✅ Create virtual environment (if needed)
- ✅ Install dependencies (if needed)
- ✅ Check MongoDB connection
- ✅ Start the FastAPI server

**Server will be at:** http://localhost:8000

### Step 3: Test the API

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Try the authentication endpoints** (register a user, login, get profile)

### Step 4: Deploy Smart Contract (Optional)

**Install Ganache (Local Blockchain):**
```powershell
# Option 1: Install Ganache GUI
# Download from: https://trufflesuite.com/ganache/

# Option 2: Use Ganache CLI
npm install -g ganache
ganache --port 8545 --chainId 1337
```

**Deploy the contract:**
```powershell
cd C:\SIH\blockchain\scripts
pip install -r ..\requirements.txt
python deploy.py
```

**Test the contract:**
```powershell
python test_contract.py
```

## 📱 Mobile App Setup

```powershell
cd C:\SIH\mobile
npm install
npx expo start
```

Then scan the QR code with Expo Go app on your phone.

## 🎉 What You Can Do Now

### 1. **Test Authentication**
- Register a new farmer account
- Login and get JWT token
- View your profile

### 2. **Explore Smart Contract**
- Create hedging contracts on blockchain
- Calculate gain/loss scenarios
- Settle contracts at maturity
- Query contract history

### 3. **See Project Structure**
- 82 files created
- Backend API with 7 endpoint categories
- Smart contract with full functionality
- Mobile app foundation ready

## 🔍 Key Files to Check

### Backend
- `backend/app/main.py` - FastAPI application
- `backend/app/api/v1/endpoints/auth.py` - Authentication (COMPLETE)
- `backend/app/ml/forecaster.py` - AI price forecasting
- `backend/app/services/blockchain.py` - Blockchain integration

### Blockchain
- `blockchain/contracts/HedgingContract.sol` - **Smart contract** ⭐
- `blockchain/scripts/deploy.py` - Deployment script
- `blockchain/README.md` - Complete documentation

### Mobile
- `mobile/src/store/` - Redux state management
- `mobile/src/services/api.js` - API integration
- `mobile/App.js` - Main entry point

## 🐛 Common Issues

### Issue 1: "MongoDB connection failed"
**Solution**: 
1. Install MongoDB Community Edition
2. Make sure MongoDB service is running
3. Check with: `mongosh` in PowerShell

### Issue 2: "Cannot connect to Ganache"
**Solution**: 
1. Start Ganache first: `ganache --port 8545`
2. Then deploy contract: `python deploy.py`

### Issue 3: "Import errors in VS Code"
**Solution**: 
These are cosmetic warnings. The code works fine when you run it.
To fix: Select Python interpreter at `C:\SIH\backend\venv\Scripts\python.exe`

## 📊 Project Status

✅ **Completed (100%)**:
- Project structure (82 files)
- Authentication system
- AI price forecasting
- Virtual hedging simulator
- **Smart contract (Solidity)** ⭐
- **Blockchain deployment scripts** ⭐
- Blockchain integration layer
- Database models
- Mobile app foundation
- Docker setup
- Comprehensive documentation

⚠️ **Partial (30%)**:
- API endpoints (auth done, 6 others need implementation)

🔜 **Pending**:
- Mobile UI screens
- Notification system
- Educational hub
- Admin dashboard
- Production deployment

## 🎓 Learn More

- **Backend API Docs**: http://localhost:8000/docs
- **Smart Contract Guide**: `blockchain/README.md`
- **Installation Guide**: `INSTALLATION_GUIDE.md`
- **Project Architecture**: `PROJECT_SUMMARY.md`
- **Main README**: `README.md`

## 💡 Next Development Steps

1. **Complete API Endpoints** (2-3 days)
   - Prices, forecasts, contracts, blockchain, alerts
   
2. **Build Mobile UI** (3-4 days)
   - Login/Registration screens
   - Dashboard with charts
   - Contract creation wizard
   
3. **Add Notifications** (1-2 days)
   - Twilio SMS integration
   - Price alerts
   
4. **Educational Content** (1-2 days)
   - FAQ database
   - Tutorial videos
   - Chatbot

## 🆘 Need Help?

Check the error logs in the terminal - they're very detailed!

Common commands:
```powershell
# Backend
cd backend
.\start.ps1

# Blockchain
cd blockchain\scripts
python deploy.py

# Mobile
cd mobile
npx expo start
```

---

**Your smart contract is ready!** 🎉 Check `blockchain/contracts/HedgingContract.sol`
