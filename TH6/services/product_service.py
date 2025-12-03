"""
Product Service - Gọi Product Service (TH3) để quản lý sản phẩm
"""
from services.base_service import BaseService
from config import Config

class ProductService(BaseService):
    """Service để tương tác với Product Service"""
    
    def __init__(self):
        super().__init__(Config.PRODUCT_SERVICE_URL)
    
    def get_all_products(self):
        """GET /products: Lấy danh sách tất cả sản phẩm"""
        return self._make_request('GET', '/products')
    
    def get_product(self, product_id):
        """GET /products/{id}: Lấy chi tiết sản phẩm"""
        return self._make_request('GET', f'/products/{product_id}')
    
    def update_product_quantity(self, product_id, quantity):
        """
        PUT /products/{id}: Cập nhật số lượng sản phẩm
        
        Args:
            product_id: ID của sản phẩm
            quantity: Số lượng sản phẩm sau khi bán
            
        Returns:
            tuple: (response_data, status_code)
        """
        return self._make_request('PUT', f'/products/{product_id}', 
                                 data={'quantity': quantity})
    
    def check_stock(self, product_id, quantity):
        """
        Kiểm tra xem có đủ hàng không
        
        Args:
            product_id: ID sản phẩm
            quantity: Số lượng cần kiểm tra
            
        Returns:
            tuple: (is_available, product_data, error_message)
        """
        product_data, status = self.get_product(product_id)
        
        if status != 200:
            return False, None, f"Product not found or error: {status}"
        
        available_quantity = product_data.get('quantity', 0)
        if available_quantity >= quantity:
            return True, product_data, None
        else:
            return False, product_data, f"Insufficient stock. Available: {available_quantity}, Requested: {quantity}"
