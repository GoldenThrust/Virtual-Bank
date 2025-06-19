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

# Read environment variables or use defaults
$envFile = ".env"
$apiPort = "8030"
$clientPort = "8040"

if (Test-Path -Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "API_PORT=(.*)") {
            $apiPort = $Matches[1]
        }
        if ($_ -match "CLIENT_PORT=(.*)") {
            $clientPort = $Matches[1]
        }
    }
}

Write-Host "Services started:" -ForegroundColor Green
Write-Host "- API: http://localhost:$apiPort/api/" -ForegroundColor Green
Write-Host "- API Documentation: http://localhost:$apiPort/swagger/" -ForegroundColor Green
Write-Host "- API Admin: http://localhost:$apiPort/admin/" -ForegroundColor Green
Write-Host "- Client Web Interface: http://localhost:$clientPort/" -ForegroundColor Green

Write-Host "`nUse the following command to see service logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f" -ForegroundColor Yellow
