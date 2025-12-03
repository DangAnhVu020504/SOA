"""
Report Service - Gọi Report Service (TH5) để tạo báo cáo
"""
from services.base_service import BaseService
from config import Config

class ReportService(BaseService):
    """Service để tương tác với Report Service"""
    
    def __init__(self):
        super().__init__(Config.REPORT_SERVICE_URL)
    
    # ==================== Order Reports ====================
    
    def get_all_order_reports(self):
        """GET /reports/orders: Lấy danh sách báo cáo đơn hàng"""
        return self._make_request('GET', '/reports/orders')
    
    def get_order_report(self, report_id):
        """GET /reports/orders/{id}: Lấy chi tiết báo cáo đơn hàng"""
        return self._make_request('GET', f'/reports/orders/{report_id}')
    
    def create_order_report(self, data):
        """
        POST /reports/orders: Tạo báo cáo đơn hàng
        
        Args:
            data: {
                'order_id': ID đơn hàng,
                'products': [
                    {
                        'product_id': ID sản phẩm,
                        'total_sold': Số lượng bán,
                        'revenue': Doanh thu,
                        'cost': Chi phí
                    }
                ]
            }
        """
        return self._make_request('POST', '/reports/orders', data=data)
    
    # ==================== Product Reports ====================
    
    def get_all_product_reports(self):
        """GET /reports/products: Lấy danh sách báo cáo sản phẩm"""
        return self._make_request('GET', '/reports/products')
    
    def get_product_report(self, report_id):
        """GET /reports/products/{id}: Lấy chi tiết báo cáo sản phẩm"""
        return self._make_request('GET', f'/reports/products/{report_id}')
    
    def create_product_report(self, data):
        """
        POST /reports/products: Tạo báo cáo sản phẩm
        
        Args:
            data: {
                'order_report_id': ID báo cáo đơn hàng,
                'product_id': ID sản phẩm,
                'total_sold': Số lượng bán,
                'revenue': Doanh thu,
                'cost': Chi phí
            }
        """
        return self._make_request('POST', '/reports/products', data=data)
