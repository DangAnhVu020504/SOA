# Hướng Dẫn Kiểm Thử Chi Tiết - Postman & cURL

## Tổng Quan

Tài liệu này hướng dẫn kiểm thử toàn bộ quy trình mua hàng thông qua:
1. Postman (GUI Tool)
2. cURL (Command Line)
3. Web Browser

## Chuẩn Bị

### Bước 1: Khởi Động Các Service

Mở 3 terminal khác nhau và chạy:

```bash
# Terminal 1 - Product Service (TH4)
cd d:\Flask\TH6\TH4
python app.py
# Output: Running on http://0.0.0.0:5001

# Terminal 2 - Order Service (TH4)
cd d:\Flask\TH6\TH4
python app.py
# Output: Running on http://0.0.0.0:5002

# Terminal 3 - Report Service (TH5)
cd d:\Flask\TH6\TH5
python app.py
# Output: Running on http://0.0.0.0:5003

# Terminal 4 - API Gateway (TH6)
cd d:\Flask\TH6\TH6
python app.py
# Output: Running on http://0.0.0.0:5004
```

### Bước 2: Cài Đặt Postman

1. Tải Postman từ: https://www.postman.com/downloads/
2. Cài đặt và mở ứng dụng
3. Tạo New Workspace hoặc Collection

## Kiểm Thử Quy Trình

### Quy Trình Mua Hàng Hoàn Chỉnh

```
┌─────────────────────────────────────────────────────────┐
│         Quy Trình Mua Hàng Bán Hàng Online             │
└─────────────────────────────────────────────────────────┘

Step 1: Khách hàng xem danh sách sản phẩm
        ↓
        GET /api/products
        
Step 2: Khách hàng chọn sản phẩm và tạo đơn hàng
        ↓
        POST /api/orders (tự động: tạo đơn, cập nhật stock, tạo report)
        
Step 3: Xem chi tiết đơn hàng
        ↓
        GET /api/orders/{id}
        
Step 4: Cập nhật trạng thái thanh toán/vận chuyển
        ↓
        PUT /api/orders/{id}
        
Step 5: Xem báo cáo
        ↓
        GET /api/reports/orders
        GET /api/reports/products
```

---

## TEST CASE 1: Kiểm Thử Danh Sách Sản Phẩm

### Postman

1. Nhấp "New" → "HTTP Request"
2. Chọn method: **GET**
3. Nhập URL: `http://localhost:5004/api/products`
4. Nhấp **Send**

Expected Response (200):
```json
[
  {
    "id": 1,
    "name": "Laptop Dell XPS 13",
    "price": 25000000,
    "quantity": 10,
    "description": "Laptop mỏng nhẹ"
  },
  {
    "id": 2,
    "name": "iPhone 14 Pro",
    "price": 30000000,
    "quantity": 15,
    "description": "Điện thoại cao cấp"
  }
]
```

### cURL

```bash
curl -X GET http://localhost:5004/api/products
```

### Web Browser

Mở: `http://localhost:5004/` → Nhấp "Xem Sản Phẩm"

---

## TEST CASE 2: Tạo Đơn Hàng (QUY TRÌNH CHÍNH)

### Postman

1. Nhấp "New" → "HTTP Request"
2. Chọn method: **POST**
3. Nhập URL: `http://localhost:5004/api/orders`
4. Tab "Headers" → Thêm:
   - Key: `Content-Type`
   - Value: `application/json`
5. Tab "Body" → Chọn "raw" → "JSON"
6. Nhập:

```json
{
  "customer_name": "Nguyễn Văn A",
  "customer_email": "nguyenvana@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}
```

7. Nhấp **Send**

Expected Response (201):
```json
{
  "success": true,
  "message": "Purchase order created successfully",
  "order_id": 1,
  "order": {
    "id": 1,
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "total_amount": 80000000,
    "status": "pending",
    "created_at": "2024-12-03T10:30:00",
    "items": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "Laptop Dell XPS 13",
        "quantity": 2,
        "unit_price": 25000000,
        "total_price": 50000000
      },
      {
        "id": 2,
        "product_id": 2,
        "product_name": "iPhone 14 Pro",
        "quantity": 1,
        "unit_price": 30000000,
        "total_price": 30000000
      }
    ]
  }
}
```

**Ghi chú order_id = 1 để dùng sau**

### cURL

```bash
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ]
  }'
```

### Web Browser

1. Mở: `http://localhost:5004/checkout`
2. Chọn sản phẩm → Nhập số lượng → "Thêm vào giỏ"
3. Điền thông tin:
   - Tên: Nguyễn Văn A
   - Email: nguyenvana@example.com
4. Nhấp "Đặt Hàng"

---

## TEST CASE 3: Lấy Chi Tiết Đơn Hàng

### Postman

