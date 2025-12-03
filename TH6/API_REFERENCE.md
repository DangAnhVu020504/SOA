# API Reference - TH6 API Gateway

## Base URL

```
http://localhost:5004
```

## Authentication

Tất cả các endpoint (trừ `/health` và routes web) yêu cầu JWT token:

```
Header: Authorization: Bearer <TOKEN>
```

Token mặc định trong `.env`:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

---

## 1. Health Check Endpoints

### Health Status
```http
GET /health
```

**Response (200)**:
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

---

## 2. Web UI Endpoints (No Auth Required)

### Dashboard
```http
GET /
```

### Checkout Page
```http
GET /checkout
```

### Reports Page
```http
GET /reports
```

---

## 3. Product Endpoints

### Get All Products
```http
GET /api/products
```

**Response (200)**:
```json
[
  {
    "id": 1,
    "name": "Laptop Dell XPS 13",
    "description": "Laptop mỏng nhẹ",
    "price": 25000000,
    "quantity": 10,
    "cost": 10000000
  },
  {
    "id": 2,
    "name": "iPhone 14 Pro",
    "description": "Điện thoại cao cấp",
    "price": 30000000,
    "quantity": 15,
    "cost": 12000000
  }
]
```

### Get Product by ID
```http
GET /api/products/:id
```

**Example**:
```
GET /api/products/1
```

**Response (200)**:
```json
{
  "id": 1,
  "name": "Laptop Dell XPS 13",
  "price": 25000000,
  "quantity": 10
}
```

**Response (404)**:
```json
{
  "error": "Product not found"
}
```

---

## 4. Order Endpoints

### Get All Orders
```http
GET /api/orders
```

**Response (200)**:
```json
[
  {
    "id": 1,
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "total_amount": 80000000,
    "status": "completed",
    "created_at": "2024-12-03T10:30:00",
    "updated_at": "2024-12-03T10:35:00",
    "items": [
      {
        "id": 1,
        "order_id": 1,
        "product_id": 1,
        "product_name": "Laptop Dell XPS 13",
        "quantity": 2,
        "unit_price": 25000000,
        "total_price": 50000000
      }
    ]
  }
]
```

### Get Order by ID
```http
GET /api/orders/:id
```

**Example**:
```
GET /api/orders/1
```

**Response (200)**:
```json
{
  "id": 1,
  "customer_name": "Nguyễn Văn A",
  "customer_email": "nguyenvana@example.com",
  "total_amount": 80000000,
  "status": "completed",
  "items": [...]
}
```

### Create Order (Main Workflow)
```http
POST /api/orders
Content-Type: application/json
```

**Request Body**:
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

**Response (201)**:
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
    "items": [...]
  }
}
```

**Automatic Process**:
1. ✅ Kiểm tra tồn kho từ Product Service
2. ✅ Tạo đơn hàng trong Order Service
3. ✅ Thêm order items
4. ✅ Cập nhật số lượng sản phẩm (giảm tồn kho)
5. ✅ Tạo báo cáo trong Report Service

**Error Responses**:

Insufficient stock (400):
```json
{
  "error": "Insufficient stock. Available: 8, Requested: 1000"
}
```

Product not found (400):
```json
{
  "error": "Product not found or error: 404"
}
```

Invalid data (400):
```json
{
  "error": "customer_name is required"
}
```

### Update Order Status
```http
PUT /api/orders/:id
Content-Type: application/json
```

**Example**:
```
PUT /api/orders/1
```

**Request Body**:
```json
{
  "status": "completed"
}
```

**Valid Status Values**:
- `pending` - Chờ xử lý
- `completed` - Hoàn thành (tạo báo cáo tự động)
- `cancelled` - Đã hủy

**Response (200)**:
```json
{
  "success": true,
  "message": "Order status updated to completed",
  "order": {
    "id": 1,
    "customer_name": "Nguyễn Văn A",
    "status": "completed",
    "updated_at": "2024-12-03T10:35:00",
    "items": [...]
  }
}
```

---

## 5. Report Endpoints

### Get All Order Reports
```http
GET /api/reports/orders
```

**Response (200)**:
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
      "created_at": "2024-12-03T10:30:00",
      "updated_at": "2024-12-03T10:30:00"
    }
  ],
  "count": 1
}
```

### Get Order Report by ID
```http
GET /api/reports/orders/:id
```

**Example**:
```
GET /api/reports/orders/1
```

