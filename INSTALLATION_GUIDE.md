# AgriHedge - Complete Installation & Troubleshooting Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Automated Installation](#automated-installation)
3. [Manual Installation](#manual-installation)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Testing the API](#testing-the-api)
7. [Mobile App Setup](#mobile-app-setup)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 20.04+
- **RAM**: 8 GB
- **Disk Space**: 5 GB free
- **Internet**: Stable connection for package downloads

### Required Software
- Python 3.10 or higher
- Node.js 18 or higher
- Docker Desktop (optional but recommended)
- Git
- MongoDB 7.0+ (if not using Docker)
- Visual Studio Code (recommended)

---

## Automated Installation

### Windows (PowerShell)

Run as Administrator:

```powershell
# Clone the repository (if not already done)
git clone <repository-url>
cd C:\SIH

# Run setup script
.\setup.ps1
```

The script will:
- Check and install prerequisites
- Set up Python virtual environment
- Install Python dependencies
- Install Node.js dependencies
- Create .env file
- Start Docker containers (if available)

---

## Manual Installation

### Step 1: Install Python

**Windows:**
```powershell
winget install Python.Python.3.10
```

**macOS:**
```bash
brew install python@3.10
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### Step 2: Install Node.js

**Windows:**
```powershell
winget install OpenJS.NodeJS.LTS
```

**macOS:**
```bash
brew install node
```

**Ubuntu:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Step 3: Install Docker

**Windows & macOS:**
- Download from https://www.docker.com/products/docker-desktop
- Run installer and follow instructions

**Ubuntu:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Step 4: Install MongoDB (if not using Docker)

**Windows:**
```powershell
winget install MongoDB.Server
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
```

**Ubuntu:**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## Database Setup

### Using Docker (Recommended)

```powershell
# Start all services including MongoDB
docker-compose up -d

# Wait for services to start (30 seconds)
timeout /t 30

# Initialize database
cd backend
python -m app.db.init_db
```

### Manual MongoDB Setup

1. **Start MongoDB:**

**Windows:**
```powershell
net start MongoDB
```

**macOS/Linux:**
```bash
brew services start mongodb-community  # macOS
sudo systemctl start mongod  # Linux
```

2. **Initialize Database:**

```powershell
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and update:
# MONGODB_URI=mongodb://localhost:27017/agrihedge

# Initialize database
python -m app.db.init_db
```

---

## Running the Application

### Option 1: Using Docker

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

**Services will be available at:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MongoDB: localhost:27017
- Redis: localhost:6379
- Ganache Blockchain: localhost:8545

### Option 2: Running Manually

**Backend:**

```powershell
cd backend

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Mobile App:**

```powershell
cd mobile

# Install dependencies (first time only)
npm install

# Start Expo
npx expo start

# Then:
# - Press 'a' for Android
# - Press 'i' for iOS
# - Scan QR code with Expo Go app
```

---

## Testing the API

### 1. Access API Documentation

Open browser: http://localhost:8000/docs

### 2. Test with Swagger UI

1. Go to http://localhost:8000/docs
2. Click on "POST /api/v1/auth/register"
3. Click "Try it out"
4. Enter test data:

```json
{
  "full_name": "Test Farmer",
  "phone": "+919999999999",
  "email": "test@example.com",
  "password": "test123",
  "confirm_password": "test123",
  "role": "farmer",
  "preferred_language": "en"
}
```

5. Click "Execute"
6. Check response (should be 201 Created)

### 3. Test Login

1. Click on "POST /api/v1/auth/login"
2. Enter:
   - username: `+919999999999`
   - password: `test123`
3. Copy the `access_token` from response

### 4. Test Authenticated Endpoint

1. Click "Authorize" button (top right)
2. Enter: `Bearer <your_access_token>`
3. Click "Authorize"
4. Try "GET /api/v1/auth/me"

---

## Mobile App Setup

### Install Expo CLI

```powershell
npm install -g expo-cli
```

### Setup Mobile App

```powershell
cd mobile
npm install
```

### Configure API URL

Edit `mobile/app.json`:

```json
"extra": {
  "apiUrl": "http://YOUR_IP:8000/api/v1"
}
```

Replace `YOUR_IP` with your computer's IP address (not localhost if testing on physical device).

**Find your IP:**

Windows:
```powershell
ipconfig
# Look for IPv4 Address
```

macOS/Linux:
```bash
ifconfig
# Look for inet address
```

### Run on Android Emulator

```powershell
npx expo run:android
```

### Run on iOS Simulator (macOS only)

```bash
npx expo run:ios
```

### Run on Physical Device

1. Install "Expo Go" app from Play Store / App Store
2. Run: `npx expo start`
3. Scan QR code with Expo Go app

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error:** `Address already in use: 8000`

**Solution:**

Windows:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

macOS/Linux:
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

#### 2. MongoDB Connection Failed

**Error:** `ServerSelectionTimeoutError`

**Solution:**

1. Check MongoDB is running:

Windows:
```powershell
net start MongoDB
```

macOS:
```bash
brew services start mongodb-community
```

Linux:
```bash
sudo systemctl start mongod
sudo systemctl status mongod
```

2. Check connection string in `.env`:
```
MONGODB_URI=mongodb://localhost:27017/agrihedge
```

#### 3. Docker Containers Not Starting

**Error:** `Cannot connect to Docker daemon`

**Solution:**

1. Start Docker Desktop
2. Wait for it to fully start
3. Try again: `docker-compose up -d`

#### 4. Python Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**

```powershell
# Ensure virtual environment is activated
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 5. Expo Metro Bundler Issues

**Error:** `Metro bundler has encountered an error`

**Solution:**

```powershell
cd mobile

# Clear cache
npx expo start -c

# Or reset expo
rm -rf node_modules
npm install
npx expo start --clear
```

#### 6. CORS Errors in Mobile App

**Error:** `Network request failed` or `CORS blocked`

**Solution:**

1. Check `backend/app/core/config.py`:

```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8081",
    "http://localhost:19006",
    "http://YOUR_IP:19006"  # Add your IP
]
```

2. Restart backend server

#### 7. JWT Token Expired

**Error:** `401 Unauthorized` on API calls

**Solution:**

The mobile app should automatically refresh tokens. If not:

1. Log out and log back in
2. Check token expiration in `backend/.env`:
```
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## FAQ

### Q: Do I need Docker to run this project?

**A:** No, Docker is optional but recommended. You can run MongoDB, Redis, and Ganache manually.

### Q: Can I use a different database?

**A:** The project is designed for MongoDB, but you can adapt it for PostgreSQL or MySQL by changing the database layer.

### Q: How do I add more commodities?

**A:** Edit `backend/app/models/price.py` and add to `CommodityType` enum:

```python
class CommodityType(str, Enum):
    SOYBEAN = "soybean"
    MUSTARD = "mustard"
    YOUR_COMMODITY = "your_commodity"
```

### Q: How do I deploy to production?

**A:** See deployment guides:
- Backend: AWS EC2 or Azure App Service
- Mobile: EAS Build (Expo Application Services)
- Database: MongoDB Atlas (cloud)

### Q: How do I add real market data?

**A:** Integrate with Agmarknet API in `backend/app/services/price_data.py`:

```python
import httpx

async def fetch_agmarknet_prices(commodity: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.AGMARKNET_API_URL}/prices",
            params={"commodity": commodity}
        )
        return response.json()
```

### Q: Can I use this for other commodities (not oilseeds)?

**A:** Yes! The platform is designed to be extensible. Just add more commodity types and adjust the ML models accordingly.

### Q: How do I backup the database?

**A:**

```powershell
# Using Docker
docker exec agrihedge-mongodb mongodump --out /backup

# Manual MongoDB
mongodump --db agrihedge --out ./backup
```

---

## Getting Help

### Documentation
- Main README: [README.md](README.md)
- Quick Start: [QUICKSTART.md](QUICKSTART.md)
- Project Summary: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Community
- GitHub Issues: Report bugs and request features
- Discord: Join team discussion
- Email: support@agrihedge.com

---

## Logs and Debugging

### Backend Logs

**Docker:**
```powershell
docker-compose logs -f backend
```

**Manual:**
Check `backend/logs/agrihedge.log`

### Mobile Logs

**Expo:**
```powershell
npx expo start
# Logs appear in terminal
```

**React Native Debugger:**
- Press `j` in Expo terminal
- Opens Chrome DevTools

### Database Logs

**MongoDB:**
```powershell
# Docker
docker logs agrihedge-mongodb

# Manual (Windows)
type "C:\Program Files\MongoDB\Server\7.0\log\mongod.log"

# Manual (macOS)
tail -f /usr/local/var/log/mongodb/mongo.log

# Manual (Linux)
sudo tail -f /var/log/mongodb/mongod.log
```

---

## Performance Optimization

### Backend
- Enable Redis caching
- Use database indexes
- Implement pagination
- Compress responses

### Mobile
- Use FlatList for long lists
- Implement lazy loading
- Cache API responses
- Optimize images

---

**Last Updated:** October 22, 2025

**Version:** 1.0.0

**Maintainers:** AgriHedge Team - Smart India Hackathon 2025
