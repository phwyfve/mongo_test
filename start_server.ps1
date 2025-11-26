Write-Host "Starting FastAPI MongoDB Authentication Server..." -ForegroundColor Green
Write-Host ""
Write-Host "Make sure MongoDB is running before starting the server." -ForegroundColor Yellow
Write-Host ""
Write-Host "The server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation will be available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
