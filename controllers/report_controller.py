"""
Controller xử lý nghiệp vụ báo cáo
"""
from flask import jsonify, request
from models import db, OrderReport, ProductReport
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

class ReportController:
    """Controller cho các thao tác báo cáo"""
    
    @staticmethod
    def get_all_product_reports():
        """Lấy danh sách tất cả các báo cáo theo sản phẩm"""
        try:
            product_reports = ProductReport.query.all()
            return jsonify({
                'success': True,
                'data': [report.to_dict() for report in product_reports],
                'count': len(product_reports)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Lỗi khi lấy danh sách báo cáo sản phẩm: {str(e)}'
            }), 500
    
    @staticmethod
    def get_product_report_by_id(report_id):
        """Lấy chi tiết báo cáo cho một sản phẩm"""
        try:
            product_report = ProductReport.query.get(report_id)
            if not product_report:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy báo cáo sản phẩm'
                }), 404
            
            return jsonify({
                'success': True,
                'data': product_report.to_dict()
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Lỗi khi lấy báo cáo sản phẩm: {str(e)}'
            }), 500
    
    @staticmethod
    def get_all_order_reports():
        """Lấy danh sách tất cả các báo cáo theo đơn hàng"""
        try:
            order_reports = OrderReport.query.all()
            return jsonify({
                'success': True,
                'data': [report.to_dict() for report in order_reports],
                'count': len(order_reports)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Lỗi khi lấy danh sách báo cáo đơn hàng: {str(e)}'
            }), 500
    
    @staticmethod
    def get_order_report_by_id(report_id):
        """Lấy chi tiết báo cáo cho một đơn hàng"""
        try:
            order_report = OrderReport.query.get(report_id)
            if not order_report:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy báo cáo đơn hàng'
                }), 404
            
            # Lấy thêm thông tin product reports liên quan
            product_reports = ProductReport.query.filter_by(order_report_id=report_id).all()
            
            result = order_report.to_dict()
            result['product_reports'] = [pr.to_dict() for pr in product_reports]
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Lỗi khi lấy báo cáo đơn hàng: {str(e)}'
            }), 500
    
    @staticmethod
    def create_product_report():
        """Tạo báo cáo sản phẩm mới dựa trên dữ liệu từ dịch vụ quản lý sản phẩm và quản lý đơn hàng"""
        try:
            data = request.get_json()
            
            # Validate dữ liệu đầu vào
            required_fields = ['order_report_id', 'product_id']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'success': False,
                        'message': f'Thiếu trường bắt buộc: {field}'
                    }), 400
            
            # Kiểm tra order_report_id có tồn tại không
            order_report = OrderReport.query.get(data['order_report_id'])
            if not order_report:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy báo cáo đơn hàng với ID này'
                }), 404
            
            # Lấy các giá trị từ request, mặc định là 0 nếu không có
            total_sold = data.get('total_sold', 0)
            revenue = Decimal(str(data.get('revenue', 0.00)))
            cost = Decimal(str(data.get('cost', 0.00)))
            
            # Tạo product report mới
            product_report = ProductReport(
                order_report_id=data['order_report_id'],
                product_id=data['product_id'],
                total_sold=total_sold,
                revenue=revenue,
                cost=cost
            )
            
            # Tính toán profit
            product_report.calculate_profit()
            
            db.session.add(product_report)
            db.session.commit()
            
            # Cập nhật lại tổng doanh thu, chi phí và lợi nhuận của order report
            ReportController._update_order_report_totals(data['order_report_id'])
            
            return jsonify({
                'success': True,
                'message': 'Tạo báo cáo sản phẩm thành công',
                'data': product_report.to_dict()
            }), 201
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Lỗi ràng buộc dữ liệu: {str(e)}'
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Lỗi khi tạo báo cáo sản phẩm: {str(e)}'
            }), 500
    
    @staticmethod
    def create_order_report():
        """Tạo báo cáo đơn hàng mới dựa trên dữ liệu từ dịch vụ quản lý đơn hàng"""
        try:
            data = request.get_json()
            
            # Validate dữ liệu đầu vào
            if 'order_id' not in data:
                return jsonify({
                    'success': False,
                    'message': 'Thiếu trường bắt buộc: order_id'
                }), 400
            
            # Kiểm tra order_id đã tồn tại chưa
            existing_report = OrderReport.query.filter_by(order_id=data['order_id']).first()
            if existing_report:
                return jsonify({
                    'success': False,
                    'message': 'Báo cáo cho đơn hàng này đã tồn tại'
                }), 400
            
            # Lấy các giá trị từ request, mặc định là 0 nếu không có
            total_revenue = Decimal(str(data.get('total_revenue', 0.00)))
            total_cost = Decimal(str(data.get('total_cost', 0.00)))
            
            # Tạo order report mới
            order_report = OrderReport(
                order_id=data['order_id'],
                total_revenue=total_revenue,
                total_cost=total_cost
            )
            
            # Tính toán profit
            order_report.calculate_profit()
            
            db.session.add(order_report)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Tạo báo cáo đơn hàng thành công',
                'data': order_report.to_dict()
            }), 201
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Lỗi ràng buộc dữ liệu: {str(e)}'
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Lỗi khi tạo báo cáo đơn hàng: {str(e)}'
            }), 500
    
    @staticmethod
    def delete_product_report(report_id):
        """Xóa báo cáo sản phẩm"""
        try:
            product_report = ProductReport.query.get(report_id)
            if not product_report:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy báo cáo sản phẩm'
                }), 404
            
            order_report_id = product_report.order_report_id
            
            db.session.delete(product_report)
            db.session.commit()
            
            # Cập nhật lại tổng doanh thu, chi phí và lợi nhuận của order report
            ReportController._update_order_report_totals(order_report_id)
            
            return jsonify({
                'success': True,
                'message': 'Xóa báo cáo sản phẩm thành công'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Lỗi khi xóa báo cáo sản phẩm: {str(e)}'
            }), 500
    
    @staticmethod
    def delete_order_report(report_id):
        """Xóa báo cáo đơn hàng (sẽ tự động xóa các product reports liên quan do CASCADE)"""
        try:
            order_report = OrderReport.query.get(report_id)
            if not order_report:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy báo cáo đơn hàng'
                }), 404
            
            db.session.delete(order_report)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Xóa báo cáo đơn hàng thành công'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Lỗi khi xóa báo cáo đơn hàng: {str(e)}'
            }), 500
    
    @staticmethod
    def _update_order_report_totals(order_report_id):
        """Cập nhật lại tổng doanh thu, chi phí và lợi nhuận của order report dựa trên các product reports"""
        try:
            order_report = OrderReport.query.get(order_report_id)
            if not order_report:
                return
            
            # Tính tổng từ các product reports
            product_reports = ProductReport.query.filter_by(order_report_id=order_report_id).all()
            
            total_revenue = sum(Decimal(str(pr.revenue)) for pr in product_reports)
            total_cost = sum(Decimal(str(pr.cost)) for pr in product_reports)
            
            order_report.total_revenue = total_revenue
            order_report.total_cost = total_cost
            order_report.calculate_profit()
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

