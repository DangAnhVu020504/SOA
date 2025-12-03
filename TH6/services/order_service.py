"""
Order Service - Gọi Order Service (TH4) để quản lý đơn hàng
"""
from services.base_service import BaseService
from config import Config

class OrderService(BaseService):
    """Service để tương tác với Order Service"""
    
    def __init__(self):
        super().__init__(Config.ORDER_SERVICE_URL)
    
    def list_orders(self):
        """GET /orders: Lấy danh sách đơn hàng"""
        return self._make_request('GET', '/orders')
    
    def get_order(self, order_id):
        """GET /orders/{id}: Lấy chi tiết đơn hàng"""
        return self._make_request('GET', f'/orders/{order_id}')
    
    def create_order(self, customer_name, customer_email, items):
        """
        POST /orders: Tạo đơn hàng mới
        
        Args:
            customer_name: Tên khách hàng
            customer_email: Email khách hàng
            items: Danh sách sản phẩm
            
        Returns:
            tuple: (response_data, status_code)
        """
        data = {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'items': items
        }
        return self._make_request('POST', '/orders', data=data)
    
    def update_order_status(self, order_id, status):
        """
        PUT /orders/{id}: Cập nhật trạng thái đơn hàng
        
        Args:
            order_id: ID đơn hàng
            status: Trạng thái mới (pending, completed, cancelled)
            
        Returns:
            tuple: (response_data, status_code)
        """
        data = {'status': status}
        return self._make_request('PUT', f'/orders/{order_id}', data=data)
    
    def add_order_item(self, order_id, product_id, quantity):
        """
        POST /order_items: Thêm sản phẩm vào đơn hàng
        
        Args:
            order_id: ID đơn hàng
            product_id: ID sản phẩm
            quantity: Số lượng
            
        Returns:
            tuple: (response_data, status_code)
        """
        data = {
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity
        }
        return self._make_request('POST', '/order_items', data=data)
    
    def delete_order(self, order_id):
        """DELETE /orders/{id}: Xóa đơn hàng"""
        return self._make_request('DELETE', f'/orders/{order_id}')