1. Method: **GET**
2. URL: `http://localhost:5004/api/orders/1`
3. Nhấp **Send**

Expected Response (200):
```json
{
  "id": 1,
  "customer_name": "Nguyễn Văn A",
  "customer_email": "nguyenvana@example.com",
  "total_amount": 80000000,
  "status": "pending",
  "created_at": "2024-12-03T10:30:00",
  "items": [...]
}
```

### cURL

```bash
curl -X GET http://localhost:5004/api/orders/1
```

---

## TEST CASE 4: Cập Nhật Trạng Thái Đơn Hàng (Hoàn Thành Thanh Toán)

### Postman

1. Method: **PUT**
2. URL: `http://localhost:5004/api/orders/1`
3. Headers:
   - Key: `Content-Type`
   - Value: `application/json`
4. Body (JSON):

```json
{
  "status": "completed"
}
```

5. Nhấp **Send**

Expected Response (200):
```json
{
  "success": true,
  "message": "Order status updated to completed",
  "order": {
    "id": 1,
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "total_amount": 80000000,
    "status": "completed",
    "updated_at": "2024-12-03T10:35:00",
    "items": [...]
  }
}
```

### cURL

```bash
curl -X PUT http://localhost:5004/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

## TEST CASE 5: Lấy Danh Sách Đơn Hàng

### Postman

1. Method: **GET**
2. URL: `http://localhost:5004/api/orders`
3. Nhấp **Send**

Expected Response (200):
```json
[
  {
    "id": 1,
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "total_amount": 80000000,
    "status": "completed",
    "items": [...]
  }
]
```

### cURL

```bash
curl -X GET http://localhost:5004/api/orders
```

---

## TEST CASE 6: Lấy Báo Cáo Đơn Hàng

### Postman

1. Method: **GET**
2. URL: `http://localhost:5004/api/reports/orders`
3. Nhấp **Send**

Expected Response (200):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "order_id": 1,
      "total_revenue": 80000000,
      "total_cost": 40000000,
      "total_profit": 40000000,
      "product_reports": [
        {
          "id": 1,
          "product_id": 1,
          "total_sold": 2,
          "revenue": 50000000,
          "cost": 20000000,
          "profit": 30000000
        }
      ]
    }
  ]
}
```

### cURL

```bash
curl -X GET http://localhost:5004/api/reports/orders
```

---

## TEST CASE 7: Lấy Báo Cáo Sản Phẩm

### Postman

1. Method: **GET**
2. URL: `http://localhost:5004/api/reports/products`
3. Nhấp **Send**

Expected Response (200):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "product_id": 1,
      "total_sold": 2,
      "revenue": 50000000,
      "cost": 20000000,
      "profit": 30000000,
      "created_at": "2024-12-03T10:30:00"
    },
    {
      "id": 2,
      "product_id": 2,
      "total_sold": 1,
      "revenue": 30000000,
      "cost": 12000000,
      "profit": 18000000,
      "created_at": "2024-12-03T10:30:00"
    }
  ]
}
```

### cURL

```bash
curl -X GET http://localhost:5004/api/reports/products
```

---

## TEST CASE 8: Tạo Đơn Hàng Thứ 2 (Test Múltiple Orders)

### Postman

1. Method: **POST**
2. URL: `http://localhost:5004/api/orders`
3. Body:

```json
{
  "customer_name": "Trần Thị B",
  "customer_email": "tranthib@example.com",
  "items": [
    {
      "product_id": 2,
      "quantity": 3
    }
  ]
}
```

Expected Response (201):
```json
{
  "success": true,
  "order_id": 2,
  "order": {
    "id": 2,
    "customer_name": "Trần Thị B",
    "customer_email": "tranthib@example.com",
    "total_amount": 90000000,
    "status": "pending"
  }
}
```

### cURL

```bash
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Trần Thị B",
    "customer_email": "tranthib@example.com",
    "items": [
      {"product_id": 2, "quantity": 3}
    ]
  }'
```

---

## TEST CASE 9: Lấy Báo Cáo Chi Tiết Đơn Hàng

### Postman

1. Method: **GET**
2. URL: `http://localhost:5004/api/reports/orders/1`
3. Nhấp **Send**

Expected Response (200):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_id": 1,
    "total_revenue": 80000000,
    "total_cost": 40000000,
    "total_profit": 40000000,
    "product_reports": [
      {
        "id": 1,
        "product_id": 1,
        "total_sold": 2,
        "revenue": 50000000,
        "cost": 20000000,
        "profit": 30000000
      }
    ]
  }
}
```

### cURL

```bash
curl -X GET http://localhost:5004/api/reports/orders/1
```

---

## TEST CASE 10: Lấy Báo Cáo Chi Tiết Sản Phẩm

### Postman

1. Method: **GET**
2. URL: `http://localhost:5004/api/reports/products/1`
3. Nhấp **Send**

