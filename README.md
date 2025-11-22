# Dịch vụ Báo cáo (Reporting Service)

Dịch vụ báo cáo độc lập cho hệ thống quản lý đơn hàng và sản phẩm - Bài thực hành số 5

## Mô tả

Dịch vụ báo cáo cung cấp các chức năng thống kê số lượng hàng tồn, hàng bán được, doanh thu, chi phí, lợi nhuận. Báo cáo theo sản phẩm và đơn hàng.

## Cấu trúc Database

### Bảng `orders_reports`
- `id`: INT (PRIMARY KEY) - ID của báo cáo đơn hàng
- `order_id`: INT - ID của đơn hàng
- `total_revenue`: DECIMAL(10, 2) - Tổng doanh thu của đơn hàng
- `total_cost`: DECIMAL(10, 2) - Tổng chi phí nhập sản phẩm trong đơn hàng
- `total_profit`: DECIMAL(10, 2) - Tổng lợi nhuận (total_revenue - total_cost)

### Bảng `product_reports`
- `id`: INT (PRIMARY KEY) - ID của báo cáo sản phẩm
- `order_report_id`: INT - ID đơn hàng (liên kết với bảng orders_reports)
- `product_id`: INT - ID sản phẩm
- `total_sold`: INT - Tổng số lượng sản phẩm đã bán
- `revenue`: DECIMAL(10, 2) - Doanh thu từ sản phẩm
- `cost`: DECIMAL(10, 2) - Chi phí nhập sản phẩm
- `profit`: DECIMAL(10, 2) - Lợi nhuận (revenue - cost)

## Cài đặt

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Tạo database MySQL:**
```bash
mysql -u root -p < database_schema.sql
```

3. **Cấu hình môi trường (tùy chọn):**
Tạo file `.env` hoặc set các biến môi trường:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=reporting_service
MYSQL_PORT=3306
PORT=5003
AUTH_SERVICE_URL=http://localhost:5002
JWT_SECRET_KEY=your-jwt-secret-key
```

4. **Chạy ứng dụng:**
```bash
python app.py
```

Service sẽ chạy tại: `http://localhost:5003`

## API Endpoints

Tất cả các endpoints đều yêu cầu xác thực qua JWT token (từ authentication service - bài TH2).

### Product Reports

- **GET** `/reports/products` - Lấy danh sách tất cả các báo cáo theo sản phẩm
- **GET** `/reports/products/<id>` - Lấy chi tiết báo cáo cho một sản phẩm
- **POST** `/reports/products` - Tạo báo cáo sản phẩm mới
- **DELETE** `/reports/products/<id>` - Xóa báo cáo sản phẩm

### Order Reports

- **GET** `/reports/orders` - Lấy danh sách tất cả các báo cáo theo đơn hàng
- **GET** `/reports/orders/<id>` - Lấy chi tiết báo cáo cho một đơn hàng
- **POST** `/reports/orders` - Tạo báo cáo đơn hàng mới
- **DELETE** `/reports/orders/<id>` - Xóa báo cáo đơn hàng

### Health Check

- **GET** `/health` - Kiểm tra trạng thái service

## Ví dụ sử dụng API

### Tạo báo cáo đơn hàng:
```bash
curl -X POST http://localhost:5003/reports/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "order_id": 1,
    "total_revenue": 1000000.00,
    "total_cost": 600000.00
  }'
```

### Tạo báo cáo sản phẩm:
```bash
curl -X POST http://localhost:5003/reports/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "order_report_id": 1,
    "product_id": 101,
    "total_sold": 10,
    "revenue": 500000.00,
    "cost": 300000.00
  }'
```

### Lấy danh sách báo cáo đơn hàng:
```bash
curl -X GET http://localhost:5003/reports/orders \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Cấu trúc Project

```
TH5/
├── app.py                 # Main application
├── config.py             # Cấu hình
├── models.py             # Database models
├── auth_middleware.py    # Authentication middleware
├── database_schema.sql   # SQL schema
├── requirements.txt      # Dependencies
├── controllers/
│   └── report_controller.py  # Business logic
└── routes/
    └── report_routes.py      # API routes
```

## Lưu ý

- Service hoạt động độc lập trên cổng 5003 (có thể thay đổi qua biến môi trường PORT)
- Xác thực qua JWT token từ authentication service (bài TH2)
- Database MySQL riêng biệt, tuân theo nguyên tắc SOA
- Tự động tính toán profit khi tạo/cập nhật báo cáo

