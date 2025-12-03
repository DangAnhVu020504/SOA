# Quick Start Guide - TH6

Bắt đầu nhanh trong 5 phút! 🚀

## Cách 1: Sử Dụng Batch Script (Cách Dễ Nhất - Windows)

### Bước 1: Mở Command Prompt

```bash
cd d:\Flask\TH6
```

### Bước 2: Chạy Script

```bash
run-all-services.bat
```

✅ Tất cả 4 services sẽ khởi động tự động!

### Bước 3: Mở Trình Duyệt

```
http://localhost:5004/
```

Done! ✨

---

## Cách 2: Sử Dụng Bash Script (Linux/Mac)

```bash
cd /path/to/TH6
chmod +x run-all-services.sh
./run-all-services.sh
```

---

## Cách 3: Chạy Thủ Công (Tất Cả OS)

### Terminal 1 - Product Service

```bash
cd d:\Flask\TH6\TH4
pip install -r requirements.txt
python app.py
```

### Terminal 2 - Order Service

```bash
cd d:\Flask\TH6\TH4
python app.py
```

### Terminal 3 - Report Service

```bash
cd d:\Flask\TH6\TH5
python app.py
```

### Terminal 4 - API Gateway

```bash
cd d:\Flask\TH6\TH6
python app.py
```

---

## Cách 4: Sử Dụng VS Code

1. Mở folder `d:\Flask\TH6` trong VS Code
2. Mở file `TH4/app.py`
3. Nhấp nút **Run** (Ctrl+F5)
4. Lặp lại cho TH5/app.py và TH6/app.py

---

## Kiểm Tra Hoạt Động

### Dashboard
```
http://localhost:5004/
```

### Shopping Cart
```
http://localhost:5004/checkout
```

### Reports
```
http://localhost:5004/reports
```

### Health Check (Terminal)
```bash
curl http://localhost:5004/health
```

---

## Quy Trình Test Nhanh

### 1. Xem Sản Phẩm
```bash
curl http://localhost:5004/api/products
```

### 2. Tạo Đơn Hàng
```bash
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test User",
    "customer_email": "test@test.com",
    "items": [{"product_id": 1, "quantity": 1}]
  }'
```

### 3. Xem Báo Cáo
```bash
curl http://localhost:5004/api/reports/orders
```

Done! 🎉

---

## Điều Chỉnh Cấu Hình

### Thay Đổi Port

File `.env` (TH6):
```
PORT=8080
```

File `.env` (TH4):
```
PORT=8081
```

Và tương tự cho TH5.

### Thay Đổi URL Services

File `.env` (TH6):
```
PRODUCT_SERVICE_URL=http://192.168.1.100:5001
ORDER_SERVICE_URL=http://192.168.1.100:5002
REPORT_SERVICE_URL=http://192.168.1.100:5003
```

---

## Khắc Phục Nhanh

| Vấn Đề | Giải Pháp |
|--------|----------|
| Port đã được sử dụng | `netstat -ano \| findstr :5004` rồi `taskkill /PID <PID> /F` |
| Module not found | `pip install -r requirements.txt` |
| Connection refused | Kiểm tra tất cả 4 services đã chạy |
| CORS Error | Cài `pip install flask-cors` |
| Token Error | Kiểm tra `.env` AUTH_TOKEN |

---

## Tài Liệu Chi Tiết

- **README.md** - Tổng quan dự án
- **INSTALLATION.md** - Hướng dẫn cài đặt đầy đủ
- **TEST_GUIDE.md** - Hướng dẫn kiểm thử chi tiết
- **API_REFERENCE.md** - Tài liệu API endpoints

---

## Bước Tiếp Theo

1. ✅ Chạy services
2. 📊 Kiểm thử quy trình mua hàng
3. 🔍 Xem báo cáo
4. 📚 Đọc tài liệu chi tiết
5. 🚀 Tùy chỉnh theo nhu cầu

---

**Chúc bạn thành công!** 🎯

Câu hỏi? Xem file `README.md` hoặc `INSTALLATION.md`
