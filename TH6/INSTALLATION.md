# Hướng Dẫn Cài Đặt Chi Tiết - TH6

## Yêu Cầu Hệ Thống

- **OS**: Windows 10/11 hoặc Linux/Mac
- **Python**: 3.8 hoặc cao hơn
- **Port Trống**: 5001, 5002, 5003, 5004
- **RAM**: Tối thiểu 2GB
- **Ổ cứng**: 500MB trống

## Bước 1: Kiểm Tra Cài Đặt Python

### Windows

Mở PowerShell và chạy:

```powershell
python --version
```

Output mong muốn:
```
Python 3.8.0 hoặc cao hơn
```

Nếu không có Python:
1. Tải từ: https://www.python.org/downloads/
2. Cài đặt (chọn "Add Python to PATH")
3. Khởi động lại terminal

### Linux/Mac

```bash
python3 --version
```

## Bước 2: Cài Đặt Dependencies

### Windows (PowerShell)

```powershell
# Chuyển đến thư mục TH6
cd d:\Flask\TH6\TH6

# Cài đặt dependencies
pip install -r requirements.txt
```

### Linux/Mac

```bash
cd /path/to/TH6

# Tạo virtual environment (optional nhưng khuyến khích)
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Kiểm Tra Cài Đặt

```bash
pip list
```

Bạn sẽ thấy:
```
Flask==3.0.0
flask-cors==4.0.0
requests==2.32.3
python-dotenv==1.0.1
```

## Bước 3: Cấu Hình .env

File `.env` đã có sẵn. Kiểm tra nội dung:

```bash
# Windows
type .env

# Linux/Mac
cat .env
```

Nội dung mong muốn:
```
PORT=5004
PRODUCT_SERVICE_URL=http://localhost:5001
ORDER_SERVICE_URL=http://localhost:5002
REPORT_SERVICE_URL=http://localhost:5003
AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Lưu ý**: Nếu các service chạy trên máy khác:
- Sửa `localhost` thành IP của máy đó
- Ví dụ: `http://192.168.1.100:5001`

## Bước 4: Kiểm Tra Kết Nối Internet

```bash
# Kiểm tra kết nối
ping http://localhost:5001
ping http://localhost:5002
ping http://localhost:5003
```

## Bước 5: Khởi Động Các Service

### Phương Pháp 1: Từ Terminal (Khuyến Khích)

Mở **4 terminal khác nhau**:

#### Terminal 1 - Product Service (Port 5001)

```powershell
cd d:\Flask\TH6\TH4
python app.py
```

Chờ khi thấy:
```
Running on http://0.0.0.0:5001 (Press CTRL+C to quit)
```

#### Terminal 2 - Order Service (Port 5002)

```powershell
cd d:\Flask\TH6\TH4
# Lưu ý: Cùng thư mục TH4, nhưng cấu hình khác (xem app.py)
python app.py
```

#### Terminal 3 - Report Service (Port 5003)

```powershell
cd d:\Flask\TH6\TH5
python app.py
```

#### Terminal 4 - API Gateway (Port 5004)

```powershell
cd d:\Flask\TH6\TH6
python app.py
```

### Phương Pháp 2: Từ VS Code

1. Mở file `app.py` tương ứng
2. Nhấp nút **Run** hoặc Ctrl+F5
3. Hoặc sử dụng Debug (F5)

### Phương Pháp 3: Từ Command Prompt (Windows)

```batch
@echo off
cd d:\Flask\TH6\TH4
start "Product Service" python app.py

cd d:\Flask\TH6\TH4
start "Order Service" python app.py

cd d:\Flask\TH6\TH5
start "Report Service" python app.py

cd d:\Flask\TH6\TH6
start "API Gateway" python app.py
```

Lưu thành file `run-all.bat` và chạy.

## Bước 6: Kiểm Tra Services Đã Chạy

Mở terminal mới (hoặc PowerShell tab mới):

```bash
# Kiểm tra Product Service
curl http://localhost:5001/health

# Kiểm tra Order Service
curl http://localhost:5002/health

# Kiểm tra Report Service
curl http://localhost:5003/health

# Kiểm tra API Gateway
curl http://localhost:5004/health
```

Nếu tất cả return `200`, chúc mừng! 🎉

## Bước 7: Truy Cập Giao Diện Web

Mở trình duyệt:

### Dashboard
```
http://localhost:5004/
```

### Shopping Cart (Mua Hàng)
```
http://localhost:5004/checkout
```

### Reports (Báo Cáo)
```
http://localhost:5004/reports
```

## Bước 8: Kiểm Thử Quy Trình

Xem chi tiết tại `TEST_GUIDE.md`:

```bash
# Xem sản phẩm
curl http://localhost:5004/api/products

# Tạo đơn hàng
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Test","customer_email":"test@test.com","items":[{"product_id":1,"quantity":1}]}'

# Xem báo cáo
curl http://localhost:5004/api/reports/orders
```

---

## Khắc Phục Sự Cố

### Vấn Đề 1: "Port already in use"

**Nguyên nhân**: Có ứng dụng khác chiếm port

**Giải pháp**:

