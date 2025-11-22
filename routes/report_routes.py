"""
Routes cho API báo cáo
"""
from flask import Blueprint
from controllers.report_controller import ReportController
from auth_middleware import token_required

# Tạo Blueprint cho reporting routes
report_bp = Blueprint('reports', __name__, url_prefix='/reports')

# Routes cho Product Reports
@report_bp.route('/products', methods=['GET'])
@token_required
def get_all_product_reports():
    """GET /reports/products: Lấy danh sách tất cả các báo cáo theo sản phẩm"""
    return ReportController.get_all_product_reports()

@report_bp.route('/products/<int:report_id>', methods=['GET'])
@token_required
def get_product_report_by_id(report_id):
    """GET /reports/products/id: Lấy chi tiết báo cáo cho một sản phẩm"""
    return ReportController.get_product_report_by_id(report_id)

@report_bp.route('/products', methods=['POST'])
@token_required
def create_product_report():
    """POST /reports/products: Tạo báo cáo sản phẩm mới"""
    return ReportController.create_product_report()

@report_bp.route('/products/<int:report_id>', methods=['DELETE'])
@token_required
def delete_product_report(report_id):
    """DELETE /reports/products/id: Xóa báo cáo sản phẩm"""
    return ReportController.delete_product_report(report_id)

# Routes cho Order Reports
@report_bp.route('/orders', methods=['GET'])
@token_required
def get_all_order_reports():
    """GET /reports/orders: Lấy danh sách tất cả các báo cáo theo đơn hàng"""
    return ReportController.get_all_order_reports()

@report_bp.route('/orders/<int:report_id>', methods=['GET'])
@token_required
def get_order_report_by_id(report_id):
    """GET /reports/orders/id: Lấy chi tiết báo cáo cho một đơn hàng"""
    return ReportController.get_order_report_by_id(report_id)

@report_bp.route('/orders', methods=['POST'])
@token_required
def create_order_report():
    """POST /reports/orders: Tạo báo cáo đơn hàng mới"""
    return ReportController.create_order_report()

@report_bp.route('/orders/<int:report_id>', methods=['DELETE'])
@token_required
def delete_order_report(report_id):
    """DELETE /reports/orders/id: Xóa báo cáo đơn hàng"""
    return ReportController.delete_order_report(report_id)

