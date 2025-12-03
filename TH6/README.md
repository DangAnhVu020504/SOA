# TH6 - Kết Nối Quy Trình và Kiểm Thử Các Dịch Vụ

## Mô Tả

TH6 là một API Gateway được thiết kế để điều phối (orchestrate) các quy trình bán hàng giữa các dịch vụ microservice đã phát triển ở các bài thực hành trước:

- **TH3/TH4**: Dịch vụ quản lý sản phẩm (Product Service) - Port 5001
- **TH4**: Dịch vụ quản lý đơn hàng (Order Service) - Port 5002
- **TH5**: Dịch vụ báo cáo (Reporting Service) - Port 5003

**TH6** chạy trên **Port 5004** và cung cấp:
1. API Gateway để gọi các dịch vụ khác
2. Giao diện web thân thiện cho người dùng
3. Quy trình mua hàng hoàn chỉnh: chọn sản phẩm → thêm giỏ hàng → thanh toán → tạo báo cáo

## Cấu Trúc Thư Mục

```
TH6/
├── .env                          # Cấu hình biến môi trường
├── requirements.txt              # Dependencies
├── config.py                     # Cấu hình Flask
├── app.py                        # Main Flask application
├── services/                     # Các service modules
│   ├── __init__.py
│   ├── base_service.py          # Lớp cơ sở cho HTTP requests
│   ├── product_service.py       # Gọi Product Service
│   ├── order_service.py         # Gọi Order Service
│   ├── report_service.py        # Gọi Report Service
│   └── orchestration_service.py # Điều phối quy trình mua hàng
├── static/
│   ├── css/
│   │   └── style.css           # Styling cho web UI
│   └── js/
│       ├── app.js              # Dashboard scripts
│       ├── checkout.js         # Shopping cart scripts
│       └── reports.js          # Reports page scripts
└── templates/
    ├── index.html              # Dashboard page
    ├── checkout.html           # Shopping cart & checkout page
    └── reports.html            # Reports page
```

## Cài Đặt

### 1. Cài Đặt Dependencies

```bash
cd d:\Flask\TH6\TH6
pip install -r requirements.txt
```

### 2. Cấu Hình .env

File `.env` đã được tạo với các giá trị mặc định:

```
PORT=5004
PRODUCT_SERVICE_URL=http://localhost:5001
ORDER_SERVICE_URL=http://localhost:5002
REPORT_SERVICE_URL=http://localhost:5003
AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Lưu ý**: Cần điều chỉnh `AUTH_TOKEN` để khớp với token trong TH4 và TH5.

## Chạy Ứng Dụng

### Cách 1: Chạy từ Terminal

```bash
# Terminal 1 - TH4 (Order Service)
cd d:\Flask\TH6\TH4
python app.py

# Terminal 2 - TH5 (Report Service)
cd d:\Flask\TH6\TH5
python app.py

# Terminal 3 - TH6 (API Gateway)
cd d:\Flask\TH6\TH6
python app.py
```

### Cách 2: Chạy từ VS Code

1. Mở TH4/app.py → Chọn "Run" hoặc Ctrl+F5
2. Mở TH5/app.py → Chọn "Run" hoặc Ctrl+F5
3. Mở TH6/app.py → Chọn "Run" hoặc Ctrl+F5

## API Endpoints

### 1. Lấy Danh Sách Sản Phẩm

```
GET http://localhost:5004/api/products
```

Response:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "price": 15000000,
    "quantity": 10,
    "description": "Laptop mạnh mẽ"
  }
]
```

### 2. Tạo Đơn Hàng (Quy Trình Chính)

```
POST http://localhost:5004/api/orders
Content-Type: application/json

{
  "customer_name": "Nguyễn Văn A",
  "customer_email": "nguyenvana@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

**Quy Trình Tự Động**:
1. ✅ Kiểm tra tồn kho sản phẩm từ Product Service
2. ✅ Tạo đơn hàng trong Order Service
3. ✅ Thêm order items
4. ✅ Cập nhật số lượng sản phẩm (giảm tồn kho)
5. ✅ Tạo báo cáo trong Report Service

Response:
```json
{
  "success": true,
  "message": "Purchase order created successfully",
  "order_id": 1,
  "order": {
    "id": 1,
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "total_amount": 30000000,
    "status": "pending",
    "items": [...]
  }
}
```

### 3. Cập Nhật Trạng Thái Đơn Hàng

```
PUT http://localhost:5004/api/orders/:id
Content-Type: application/json

