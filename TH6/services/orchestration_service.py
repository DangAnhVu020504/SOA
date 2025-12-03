"""
Orchestration Service - Điều phối quy trình giữa các service
Quy trình mua hàng hoàn chỉnh:
1. Kiểm tra tồn kho
2. Tạo đơn hàng
3. Thêm sản phẩm vào đơn hàng
4. Cập nhật tồn kho sản phẩm
5. Tạo báo cáo
"""
from decimal import Decimal
from services.product_service import ProductService
from services.order_service import OrderService
from services.report_service import ReportService

class OrchestrationService:
    """Service điều phối quy trình mua hàng"""
    
    def __init__(self):
        self.product_service = ProductService()
        self.order_service = OrderService()
        self.report_service = ReportService()
    
    def create_purchase_order(self, data):
        """
        Quy trình mua hàng hoàn chỉnh:
        1. Kiểm tra tồn kho sản phẩm
        2. Tạo đơn hàng
        3. Thêm các sản phẩm vào đơn hàng
        4. Cập nhật số lượng sản phẩm
        
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
        """
        try:
            # Validate
            customer_name = data.get('customer_name', '').strip()
            customer_email = data.get('customer_email', '').strip()
            items = data.get('items', [])
            
            if not customer_name:
                return {'error': 'customer_name is required'}, 400
            if not customer_email:
                return {'error': 'customer_email is required'}, 400
            if not items or len(items) == 0:
                return {'error': 'items is required and must not be empty'}, 400
            
            # Step 1: Kiểm tra tồn kho cho tất cả sản phẩm
            order_items = []
            for item in items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                
                if not product_id or not quantity or quantity <= 0:
                    return {'error': 'Invalid product_id or quantity'}, 400
                
                # Kiểm tra sản phẩm tồn tại và có đủ hàng
                is_available, product_data, error = self.product_service.check_stock(product_id, quantity)
                
                if not is_available:
                    return {'error': error}, 400
                
                order_items.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'product_data': product_data
                })
            
            # Step 2: Tạo đơn hàng
            create_items = [{'product_id': item['product_id'], 'quantity': item['quantity']} 
                          for item in order_items]
            
            order_result, order_status = self.order_service.create_order(
                customer_name, customer_email, create_items
            )
            
            if order_status != 201:
                return order_result, order_status
            
            order_id = order_result.get('id')
            if not order_id:
                return {'error': 'Failed to create order'}, 500
            
            # Step 3: Cập nhật số lượng sản phẩm
            for item in order_items:
                product_id = item['product_id']
                old_quantity = item['product_data'].get('quantity', 0)
                new_quantity = old_quantity - item['quantity']
                
                update_result, update_status = self.product_service.update_product_quantity(
                    product_id, new_quantity
                )
                
                if update_status not in [200, 201]:
                    # Log warning nhưng không dừng quy trình
                    print(f"Warning: Failed to update product quantity for {product_id}")
            
            # Step 4: Tạo báo cáo (lấy chi tiết đơn hàng trước)
            order_detail, detail_status = self.order_service.get_order(order_id)
            if detail_status == 200:
                # Tạo order report
                report_data = {
                    'order_id': order_id,
                    'total_revenue': float(order_detail.get('total_amount', 0)),
                    'total_cost': 0  # Sẽ tính từ product reports
                }
                
                report_result, report_status = self.report_service.create_order_report(report_data)
                
                # Tạo product reports
                if report_status in [200, 201]:
                    order_report_id = report_result.get('id')
                    
                    for order_item in order_detail.get('items', []):
                        product_id = order_item.get('product_id')
                        
                        # Lấy cost từ product data
                        product_data, _ = self.product_service.get_product(product_id)
                        cost = product_data.get('cost', 0) if isinstance(product_data, dict) else 0
                        
                        product_report_data = {
                            'order_report_id': order_report_id,
                            'product_id': product_id,
                            'total_sold': order_item.get('quantity', 0),
                            'revenue': float(order_item.get('total_price', 0)),
                            'cost': cost * order_item.get('quantity', 0)
                        }
                        
                        self.report_service.create_product_report(product_report_data)
            
            return {
                'success': True,
                'message': 'Purchase order created successfully',
                'order': order_result,
                'order_id': order_id
            }, 201
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def update_order_status(self, order_id, data):
        """
        Cập nhật trạng thái đơn hàng
        Khi trạng thái chuyển thành 'completed', tạo báo cáo
        
        Request body:
        {
            "status": "completed"
        }
        """
        try:
            status = data.get('status', '').strip()
            
            if not status:
                return {'error': 'status is required'}, 400
            
            valid_statuses = ['pending', 'completed', 'cancelled']
            if status not in valid_statuses:
                return {'error': f'status must be one of: {", ".join(valid_statuses)}'}, 400
            
            # Cập nhật trạng thái đơn hàng
            update_result, update_status = self.order_service.update_order_status(order_id, status)
            
            if update_status != 200:
                return update_result, update_status
            
            # Nếu status = completed, tạo báo cáo nếu chưa có
            if status == 'completed':
                order_detail, detail_status = self.order_service.get_order(order_id)
                
                if detail_status == 200:
                    # Kiểm tra xem báo cáo đã tồn tại chưa
                    all_reports, _ = self.report_service.get_all_order_reports()
                    
                    order_report_exists = False
                    if isinstance(all_reports, dict) and 'data' in all_reports:
                        for report in all_reports['data']:
                            if report.get('order_id') == order_id:
                                order_report_exists = True
                                break
                    
                    # Nếu chưa có báo cáo thì tạo mới
                    if not order_report_exists:
                        report_data = {
                            'order_id': order_id,
                            'total_revenue': float(order_detail.get('total_amount', 0)),
                            'total_cost': 0
                        }
                        
                        report_result, report_status = self.report_service.create_order_report(report_data)
                        
                        if report_status in [200, 201]:
                            order_report_id = report_result.get('id')
                            
                            for order_item in order_detail.get('items', []):
                                product_id = order_item.get('product_id')
                                
                                product_data, _ = self.product_service.get_product(product_id)
                                cost = product_data.get('cost', 0) if isinstance(product_data, dict) else 0
                                
                                product_report_data = {
                                    'order_report_id': order_report_id,
                                    'product_id': product_id,
                                    'total_sold': order_item.get('quantity', 0),
                                    'revenue': float(order_item.get('total_price', 0)),
                                    'cost': cost * order_item.get('quantity', 0)
                                }
                                
                                self.report_service.create_product_report(product_report_data)
            
            return {
                'success': True,
                'message': f'Order status updated to {status}',
                'order': update_result
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