Expected Response (200):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "product_id": 1,
    "total_sold": 2,
    "revenue": 50000000,
    "cost": 20000000,
    "profit": 30000000
  }
}
```

### cURL

```bash
curl -X GET http://localhost:5004/api/reports/products/1
```

---

## Kiểm Thử Error Handling

### TEST CASE 11: Lỗi - Không Đủ Hàng

### Postman

1. Method: **POST**
2. URL: `http://localhost:5004/api/orders`
3. Body:

```json
{
  "customer_name": "Lê Văn C",
  "customer_email": "levanc@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 1000
    }
  ]
}
```

Expected Response (400):
```json
{
  "error": "Insufficient stock. Available: 8, Requested: 1000"
}
```

### TEST CASE 12: Lỗi - Sản Phẩm Không Tồn Tại

### Postman

1. Method: **POST**
2. URL: `http://localhost:5004/api/orders`
3. Body:

```json
{
  "customer_name": "Phạm Văn D",
  "customer_email": "phamvand@example.com",
  "items": [
    {
      "product_id": 99999,
      "quantity": 1
    }
  ]
}
```

Expected Response (400):
```json
{
  "error": "Product not found or error: 404"
}
```

### TEST CASE 13: Lỗi - Dữ Liệu Không Hợp Lệ

### Postman

1. Method: **POST**
2. URL: `http://localhost:5004/api/orders`
3. Body:

```json
{
  "customer_name": "",
  "customer_email": "test@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```

Expected Response (400):
```json
{
  "error": "customer_name is required"
}
```

---

## Ghi Chú Quan Trọng

### 1. **Quy Trình Tự Động**

Khi tạo đơn hàng, API Gateway tự động:

1. ✅ Gọi Product Service để kiểm tra tồn kho
2. ✅ Gọi Order Service để tạo đơn hàng
3. ✅ Gọi Order Service để thêm order items
4. ✅ Gọi Product Service để cập nhật tồn kho (giảm)
5. ✅ Gọi Report Service để tạo báo cáo tự động

### 2. **Kiểm Tra Tồn Kho**

Sau khi tạo đơn hàng, hãy kiểm tra lại danh sách sản phẩm:

```bash
GET http://localhost:5004/api/products
```

Bạn sẽ thấy số lượng đã giảm.

### 3. **Cập Nhật Trạng Thái**

Khi cập nhật trạng thái thành "completed", báo cáo sẽ được tạo tự động.

### 4. **Loại Trạng Thái**

```
pending    = Chờ xử lý
completed  = Hoàn thành
cancelled  = Đã hủy
```

---

## Postman Collection (Export/Import)

### Xuất Collection

1. Chọn Collection → "..." → "Export"
2. Chọn format: "Collection v2.1"
3. Lưu file

### Nhập Collection

1. Nhấp "Import" 
2. Chọn file `.json`
3. Collection được nhập

---

## Tính Năng Thêm

### 1. **Xem Health Check**

```bash
GET http://localhost:5004/health
```

Response:
```json
{
  "status": "healthy",
  "service": "API Gateway",
  "services": {
    "product_service": "http://localhost:5001/health",
    "order_service": "http://localhost:5002/health",
    "report_service": "http://localhost:5003/health"
  }
}
```

### 2. **Xem Logs**

Kiểm tra Terminal nơi chạy Flask app để xem logs.

### 3. **Database**

Kiểm tra database tương ứng:
- TH4: `order_management.db`
- TH5: `reporting_service.db`

---

## Tóm Tắt Lệnh cURL

```bash
# 1. Xem sản phẩm
curl http://localhost:5004/api/products

# 2. Tạo đơn hàng
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"A","customer_email":"a@test.com","items":[{"product_id":1,"quantity":2}]}'

# 3. Xem đơn hàng
curl http://localhost:5004/api/orders

# 4. Xem chi tiết đơn hàng
curl http://localhost:5004/api/orders/1

# 5. Cập nhật trạng thái
curl -X PUT http://localhost:5004/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# 6. Xem báo cáo đơn hàng
curl http://localhost:5004/api/reports/orders

# 7. Xem báo cáo sản phẩm
curl http://localhost:5004/api/reports/products

# 8. Xem báo cáo chi tiết đơn hàng
curl http://localhost:5004/api/reports/orders/1

# 9. Xem báo cáo chi tiết sản phẩm
curl http://localhost:5004/api/reports/products/1

# 10. Health check
curl http://localhost:5004/health
```

---

## Hỗ Trợ

Nếu gặp vấn đề:

1. Kiểm tra tất cả 4 service đã chạy
2. Kiểm tra port không bị chiếm dụng
3. Kiểm tra token authentication
4. Xem logs trong Terminal
5. Kiểm tra database tồn tại

---

**Chúc bạn kiểm thử thành công!** 🎉
