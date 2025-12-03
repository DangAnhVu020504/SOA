/* App.js - Main Dashboard Scripts */

const API_BASE = '/api';

// Load products on dashboard
function loadProducts() {
    const productsSection = document.getElementById('products-section');
    const productsList = document.getElementById('products-list');
    
    // Hide other sections
    document.getElementById('orders-section').classList.add('hidden');
    document.getElementById('reports-section').classList.add('hidden');
    productsSection.classList.remove('hidden');
    
    productsList.innerHTML = '<p class="loading">Đang tải sản phẩm...</p>';
    
    fetch(`${API_BASE}/products`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                if (data.length === 0) {
                    productsList.innerHTML = '<p class="empty-message">Không có sản phẩm nào</p>';
                    return;
                }
                
                productsList.innerHTML = data.map(product => `
                    <div class="product-card">
                        <div class="product-header">
                            <div class="product-image">📦</div>
                            <div class="product-name">${product.name}</div>
                        </div>
                        <div class="product-body">
                            <div class="product-price">${formatPrice(product.price)}</div>
                            <div class="product-stock">Tồn kho: ${product.quantity}</div>
                            <p>${product.description || 'Mô tả sản phẩm'}</p>
                        </div>
                    </div>
                `).join('');
            } else {
                productsList.innerHTML = '<p class="empty-message">Lỗi tải dữ liệu</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            productsList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Load orders on dashboard
function loadOrders() {
    const ordersSection = document.getElementById('orders-section');
    const ordersList = document.getElementById('orders-list');
    
    // Hide other sections
    document.getElementById('products-section').classList.add('hidden');
    document.getElementById('reports-section').classList.add('hidden');
    ordersSection.classList.remove('hidden');
    
    ordersList.innerHTML = '<p class="loading">Đang tải đơn hàng...</p>';
    
    fetch(`${API_BASE}/orders`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                let html = `
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Khách hàng</th>
                                <th>Email</th>
                                <th>Tổng tiền</th>
                                <th>Trạng thái</th>
                                <th>Ngày tạo</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                data.forEach(order => {
                    html += `
                        <tr>
                            <td>${order.id}</td>
                            <td>${order.customer_name}</td>
                            <td>${order.customer_email}</td>
                            <td>${formatPrice(order.total_amount)}</td>
                            <td><span class="status-${order.status}">${getStatusText(order.status)}</span></td>
                            <td>${new Date(order.created_at).toLocaleDateString('vi-VN')}</td>
                        </tr>
                    `;
                });
                
                html += `
                        </tbody>
                    </table>
                `;
                ordersList.innerHTML = html;
            } else {
                ordersList.innerHTML = '<p class="empty-message">Không có đơn hàng nào</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            ordersList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Load reports on dashboard
function loadReports() {
    const reportsSection = document.getElementById('reports-section');
    
    // Hide other sections
    document.getElementById('products-section').classList.add('hidden');
    document.getElementById('orders-section').classList.add('hidden');
    reportsSection.classList.remove('hidden');
    
    loadOrderReports();
}

function showOrderReports() {
    document.getElementById('order-reports').classList.remove('hidden');
    document.getElementById('product-reports').classList.add('hidden');
    loadOrderReports();
}

function showProductReports() {
    document.getElementById('product-reports').classList.remove('hidden');
    document.getElementById('order-reports').classList.add('hidden');
    loadProductReports();
}

function loadOrderReports() {
    const reportsList = document.getElementById('order-reports') || 
                       document.getElementById('order-reports-list');
    
    if (reportsList) {
        reportsList.innerHTML = '<p class="loading">Đang tải báo cáo...</p>';
    }
    
    fetch(`${API_BASE}/reports/orders`)
        .then(response => response.json())
        .then(data => {
            let reports = data.data || (Array.isArray(data) ? data : []);
            
            if (reportsList) {
                if (reports.length === 0) {
                    reportsList.innerHTML = '<p class="empty-message">Không có báo cáo nào</p>';
                } else {
                    reportsList.innerHTML = reports.map(report => `
                        <div class="report-card">
                            <h3>Đơn Hàng #${report.order_id}</h3>
                            <div class="report-item">
                                <span class="report-label">Tổng doanh thu:</span>
                                <span class="report-value">${formatPrice(report.total_revenue)}</span>
                            </div>
                            <div class="report-item">
                                <span class="report-label">Tổng chi phí:</span>
                                <span class="report-value">${formatPrice(report.total_cost)}</span>
                            </div>
                            <div class="report-item">
                                <span class="report-label">Lợi nhuận:</span>
                                <span class="report-value">${formatPrice(report.total_profit)}</span>
                            </div>
                        </div>
                    `).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (reportsList) {
                reportsList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
            }
        });
}

function loadProductReports() {
    const reportsList = document.getElementById('product-reports') || 
                       document.getElementById('product-reports-list');
    
    if (reportsList) {
        reportsList.innerHTML = '<p class="loading">Đang tải báo cáo...</p>';
    }
    
    fetch(`${API_BASE}/reports/products`)
        .then(response => response.json())
        .then(data => {
            let reports = data.data || (Array.isArray(data) ? data : []);
            
            if (reportsList) {
                if (reports.length === 0) {
                    reportsList.innerHTML = '<p class="empty-message">Không có báo cáo nào</p>';
                } else {
                    reportsList.innerHTML = reports.map(report => `
                        <div class="report-card">
                            <h3>Sản phẩm #${report.product_id}</h3>
                            <div class="report-item">
                                <span class="report-label">Số lượng bán:</span>
                                <span class="report-value">${report.total_sold}</span>
                            </div>
                            <div class="report-item">
                                <span class="report-label">Doanh thu:</span>
                                <span class="report-value">${formatPrice(report.revenue)}</span>
                            </div>
                            <div class="report-item">
                                <span class="report-label">Chi phí:</span>
                                <span class="report-value">${formatPrice(report.cost)}</span>
                            </div>
                            <div class="report-item">
                                <span class="report-label">Lợi nhuận:</span>
                                <span class="report-value">${formatPrice(report.profit)}</span>
                            </div>
                        </div>
                    `).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (reportsList) {
                reportsList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
            }
        });
}

// Utility functions
function formatPrice(price) {
    if (typeof price === 'string') {
        price = parseFloat(price);
    }
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

function getStatusText(status) {
    const statuses = {
        'pending': '⏳ Chờ xử lý',
        'completed': '✅ Hoàn thành',
        'cancelled': '❌ Đã hủy'
    };
    return statuses[status] || status;
}
