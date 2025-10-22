# AgriHedge Quick Start Guide

## Prerequisites Installation

### 1. Install Python 3.10+
```powershell
# Download from python.org or use:
winget install Python.Python.3.10
```

### 2. Install Node.js 18+
```powershell
winget install OpenJS.NodeJS.LTS
```

### 3. Install Docker Desktop
```powershell
winget install Docker.DockerDesktop
```

### 4. Install MongoDB (Optional - Docker will handle this)
```powershell
winget install MongoDB.Server
```

---

## Backend Setup (FastAPI)

### Step 1: Navigate to Backend Directory
```powershell
cd backend
```

### Step 2: Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```powershell
cp .env.example .env
# Edit .env file with your configurations
```

### Step 5: Start Backend Server
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

---

## Mobile App Setup (React Native / Expo)

### Step 1: Navigate to Mobile Directory
```powershell
cd mobile
```

### Step 2: Install Dependencies
```powershell
npm install
```

### Step 3: Start Expo Development Server
```powershell
npx expo start
```

### Step 4: Run on Device/Emulator
- Scan QR code with Expo Go app (Android/iOS)
- Press `a` for Android emulator
- Press `i` for iOS simulator

---

## Using Docker (Recommended for Full Stack)

### Start All Services
```powershell
docker-compose up -d
```

### View Logs
```powershell
docker-compose logs -f
```

### Stop Services
```powershell
docker-compose down
```

### Services Running:
- **Backend API:** http://localhost:8000
- **MongoDB:** localhost:27017
- **Redis:** localhost:6379
- **Ganache Blockchain:** localhost:8545
- **Admin Dashboard:** http://localhost:3000

---

## Initial Data Setup

### Create Sample Price Data
```powershell
cd backend
python -m app.db.seed_data
```

### Create Admin User
```powershell
python -m app.db.create_admin
```

---

## Testing the API

### 1. Register a New User
```powershell
curl -X POST http://localhost:8000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "full_name": "Test Farmer",
    "phone": "+919876543210",
    "email": "farmer@test.com",
    "password": "test123",
    "confirm_password": "test123",
    "role": "farmer"
  }'
```

### 2. Login
```powershell
curl -X POST http://localhost:8000/api/v1/auth/login `
  -d "username=+919876543210&password=test123"
```

### 3. Get Current Prices
```powershell
curl http://localhost:8000/api/v1/prices/current/soybean `
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Troubleshooting

### Port Already in Use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### MongoDB Connection Issues
```powershell
# Check MongoDB status
docker ps | findstr mongodb

# Restart MongoDB container
docker restart agrihedge-mongodb
```

### Expo Metro Bundler Issues
```powershell
# Clear cache
npx expo start -c

# Reset expo
npx expo start --clear
```

---

## Development Workflow

### Backend Development
1. Make code changes in `backend/app/`
2. Server auto-reloads with `--reload` flag
3. Test endpoints at http://localhost:8000/docs
4. Check logs in terminal

### Mobile Development
1. Make code changes in `mobile/src/`
2. Press `r` in terminal to reload app
3. Use Expo Dev Tools for debugging
4. Check console logs in terminal

---

## Project Structure Overview

```
AgriHedge/
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Config & security
│   │   ├── models/       # Pydantic models
│   │   ├── services/     # Business logic
│   │   └── ml/           # ML forecasting
│   └── requirements.txt
├── mobile/               # React Native app
│   ├── src/
│   │   ├── screens/     # App screens
│   │   ├── components/  # Reusable components
│   │   ├── services/    # API integration
│   │   └── store/       # Redux state
│   └── package.json
├── docker-compose.yml    # Docker services
└── README.md
```

---

## Next Steps

1. ✅ Start backend server
2. ✅ Start mobile app
3. 📱 Test user registration & login
4. 📊 View price dashboard
5. 🤖 Test AI price forecasting
6. 🔐 Create virtual hedging contracts
7. 🔗 View blockchain ledger

---

## Support

For issues or questions:
- Check API docs: http://localhost:8000/docs
- Review logs in `backend/logs/`
- Check Docker logs: `docker-compose logs -f`

---

**Happy Coding! 🚀**