{
  "status": "completed"
}
```

**Statuses**: `pending`, `completed`, `cancelled`

### 4. Lấy Danh Sách Báo Cáo Đơn Hàng

```
GET http://localhost:5004/api/reports/orders
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "order_id": 1,
      "total_revenue": 30000000,
      "total_cost": 12000000,
      "total_profit": 18000000,
      "product_reports": [...]
    }
  ]
}
```

### 5. Lấy Danh Sách Báo Cáo Sản Phẩm

```
GET http://localhost:5004/api/reports/products
```

## Kiểm Thử Quy Trình

### Sử Dụng Web UI (Dễ Nhất)

1. Mở trình duyệt: **http://localhost:5004/**
2. Nhấp "Mua Hàng" để vào trang checkout
3. Chọn sản phẩm → Nhập số lượng → Thêm vào giỏ
4. Điền thông tin khách hàng
5. Nhấp "Đặt Hàng"
6. Xem kết quả ngay tức thì

### Sử Dụng Postman

#### Step 1: Lấy Danh Sách Sản Phẩm

```
GET http://localhost:5004/api/products
```

Ghi chú lại `product_id` và `price`.

#### Step 2: Tạo Đơn Hàng

```
POST http://localhost:5004/api/orders
Body (JSON):
{
  "customer_name": "Trần Thị B",
  "customer_email": "tranthib@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 3
    }
  ]
}
```

Ghi chú lại `order_id`.

#### Step 3: Cập Nhật Trạng Thái Đơn Hàng

```
PUT http://localhost:5004/api/orders/:id
Body (JSON):
{
  "status": "completed"
}
```

#### Step 4: Xem Báo Cáo Đơn Hàng

```
GET http://localhost:5004/api/reports/orders
```

#### Step 5: Xem Báo Cáo Sản Phẩm

```
GET http://localhost:5004/api/reports/products
```

### Sử Dụng cURL (Command Line)

```bash
# 1. Lấy sản phẩm
curl -X GET http://localhost:5004/api/products

# 2. Tạo đơn hàng
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Lê Văn C",
    "customer_email": "levanc@example.com",
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'

# 3. Cập nhật trạng thái
curl -X PUT http://localhost:5004/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# 4. Xem báo cáo
curl -X GET http://localhost:5004/api/reports/orders
curl -X GET http://localhost:5004/api/reports/products
```

## Các Tính Năng Chính

### 1. **Giao Diện Dashboard** (/)
- Xem danh sách sản phẩm
- Xem đơn hàng
- Xem báo cáo

### 2. **Trang Mua Hàng** (/checkout)
- Chọn sản phẩm từ danh sách
- Thêm vào giỏ hàng
- Quản lý số lượng
- Điền thông tin khách hàng
- Xem lại trước khi đặt hàng

### 3. **Trang Báo Cáo** (/reports)
- Báo cáo đơn hàng (doanh thu, chi phí, lợi nhuận)
- Báo cáo sản phẩm (số bán, doanh thu, lợi nhuận)
- Xem chi tiết báo cáo
- Cập nhật trạng thái đơn hàng

## Xử Lý Lỗi

### Kết Nối Dịch Vụ Thất Bại

Nếu nhận được lỗi "Cannot connect to service":

1. Kiểm tra các dịch vụ đã chạy chưa:
   - Port 5001: Product Service
   - Port 5002: Order Service
   - Port 5003: Report Service

2. Kiểm tra URL trong `.env` có đúng không

3. Kiểm tra token authentication trong `.env`

### Token Không Hợp Lệ

Nếu nhận được lỗi 401/403:

1. Kiểm tra `AUTH_TOKEN` trong `.env`
2. Đảm bảo token khớp giữa TH4, TH5, TH6
3. Tạo token JWT mới nếu cần

## Tính Năng Nâng Cao

### 1. **Xác Thực JWT**
Tất cả các request đến các service khác đều sử dụng JWT token từ header `Authorization: Bearer <token>`

### 2. **Điều Phối Quy Trình**
`OrchestrationService` tự động:
- Kiểm tra tồn kho
- Tạo đơn hàng
- Cập nhật tồn kho
- Tạo báo cáo

### 3. **Xử Lý Lỗi Toàn Cục**
- Kiểm tra lỗi kết nối
- Timeout handling
- Response validation

## Khắc Phục Sự Cố

### Vấn đề: Port đã được sử dụng

```bash
# Tìm process sử dụng port
netstat -ano | findstr :5004

# Kill process (Windows)
taskkill /PID <PID> /F
```

### Vấn đề: Module không tìm thấy

```bash
pip install -r requirements.txt
```

### Vấn đề: CORS Error

Đảm bảo `flask-cors` đã được cài đặt:

```bash
pip install flask-cors
```

## Tiếp Theo

1. Thêm cơ sở dữ liệu cho caching
2. Thêm authentication/authorization cho web UI
3. Thêm payment gateway integration
4. Thêm email notifications
5. Thêm logging và monitoring

## Tham Khảo

- Flask Documentation: https://flask.palletsprojects.com/
- RESTful API Design: https://restfulapi.net/
- JWT Authentication: https://jwt.io/

---

**Tác Giả**: Student  
**Ngày Tạo**: December 2024  
**Phiên Bản**: 1.0.0
