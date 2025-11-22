-- Database schema for Reporting Service
-- Tạo database cho dịch vụ báo cáo

CREATE DATABASE IF NOT EXISTS reporting_service CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE reporting_service;

-- Bảng báo cáo đơn hàng
CREATE TABLE IF NOT EXISTS orders_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL COMMENT 'ID của đơn hàng (lưu vết để liên kết với dịch vụ quản lý đơn hàng)',
    total_revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Tổng doanh thu của đơn hàng',
    total_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Tổng chi phí nhập sản phẩm trong đơn hàng',
    total_profit DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Tổng lợi nhuận (total_revenue - total_cost)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời gian tạo báo cáo',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời gian cập nhật báo cáo',
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng báo cáo sản phẩm
CREATE TABLE IF NOT EXISTS product_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_report_id INT NOT NULL COMMENT 'ID đơn hàng (liên kết với bảng orders_reports)',
    product_id INT NOT NULL COMMENT 'ID sản phẩm (lưu vết để liên kết với dịch vụ quản lý sản phẩm)',
    total_sold INT NOT NULL DEFAULT 0 COMMENT 'Tổng số lượng sản phẩm đã bán',
    revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Doanh thu từ sản phẩm',
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Chi phí nhập sản phẩm',
    profit DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Lợi nhuận (revenue - cost)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời gian tạo báo cáo',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời gian cập nhật báo cáo',
    INDEX idx_order_report_id (order_report_id),
    INDEX idx_product_id (product_id),
    FOREIGN KEY (order_report_id) REFERENCES orders_reports(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