```powershell
# Tìm process sử dụng port
netstat -ano | findstr :5004

# Kill process (thay PID bằng ID thực tế)
taskkill /PID 1234 /F
```

### Vấn Đề 2: "Module not found"

**Nguyên nhân**: Dependencies không được cài

**Giải pháp**:

```bash
pip install -r requirements.txt
```

### Vấn Đề 3: "Connection refused"

**Nguyên nhân**: Service không chạy hoặc port sai

**Giải pháp**:
1. Kiểm tra tất cả 4 terminal có chạy không
2. Kiểm tra .env có đúng port không
3. Kiểm tra không có firewall chặn

### Vấn Đề 4: "CORS Error"

**Nguyên nhân**: flask-cors không cài

**Giải pháp**:

```bash
pip install flask-cors
```

### Vấn Đề 5: "Authentication Error (401/403)"

**Nguyên nhân**: Token không khớp

**Giải pháp**:
1. Kiểm tra AUTH_TOKEN trong `.env`
2. Đảm bảo token giống nhau ở TH4, TH5, TH6
3. Kiểm tra token header format: `Authorization: Bearer <token>`

### Vấn Đề 6: Database "already locked"

**Nguyên nhân**: Database đang được truy cập bởi process khác

**Giải pháp**:

```bash
# Kill all Python processes (cách cuối cùng)
taskkill /IM python.exe /F

# Xóa file lock
del *.db-journal
```

---

## Cấu Hình Nâng Cao

### 1. Sử Dụng Virtual Environment (Linux/Mac)

```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Tắt
deactivate
```

### 2. Sửa PORT

File `.env`:
```
PORT=8080
```

File `app.py` dòng cuối:
```python
port = Config.PORT
```

### 3. Debug Mode

File `.env`:
```
DEBUG=True
```

File `app.py`:
```python
app.run(debug=True)
```

### 4. Production Deployment

Cài Gunicorn:

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5004 app:app
```

---

## Máy Chủ Chạy Trên Máy Khác

Nếu các service chạy trên máy khác (192.168.1.100):

File `.env`:
```
PRODUCT_SERVICE_URL=http://192.168.1.100:5001
ORDER_SERVICE_URL=http://192.168.1.100:5002
REPORT_SERVICE_URL=http://192.168.1.100:5003
```

Chạy TH6 trên máy hiện tại:

```bash
python app.py
```

Truy cập từ máy khác:

```
http://<IP_Máy_Này>:5004
```

---

## Database

### Tạo Database Tự Động

Flask-SQLAlchemy tự tạo database khi app chạy:

```python
# app.py dòng cuối
with app.app_context():
    db.create_all()
```

Database files:
- TH4: `order_management.db`
- TH5: `reporting_service.db`
- TH6: Không có (chỉ là Gateway)

### Xóa Database Để Reset

```bash
# Windows
del *.db

# Linux/Mac
rm *.db
```

Restart app để tạo database mới.

---

## Monitoring

### Xem Logs Real-time

Logs hiển thị trong terminal nơi chạy Flask:

```
127.0.0.1 - - [03/Dec/2024 10:30:00] "GET /api/products HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2024 10:31:00] "POST /api/orders HTTP/1.1" 201 -
```

### Tăng Mức Debug

File `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Backup & Restore

### Backup Database

```bash
# Tạo thư mục backup
mkdir backup

# Copy database
cp *.db backup/
```

### Restore Database

```bash
# Copy từ backup
cp backup/*.db .
```

---

## Dừng Services

### Cách 1: Ctrl+C trong Terminal

```
Press Ctrl+C to quit
```

### Cách 2: Kill Process

```bash
# Tìm PID
netstat -ano | findstr :5004

# Kill
taskkill /PID 1234 /F
```

### Cách 3: Python Script

```python
import os
import signal

# Kill all Flask processes
os.system('taskkill /IM python.exe /F')
```

---

## Tóm Tắt Nhanh

```bash
# 1. Cài dependencies (lần đầu)
pip install -r requirements.txt

# 2. Terminal 1 - TH4 (Product Service)
cd d:\Flask\TH6\TH4 && python app.py

# 3. Terminal 2 - TH4 (Order Service)
cd d:\Flask\TH6\TH4 && python app.py

# 4. Terminal 3 - TH5 (Report Service)
cd d:\Flask\TH6\TH5 && python app.py

# 5. Terminal 4 - TH6 (API Gateway)
cd d:\Flask\TH6\TH6 && python app.py

# 6. Mở trình duyệt
http://localhost:5004

# 7. Kiểm thử quy trình
# Xem TEST_GUIDE.md
```

---

## Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề:

1. Kiểm tra README.md
2. Kiểm tra TEST_GUIDE.md
3. Xem logs trong Terminal
4. Kiểm tra firewall/antivirus
5. Thử reset: xóa database và restart

---

**Chúc mừng bạn đã cài đặt thành công!** 🚀

Bước tiếp theo:
- Đọc `README.md` để hiểu kiến trúc
- Xem `TEST_GUIDE.md` để kiểm thử
- Khám phá giao diện web tại `http://localhost:5004`
