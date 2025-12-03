"""
API Gateway để kết nối các dịch vụ (Product Service, Order Service, Report Service)
Bài thực hành số 6: Kết nối quy trình và kiểm thử các dịch vụ
"""
import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from services.orchestration_service import OrchestrationService
from services.product_service import ProductService
from services.order_service import OrderService
from services.report_service import ReportService

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Khởi tạo các service
orchestration = OrchestrationService()
product_service = ProductService()
order_service = OrderService()
report_service = ReportService()

# ==================== WEB UI ROUTES ====================

@app.route('/')
def index():
    """Trang chủ - Dashboard quản lý quy trình mua hàng"""
    return render_template('index.html')

@app.route('/checkout')
def checkout():
    """Trang checkout - Quy trình mua hàng"""
    return render_template('checkout.html')

@app.route('/reports')
def reports_page():
    """Trang quản lý báo cáo"""
    return render_template('reports.html')

@app.route('/health', methods=['GET'])
def health():
    """Kiểm tra trạng thái các service"""
    return jsonify({
        'status': 'healthy',
        'service': 'API Gateway',
        'services': {
            'product_service': 'http://localhost:5001/health',
            'order_service': 'http://localhost:5002/health',
            'report_service': 'http://localhost:5003/health'
        }
    }), 200


# ==================== PRODUCT ENDPOINTS ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    GET /api/products: Lấy danh sách sản phẩm
    Gọi Product Service: GET /products
    """
    result, status = product_service.get_all_products()
    return jsonify(result), status

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    GET /api/products/{id}: Lấy chi tiết sản phẩm
    Gọi Product Service: GET /products/{id}
    """
    result, status = product_service.get_product(product_id)
    return jsonify(result), status


# ==================== ORDER ORCHESTRATION ENDPOINTS ====================

@app.route('/api/orders', methods=['GET'])
def list_orders():
    """
    GET /api/orders: Lấy danh sách đơn hàng
    Gọi Order Service: GET /orders
    """
    result, status = order_service.list_orders()
    return jsonify(result), status

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    GET /api/orders/{id}: Lấy chi tiết đơn hàng
    Gọi Order Service: GET /orders/{id}
    """
    result, status = order_service.get_order(order_id)
    return jsonify(result), status

@app.route('/api/orders', methods=['POST'])
def create_order():
    """
    POST /api/orders: Tạo đơn hàng mới với quy trình đầy đủ
    
    Request body:
    {
        "customer_name": "Tên khách hàng",
        "customer_email": "email@example.com",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    
    Quy trình:
    1. Kiểm tra tồn kho từ Product Service (GET /products/{id})
    2. Tạo đơn hàng trong Order Service (POST /orders)
    3. Thêm order items (POST /order_items)
    4. Cập nhật số lượng sản phẩm (PUT /products/{id})
    """
    data = request.get_json() or {}
    result, status = orchestration.create_purchase_order(data)
    return jsonify(result), status

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    """
    PUT /api/orders/{id}: Cập nhật trạng thái đơn hàng
    
    Request body:
    {
        "status": "completed"  # pending, completed, cancelled
    }
    
    Khi status = "completed":
    1. Cập nhật status trong Order Service
    2. Tạo báo cáo trong Report Service
    """
    data = request.get_json() or {}
    result, status = orchestration.update_order_status(order_id, data)
    return jsonify(result), status


# ==================== REPORT ENDPOINTS ====================

@app.route('/api/reports/orders', methods=['GET'])
def get_order_reports():
    """
    GET /api/reports/orders: Lấy danh sách báo cáo đơn hàng
    Gọi Report Service: GET /reports/orders
    """
    result, status = report_service.get_all_order_reports()
    return jsonify(result), status

@app.route('/api/reports/orders/<int:report_id>', methods=['GET'])
def get_order_report(report_id):
    """
    GET /api/reports/orders/{id}: Lấy chi tiết báo cáo đơn hàng
    Gọi Report Service: GET /reports/orders/{id}
    """
    result, status = report_service.get_order_report(report_id)
    return jsonify(result), status

@app.route('/api/reports/orders', methods=['POST'])
def create_order_report():
    """
    POST /api/reports/orders: Tạo báo cáo đơn hàng
    
    Request body:
    {
        "order_id": 1,
        "products": [
            {
                "product_id": 1,
                "total_sold": 2,
                "revenue": 100.00,
                "cost": 40.00
            }
        ]
    }
    """
    data = request.get_json() or {}
    result, status = report_service.create_order_report(data)
    return jsonify(result), status

@app.route('/api/reports/products', methods=['GET'])
def get_product_reports():
    """
    GET /api/reports/products: Lấy danh sách báo cáo sản phẩm
    Gọi Report Service: GET /reports/products
    """
    result, status = report_service.get_all_product_reports()
    return jsonify(result), status

@app.route('/api/reports/products/<int:report_id>', methods=['GET'])
def get_product_report(report_id):
    """
    GET /api/reports/products/{id}: Lấy chi tiết báo cáo sản phẩm
    Gọi Report Service: GET /reports/products/{id}
    """
    result, status = report_service.get_product_report(report_id)
    return jsonify(result), status

@app.route('/api/reports/products', methods=['POST'])
def create_product_report():
    """
    POST /api/reports/products: Tạo báo cáo sản phẩm
    
    Request body:
    {
        "order_report_id": 1,
        "product_id": 1,
        "total_sold": 10,
        "revenue": 500.00,
        "cost": 200.00
    }
    """
    data = request.get_json() or {}
    result, status = report_service.create_product_report(data)
    return jsonify(result), status


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint không tồn tại'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Lỗi server nội bộ'
    }), 500


if __name__ == '__main__':
    port = Config.PORT
    app.run(host='0.0.0.0', port=port, debug=True)
