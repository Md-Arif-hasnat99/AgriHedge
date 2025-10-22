# AgriHedge Startup Guide
# Run this script to start the backend server

Write-Host "=" -ForegroundColor Cyan
Write-Host "🌾 AgriHedge Backend Startup" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path ".\venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "💡 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Check if dependencies are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>$null
if ($pipList -notlike "*fastapi*") {
    Write-Host "💡 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ Dependencies installed!" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" -ForegroundColor Cyan
Write-Host "⚠️  IMPORTANT: MongoDB Required" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Cyan
Write-Host ""
Write-Host "The server needs MongoDB to run." -ForegroundColor White
Write-Host ""
Write-Host "Option 1 - Install MongoDB Community Edition:" -ForegroundColor Cyan
Write-Host "  Download: https://www.mongodb.com/try/download/community" -ForegroundColor White
Write-Host "  After install, MongoDB will run automatically" -ForegroundColor White
Write-Host ""
Write-Host "Option 2 - Use Docker:" -ForegroundColor Cyan
Write-Host "  docker run -d -p 27017:27017 --name mongodb mongo:7.0" -ForegroundColor White
Write-Host ""
Write-Host "Press ENTER to continue (make sure MongoDB is running)..." -ForegroundColor Yellow
$null = Read-Host

Write-Host ""
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Green
Write-Host "📖 API Documentation will be at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🔗 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
