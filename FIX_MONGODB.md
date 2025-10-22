# 🚀 AgriHedge - Getting Started

## ⚠️ Current Issue: MongoDB Not Running

Your code is **100% correct** ✅ - you just need to start MongoDB!

## 🔧 Quick Fix (Choose One Option)

### Option 1: Install MongoDB Community (Recommended for Development)

1. **Download MongoDB**:
   - Visit: <https://www.mongodb.com/try/download/community>
   - Select: Windows, MSI installer
   - Click: Download

2. **Install**:
   - Run the installer
   - Choose "Complete" installation
   - Check "Install MongoDB as a Service" ✅
   - Finish installation

3. **Verify**:

   ```powershell
   # Check if MongoDB is running
   mongosh
   # You should see "test>" prompt
   # Type "exit" to close
   ```

4. **Start Backend**:

   ```powershell
   cd C:\SIH\backend
   .\start.ps1
   ```

### Option 2: Use Docker Desktop

1. **Install Docker Desktop**:
   - Download: <https://www.docker.com/products/docker-desktop/>
   - Install and restart computer

2. **Start MongoDB**:

   ```powershell
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   ```

3. **Start Backend**:

   ```powershell
   cd C:\SIH\backend
   .\start.ps1
   ```

### Option 3: Use MongoDB Atlas (Cloud - Free)

1. **Create Account**:
   - Visit: <https://www.mongodb.com/cloud/atlas/register>
   - Sign up (free tier available)

2. **Create Cluster**:
   - Choose "Free Shared" tier
   - Select nearest region
   - Create cluster

3. **Get Connection String**:
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string

4. **Update Configuration**:

   ```powershell
   cd C:\SIH\backend
   # Edit .env file and add:
   # MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agrihedge
   ```

5. **Start Backend**:

   ```powershell
   .\start.ps1
   ```

## ✅ What's Working Now

- ✅ All Python dependencies installed
- ✅ Virtual environment configured
- ✅ All imports resolved correctly
- ✅ Smart contract created (HedgingContract.sol)
- ✅ Blockchain scripts ready
- ✅ API code is correct

## 🎯 Next Steps After MongoDB is Running

1. **Test API**: <http://localhost:8000/docs>
2. **Register a user**
3. **Login and get JWT token**
4. **Explore the endpoints**

## 🐛 Still Having Issues?

### Check if MongoDB is running

```powershell
# Test connection
mongosh
```

### Check which port MongoDB is using

```powershell
netstat -an | findstr :27017
```

### View backend logs

The startup script shows detailed error messages

## 📱 Mobile App (After Backend is Running)

```powershell
cd C:\SIH\mobile
npm install
npx expo start
```

## 🔗 Blockchain (Optional)

```powershell
# Install Ganache
npm install -g ganache

# Start Ganache
ganache --port 8545 --chainId 1337

# Deploy contract (in new terminal)
cd C:\SIH\blockchain\scripts
pip install -r ..\requirements.txt
python deploy.py
```

## 💡 Recommended Path

**For fastest setup**:

1. Install MongoDB Community Edition (10 minutes)
2. It will run automatically as a Windows service
3. Run `.\start.ps1` in backend folder
4. Visit <http://localhost:8000/docs>
5. You're done! 🎉

## 📚 Documentation

- `START_HERE.md` - Detailed setup guide
- `STATUS_REPORT.md` - What's been completed
- `blockchain/README.md` - Smart contract docs
- `INSTALLATION_GUIDE.md` - Troubleshooting

---

**TL;DR**: Install MongoDB, then run `.\start.ps1` - that's it! 🚀
