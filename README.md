# AgriHedge: Oilseed Price Risk Management Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React Native](https://img.shields.io/badge/react--native-0.72+-blue.svg)](https://reactnative.dev/)

## Overview

AgriHedge is a **mobile-first, blockchain-enabled, AI-driven price hedging simulation platform** designed for Indian oilseed farmers and Farmer Producer Organizations (FPOs). The platform enables farmers to:

- 📊 View real-time and forecasted oilseed prices (soybean, mustard)
- 🤖 Access AI-powered price predictions with 7-30 day forecasts
- 🔐 Simulate virtual hedging contracts with blockchain transparency
- 📱 Receive market alerts for price volatility
- 🎓 Learn about futures, forward contracts, and hedging strategies
- 💬 Get assistance through an AI-powered chatbot (vernacular support)

## Architecture

```
AgriHedge/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── models/    # Database models
│   │   ├── services/  # Business logic
│   │   └── ml/        # AI forecasting models
│   ├── blockchain/    # Smart contracts & ledger
│   └── tests/         # Backend tests
├── mobile/            # React Native mobile app
│   ├── src/
│   │   ├── screens/   # App screens
│   │   ├── components/# Reusable components
│   │   ├── services/  # API integration
│   │   └── locales/   # Multilingual support
│   └── __tests__/     # Frontend tests
├── admin-dashboard/   # Web admin panel
│   └── src/
└── docs/              # Documentation
```

## Tech Stack

### Backend
- **Framework:** Python 3.10+ with FastAPI
- **Database:** MongoDB (or Firebase)
- **AI/ML:** scikit-learn, statsmodels (ARIMA)
- **Authentication:** JWT tokens
- **Notifications:** Twilio SMS + Firebase Cloud Messaging

### Blockchain
- **Development:** Ganache (local testnet)
- **Production:** Polygon testnet
- **Smart Contracts:** Solidity

### Frontend
- **Mobile:** React Native with Expo
- **Admin:** React.js with Material-UI
- **Charts:** Victory Native / Recharts
- **State Management:** Redux Toolkit

### DevOps
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Hosting:** AWS (backend) + Vercel (admin)

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- MongoDB (or Firebase account)
- Ganache CLI (for local blockchain)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables
copy .env.example .env
# Edit .env with your configurations

# Run database migrations
python -m app.db.init_db

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Mobile App Setup

```bash
# Navigate to mobile directory
cd mobile

# Install dependencies
npm install

# Start Expo dev server
npx expo start

# Run on Android
npx expo run:android

# Run on iOS
npx expo run:ios
```

### Blockchain Setup

```bash
# Install Ganache CLI globally
npm install -g ganache-cli

# Start local blockchain
ganache-cli -p 8545 -m "your mnemonic phrase here"

# Deploy smart contracts
cd backend/blockchain
npm install
npx hardhat run scripts/deploy.js --network localhost
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Features Roadmap

### ✅ Phase 1 - MVP (7 days)
- [x] User authentication & farmer profiles
- [x] Price visualization dashboard
- [x] AI price forecasting (ARIMA model)
- [x] Virtual hedging simulator
- [x] Blockchain ledger (simulated)
- [x] Market alerts (SMS/Push)
- [x] Educational hub & chatbot
- [x] Admin analytics dashboard

### 🚧 Phase 2 - Enhancement (Next 30 days)
- [ ] Real NCDEX/Agmarknet data integration
- [ ] Advanced ML models (LSTM, Prophet)
- [ ] Multi-commodity support
- [ ] Group hedging for FPOs
- [ ] Weather data integration
- [ ] WhatsApp notifications
- [ ] Voice interface (regional languages)

### 🔮 Phase 3 - Scale (Next 90 days)
- [ ] Real futures market integration
- [ ] KYC verification
- [ ] Payment gateway integration
- [ ] Insurance product integration
- [ ] Government scheme recommendations
- [ ] Market intelligence reports

## Project Milestones

| Day | Milestone | Status |
|-----|-----------|--------|
| 1-2 | User Auth & Dashboard Setup | ✅ |
| 2-3 | Price Visualization & AI Forecast API | ✅ |
| 3-4 | Virtual Hedging Simulator & Contract UI | ✅ |
| 4-5 | Blockchain Ledger Integration | ✅ |
| 5-6 | Market Alerts & Notification Setup | ✅ |
| 6   | Educational Hub & AI Chatbot | ✅ |
| 7   | Admin Analytics Dashboard & Refinement | ✅ |

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Mobile tests
cd mobile
npm test

# E2E tests
npm run test:e2e
```

## Deployment

### Backend (AWS EC2 + RDS)
```bash
# Build Docker image
docker build -t agrihedge-backend ./backend

# Push to ECR
docker tag agrihedge-backend:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/agrihedge-backend:latest
docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/agrihedge-backend:latest

# Deploy to ECS
aws ecs update-service --cluster agrihedge --service backend --force-new-deployment
```

### Mobile (Expo EAS)
```bash
cd mobile
eas build --platform all
eas submit --platform all
```

### Admin Dashboard (Vercel)
```bash
cd admin-dashboard
vercel --prod
```

## Environment Variables

### Backend (.env)
```env
# Database
MONGODB_URI=mongodb://localhost:27017/agrihedge
DATABASE_NAME=agrihedge

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Blockchain
BLOCKCHAIN_RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=0x...

# Notifications
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# External APIs
AGMARKNET_API_KEY=your-api-key
NCDEX_API_KEY=your-api-key
```

### Mobile (.env)
```env
API_BASE_URL=http://localhost:8000
BLOCKCHAIN_RPC_URL=http://localhost:8545
FIREBASE_CONFIG={"apiKey": "..."}
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- All API endpoints are secured with JWT authentication
- Blockchain contracts are immutable and transparent
- User data is encrypted at rest
- Regular security audits are performed
- OWASP Top 10 compliance

## Support

- 📧 Email: support@agrihedge.com
- 💬 Discord: [Join our community](https://discord.gg/agrihedge)
- 📱 WhatsApp: +91-XXXXXXXXXX
- 📚 Documentation: [docs.agrihedge.com](https://docs.agrihedge.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Indian Council of Agricultural Research (ICAR)
- National Commodity & Derivatives Exchange (NCDEX)
- Agmarknet for market data
- Polygon for blockchain infrastructure
- Open source community

## Team

Built with ❤️ by the AgriHedge team for Smart India Hackathon 2025

---

**Note:** This is an MVP for demonstration purposes. For production use with real money, ensure compliance with SEBI regulations and obtain necessary licenses.
