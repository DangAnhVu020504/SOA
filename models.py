"""
Models cho dịch vụ báo cáo
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class OrderReport(db.Model):
    """Model cho bảng orders_reports"""
    __tablename__ = 'orders_reports'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False, comment='ID của đơn hàng')
    total_revenue = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    total_profit = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship với ProductReport
    product_reports = db.relationship('ProductReport', backref='order_report', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, order_id, total_revenue=0.00, total_cost=0.00):
        self.order_id = order_id
        self.total_revenue = total_revenue
        self.total_cost = total_cost
        self.total_profit = float(total_revenue) - float(total_cost)
    
    def calculate_profit(self):
        """Tính toán lại lợi nhuận"""
        self.total_profit = float(self.total_revenue) - float(self.total_cost)
        return self.total_profit
    
    def to_dict(self):
        """Chuyển đổi model thành dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'total_revenue': float(self.total_revenue),
            'total_cost': float(self.total_cost),
            'total_profit': float(self.total_profit),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<OrderReport {self.id}: Order {self.order_id}>'


class ProductReport(db.Model):
    """Model cho bảng product_reports"""
    __tablename__ = 'product_reports'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_report_id = db.Column(db.Integer, db.ForeignKey('orders_reports.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False, comment='ID sản phẩm')
    total_sold = db.Column(db.Integer, nullable=False, default=0)
    revenue = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    cost = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    profit = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, order_report_id, product_id, total_sold=0, revenue=0.00, cost=0.00):
        self.order_report_id = order_report_id
        self.product_id = product_id
        self.total_sold = total_sold
        self.revenue = revenue
        self.cost = cost
        self.profit = float(revenue) - float(cost)
    
    def calculate_profit(self):
        """Tính toán lại lợi nhuận"""
        self.profit = float(self.revenue) - float(self.cost)
        return self.profit
    
    def to_dict(self):
        """Chuyển đổi model thành dictionary"""
        return {
            'id': self.id,
            'order_report_id': self.order_report_id,
            'product_id': self.product_id,
            'total_sold': self.total_sold,
            'revenue': float(self.revenue),
            'cost': float(self.cost),
            'profit': float(self.profit),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ProductReport {self.id}: Product {self.product_id}>'

