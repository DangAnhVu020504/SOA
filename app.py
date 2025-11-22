"""
Flask Application cho dịch vụ báo cáo (Reporting Service)
Bài thực hành số 5
"""
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import Config
from models import db
from routes.report_routes import report_bp

def create_app():
    """Tạo và cấu hình Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Khởi tạo database
    db.init_app(app)
    
    # Đăng ký Blueprints
    app.register_blueprint(report_bp)
    
    # Web UI Routes
    @app.route('/')
    def index():
        """Trang chủ - Dashboard"""
        return render_template('index.html')
    
    @app.route('/orders')
    def order_reports_page():
        """Trang quản lý báo cáo đơn hàng"""
        return render_template('order_reports.html')
    
    @app.route('/products')
    def product_reports_page():
        """Trang quản lý báo cáo sản phẩm"""
        return render_template('product_reports.html')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint kiểm tra trạng thái service"""
        return jsonify({
            'status': 'healthy',
            'service': 'Reporting Service',
            'version': '1.0.0'
        }), 200
    
    # Error handlers
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
    
    # Tạo tables nếu chưa tồn tại
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get('PORT', 5003)
    app.run(host='0.0.0.0', port=port, debug=True)

