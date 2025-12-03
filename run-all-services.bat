@echo off
REM Script để chạy tất cả các service cùng lúc trên Windows
REM Cách sử dụng: Chạy file này từ Command Prompt hoặc PowerShell

color 0A
echo =====================================================
echo   Hệ Thống Bán Hàng - Startup Script
echo   Starting all services...
echo =====================================================
echo.

REM Kiểm tra xem Python đã cài chưa
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python first.
    echo.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Kiểm tra xem các thư mục tồn tại không
if not exist "d:\Flask\TH6\TH4\app.py" (
    echo [ERROR] TH4 folder not found at d:\Flask\TH6\TH4
    pause
    exit /b 1
)

if not exist "d:\Flask\TH6\TH5\app.py" (
    echo [ERROR] TH5 folder not found at d:\Flask\TH6\TH5
    pause
    exit /b 1
)

if not exist "d:\Flask\TH6\TH6\app.py" (
    echo [ERROR] TH6 folder not found at d:\Flask\TH6\TH6
    pause
    exit /b 1
)

echo [OK] All folders found
echo.

REM Kiểm tra dependencies
echo Checking dependencies...
cd d:\Flask\TH6\TH6
pip install -r requirements.txt >nul 2>&1

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Khởi động các service
echo Launching services...
echo.

echo [1/4] Starting Product Service (Port 5001)...
cd d:\Flask\TH6\TH4
start "Product Service (5001)" python app.py
timeout /t 2 >nul

echo [2/4] Starting Order Service (Port 5002)...
cd d:\Flask\TH6\TH4
start "Order Service (5002)" python app.py
timeout /t 2 >nul

echo [3/4] Starting Report Service (Port 5003)...
cd d:\Flask\TH6\TH5
start "Report Service (5003)" python app.py
timeout /t 2 >nul

echo [4/4] Starting API Gateway (Port 5004)...
cd d:\Flask\TH6\TH6
start "API Gateway (5004)" python app.py
timeout /t 2 >nul

echo.
echo =====================================================
echo   Services Started Successfully!
echo =====================================================
echo.
echo Dashboard:   http://localhost:5004/
echo Checkout:    http://localhost:5004/checkout
echo Reports:    http://localhost:5004/reports
echo.
echo Health Check:
echo   Product Service:  http://localhost:5001/health
echo   Order Service:    http://localhost:5002/health
echo   Report Service:   http://localhost:5003/health
echo   API Gateway:      http://localhost:5004/health
echo.
echo =====================================================
echo.

REM Mở trình duyệt
echo Opening dashboard in browser...
start http://localhost:5004/

echo.
echo All services are running!
echo Press Ctrl+C in the terminal windows to stop services.
echo.
pause