**Response (200)**:
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
        "order_report_id": 1,
        "product_id": 1,
        "total_sold": 2,
        "revenue": 50000000,
        "cost": 20000000,
        "profit": 30000000
      },
      {
        "id": 2,
        "order_report_id": 1,
        "product_id": 2,
        "total_sold": 1,
        "revenue": 30000000,
        "cost": 12000000,
        "profit": 18000000
      }
    ]
  }
}
```

### Create Order Report
```http
POST /api/reports/orders
Content-Type: application/json
```

**Request Body**:
```json
{
  "order_id": 1,
  "total_revenue": 80000000,
  "total_cost": 40000000
}
```

**Response (201)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_id": 1,
    "total_revenue": 80000000,
    "total_cost": 40000000,
    "total_profit": 40000000
  }
}
```

### Get All Product Reports
```http
GET /api/reports/products
```

**Response (200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "order_report_id": 1,
      "product_id": 1,
      "total_sold": 2,
      "revenue": 50000000,
      "cost": 20000000,
      "profit": 30000000,
      "created_at": "2024-12-03T10:30:00"
    },
    {
      "id": 2,
      "order_report_id": 1,
      "product_id": 2,
      "total_sold": 1,
      "revenue": 30000000,
      "cost": 12000000,
      "profit": 18000000,
      "created_at": "2024-12-03T10:30:00"
    }
  ],
  "count": 2
}
```

### Get Product Report by ID
```http
GET /api/reports/products/:id
```

**Example**:
```
GET /api/reports/products/1
```

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_report_id": 1,
    "product_id": 1,
    "total_sold": 2,
    "revenue": 50000000,
    "cost": 20000000,
    "profit": 30000000
  }
}
```

### Create Product Report
```http
POST /api/reports/products
Content-Type: application/json
```

**Request Body**:
```json
{
  "order_report_id": 1,
  "product_id": 1,
  "total_sold": 2,
  "revenue": 50000000,
  "cost": 20000000
}
```

**Response (201)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_report_id": 1,
    "product_id": 1,
    "total_sold": 2,
    "revenue": 50000000,
    "cost": 20000000,
    "profit": 30000000
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "customer_name is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid token"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Endpoint không tồn tại"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Lỗi server nội bộ"
}
```

### 503 Service Unavailable
```json
{
  "error": "Cannot connect to service"
}
```

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Yêu cầu thành công |
| 201 | Created - Tạo mới thành công |
| 400 | Bad Request - Dữ liệu không hợp lệ |
| 401 | Unauthorized - Cần xác thực |
| 403 | Forbidden - Không có quyền |
| 404 | Not Found - Không tìm thấy |
| 500 | Internal Server Error - Lỗi server |
| 503 | Service Unavailable - Dịch vụ không khả dụng |

---

## Request/Response Formats

### Request Headers

```http
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

### Response Headers

```http
Content-Type: application/json
```

---

## cURL Examples

### Get Products
```bash
curl -X GET http://localhost:5004/api/products
```

### Create Order
```bash
curl -X POST http://localhost:5004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Nguyễn Văn A",
    "customer_email": "nguyenvana@example.com",
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'
```

### Update Order Status
```bash
curl -X PUT http://localhost:5004/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Get Reports
```bash
curl -X GET http://localhost:5004/api/reports/orders
curl -X GET http://localhost:5004/api/reports/products
```

---

## Rate Limiting

Hiện tại không có rate limiting. Có thể thêm vào trong tương lai.

---

## Versioning

Hiện tại API không có versioning. Tất cả endpoint ở dạng `/api/*`.

Phiên bản tương lai có thể sử dụng:
- `/api/v1/*`
- `/api/v2/*`

---

## Changelog

### v1.0.0 (2024-12-03)
- ✅ Lần phát hành đầu tiên
- ✅ Hỗ trợ quy trình mua hàng đầy đủ
- ✅ Hỗ trợ báo cáo
- ✅ Giao diện web UI

---

## Documentation Links

- [README.md](README.md) - Tổng quan về dự án
- [INSTALLATION.md](INSTALLATION.md) - Hướng dẫn cài đặt
- [TEST_GUIDE.md](TEST_GUIDE.md) - Hướng dẫn kiểm thử
- [API_REFERENCE.md](API_REFERENCE.md) - Tài liệu này

---

**Phiên bản**: 1.0.0  
**Cập nhật lần cuối**: December 3, 2024  
**Tác giả**: Student
