# AgriHedge Setup Script for Windows
# Run this script to set up the entire project

Write-Host "==================================" -ForegroundColor Green
Write-Host "AgriHedge Project Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  Please run this script as Administrator" -ForegroundColor Yellow
    exit
}

# Function to check if command exists
function Test-Command {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Cyan

$pythonInstalled = Test-Command python
$nodeInstalled = Test-Command node
$dockerInstalled = Test-Command docker

if (-not $pythonInstalled) {
    Write-Host "❌ Python not found. Installing Python 3.10..." -ForegroundColor Red
    winget install Python.Python.3.10 --accept-package-agreements --accept-source-agreements
} else {
    $pythonVersion = python --version
    Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
}

if (-not $nodeInstalled) {
    Write-Host "❌ Node.js not found. Installing Node.js LTS..." -ForegroundColor Red
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
} else {
    $nodeVersion = node --version
    Write-Host "✅ Node.js installed: $nodeVersion" -ForegroundColor Green
}

if (-not $dockerInstalled) {
    Write-Host "⚠️  Docker not found. Please install Docker Desktop manually." -ForegroundColor Yellow
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
} else {
    Write-Host "✅ Docker installed" -ForegroundColor Green
}

Write-Host ""

# Backend Setup
Write-Host "🐍 Setting up Backend (Python FastAPI)..." -ForegroundColor Cyan
Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "   Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "   Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "   Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "   Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "   ⚠️  Please update .env with your configuration" -ForegroundColor Yellow
}

Write-Host "✅ Backend setup complete!" -ForegroundColor Green
Set-Location ..

Write-Host ""

# Mobile Setup
Write-Host "📱 Setting up Mobile App (React Native)..." -ForegroundColor Cyan
Set-Location mobile

Write-Host "   Installing npm dependencies..." -ForegroundColor Yellow
npm install

Write-Host "✅ Mobile app setup complete!" -ForegroundColor Green
Set-Location ..

Write-Host ""

# Docker Setup
Write-Host "🐳 Docker Setup..." -ForegroundColor Cyan

if ($dockerInstalled) {
    Write-Host "   Starting Docker containers..." -ForegroundColor Yellow
    docker-compose up -d
    
    Write-Host "   Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    Write-Host "✅ Docker services started!" -ForegroundColor Green
    Write-Host ""
    Write-Host "   Services running:" -ForegroundColor Yellow
    Write-Host "   - Backend API: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "   - MongoDB: localhost:27017" -ForegroundColor Cyan
    Write-Host "   - Redis: localhost:6379" -ForegroundColor Cyan
    Write-Host "   - Ganache: localhost:8545" -ForegroundColor Cyan
} else {
    Write-Host "   ⚠️  Docker not available. Skipping container setup." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Update backend/.env with your configuration" -ForegroundColor Yellow
Write-Host "2. Start backend: cd backend; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload" -ForegroundColor Yellow
Write-Host "3. Start mobile app: cd mobile; npx expo start" -ForegroundColor Yellow
Write-Host "4. Visit API docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Cyan
Write-Host ""
