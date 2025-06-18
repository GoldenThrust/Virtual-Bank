# PowerShell script to start Virtual Bank services

# Check if .env file exists, if not create from example
if (-not (Test-Path -Path ".env")) {
    if (Test-Path -Path ".env.example") {
        Write-Host "Creating .env from .env.example..." -ForegroundColor Green
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "Please update the .env file with your configuration" -ForegroundColor Yellow
    }
    else {
        Write-Host "ERROR: .env.example file not found. Please create a .env file manually." -ForegroundColor Red
        exit 1
    }
}

# Start all services
Write-Host "Starting Virtual Bank API and Client application..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "Services started:" -ForegroundColor Green
Write-Host "- API: http://localhost:8030/api/" -ForegroundColor Green
Write-Host "- API Documentation: http://localhost:8030/swagger/" -ForegroundColor Green
Write-Host "- API Admin: http://localhost:8030/admin/" -ForegroundColor Green
Write-Host "- Client Web Interface: http://localhost:8040/" -ForegroundColor Green

Write-Host "`nUse the following command to see service logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f" -ForegroundColor Yellow
