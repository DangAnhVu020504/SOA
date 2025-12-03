#!/bin/bash
# Script để chạy tất cả các service cùng lúc trên Linux/Mac

echo "====================================================="
echo "  Hệ Thống Bán Hàng - Startup Script"
echo "  Starting all services..."
echo "====================================================="
echo ""

# Kiểm tra xem Python đã cài chưa
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found! Please install Python first."
    echo ""
    echo "macOS: brew install python3"
    echo "Ubuntu: sudo apt-get install python3"
    exit 1
fi

echo "[OK] Python found"
echo ""

# Chuyển đến thư mục TH6 và cài dependencies
echo "Installing dependencies..."
cd "$(dirname "$0")/TH6"
pip3 install -r requirements.txt >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[OK] Dependencies installed"
echo ""

# Khởi động các service trong background
echo "Launching services..."
echo ""

SCRIPT_DIR="$(dirname "$0")"

echo "[1/4] Starting Product Service (Port 5001)..."
cd "$SCRIPT_DIR/TH4"
nohup python3 app.py > /tmp/product-service.log 2>&1 &
sleep 1

echo "[2/4] Starting Order Service (Port 5002)..."
cd "$SCRIPT_DIR/TH4"
nohup python3 app.py > /tmp/order-service.log 2>&1 &
sleep 1

echo "[3/4] Starting Report Service (Port 5003)..."
cd "$SCRIPT_DIR/TH5"
nohup python3 app.py > /tmp/report-service.log 2>&1 &
sleep 1

echo "[4/4] Starting API Gateway (Port 5004)..."
cd "$SCRIPT_DIR/TH6"
nohup python3 app.py > /tmp/api-gateway.log 2>&1 &
sleep 1

echo ""
echo "====================================================="
echo "   Services Started Successfully!"
echo "====================================================="
echo ""
echo "Dashboard:   http://localhost:5004/"
echo "Checkout:    http://localhost:5004/checkout"
echo "Reports:     http://localhost:5004/reports"
echo ""
echo "Health Check:"
echo "   Product Service:  http://localhost:5001/health"
echo "   Order Service:    http://localhost:5002/health"
echo "   Report Service:   http://localhost:5003/health"
echo "   API Gateway:      http://localhost:5004/health"
echo ""
echo "====================================================="
echo ""

# Mở trình duyệt (nếu có)
if command -v open &> /dev/null; then
    open "http://localhost:5004/"
elif command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:5004/"
fi

echo "All services are running!"
echo ""
echo "To stop services:"
echo "  pkill -f 'python3 app.py'"
echo ""
echo "To view logs:"
echo "  tail -f /tmp/product-service.log"
echo "  tail -f /tmp/order-service.log"
echo "  tail -f /tmp/report-service.log"
echo "  tail -f /tmp/api-gateway.log"
echo ""
