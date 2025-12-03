/* Reports.js - Reports Page Scripts */

const API_BASE = '/api';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadOrderReports();
});

// Switch between tabs
function switchTab(tabName) {
    // Hide all content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab and activate button
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'order-reports-tab') {
        loadOrderReports();
    } else if (tabName === 'product-reports-tab') {
        loadProductReports();
    }
}

// Load order reports
function loadOrderReports() {
    const reportsList = document.getElementById('order-reports-list');
    reportsList.innerHTML = '<p class="loading">Đang tải báo cáo...</p>';
    
    fetch(`${API_BASE}/reports/orders`)
        .then(response => response.json())
        .then(data => {
            let reports = data.data || (Array.isArray(data) ? data : []);
            
            if (reports.length === 0) {
                reportsList.innerHTML = '<p class="empty-message">Không có báo cáo nào</p>';
            } else {
                reportsList.innerHTML = reports.map(report => `
                    <div class="report-card">
                        <h3>Báo Cáo Đơn Hàng #${report.order_id}</h3>
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
                        <div class="report-item">
                            <span class="report-label">Ngày tạo:</span>
                            <span class="report-value">${new Date(report.created_at).toLocaleDateString('vi-VN')}</span>
                        </div>
                        <div class="report-actions">
                            <button class="btn btn-primary" onclick="showOrderDetail(${report.id})">Chi tiết</button>
                            <button class="btn btn-secondary" onclick="updateOrderStatus(${report.order_id})">Cập nhật</button>
                        </div>
                    </div>
                `).join('');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            reportsList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Load product reports
function loadProductReports() {
    const reportsList = document.getElementById('product-reports-list');
    reportsList.innerHTML = '<p class="loading">Đang tải báo cáo...</p>';
    
    fetch(`${API_BASE}/reports/products`)
        .then(response => response.json())
        .then(data => {
            let reports = data.data || (Array.isArray(data) ? data : []);
            
            if (reports.length === 0) {
                reportsList.innerHTML = '<p class="empty-message">Không có báo cáo nào</p>';
            } else {
                reportsList.innerHTML = reports.map(report => `
                    <div class="report-card">
                        <h3>Báo Cáo Sản Phẩm #${report.product_id}</h3>
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
                        <div class="report-item">
                            <span class="report-label">Ngày tạo:</span>
                            <span class="report-value">${new Date(report.created_at).toLocaleDateString('vi-VN')}</span>
                        </div>
                        <div class="report-actions">
                            <button class="btn btn-primary" onclick="showProductDetail(${report.id})">Chi tiết</button>
                        </div>
                    </div>
                `).join('');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            reportsList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Show order details
function showOrderDetail(reportId) {
    const modal = document.getElementById('order-detail-modal');
    const content = document.getElementById('order-detail-content');
    
    content.innerHTML = '<p class="loading">Đang tải chi tiết...</p>';
    modal.classList.remove('hidden');
    
    fetch(`${API_BASE}/reports/orders/${reportId}`)
        .then(response => response.json())
        .then(data => {
            const report = data.data || data;
            
            let html = `
                <div class="result-content">
                    <div class="result-item">
                        <span class="result-label">Mã đơn hàng:</span>
                        <span class="result-value">#${report.order_id}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Tổng doanh thu:</span>
                        <span class="result-value">${formatPrice(report.total_revenue)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Tổng chi phí:</span>
                        <span class="result-value">${formatPrice(report.total_cost)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Lợi nhuận:</span>
                        <span class="result-value">${formatPrice(report.total_profit)}</span>
                    </div>
                    
                    <h3 style="margin-top: 1.5rem; margin-bottom: 1rem;">Chi tiết sản phẩm:</h3>
            `;
            
            if (report.product_reports && report.product_reports.length > 0) {
                html += report.product_reports.map(pr => `
                    <div class="result-item">
                        <div><strong>Sản phẩm #${pr.product_id}</strong></div>
                        <div style="font-size: 0.9rem; color: #666;">
                            Bán: ${pr.total_sold} | Doanh thu: ${formatPrice(pr.revenue)} | 
                            Chi phí: ${formatPrice(pr.cost)} | Lợi nhuận: ${formatPrice(pr.profit)}
                        </div>
                    </div>
                `).join('');
            }
            
            html += '</div>';
            content.innerHTML = html;
        })
        .catch(error => {
            content.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Show product details
function showProductDetail(reportId) {
    const modal = document.getElementById('product-detail-modal');
    const content = document.getElementById('product-detail-content');
    
    content.innerHTML = '<p class="loading">Đang tải chi tiết...</p>';
    modal.classList.remove('hidden');
    
    fetch(`${API_BASE}/reports/products/${reportId}`)
        .then(response => response.json())
        .then(data => {
            const report = data.data || data;
            
            const html = `
                <div class="result-content">
                    <div class="result-item">
                        <span class="result-label">Mã sản phẩm:</span>
                        <span class="result-value">#${report.product_id}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Số lượng bán:</span>
                        <span class="result-value">${report.total_sold}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Doanh thu:</span>
                        <span class="result-value">${formatPrice(report.revenue)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Chi phí:</span>
                        <span class="result-value">${formatPrice(report.cost)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Lợi nhuận:</span>
                        <span class="result-value">${formatPrice(report.profit)}</span>
                    </div>
                </div>
            `;
            content.innerHTML = html;
        })
        .catch(error => {
            content.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Close modals
function closeOrderDetailModal() {
    document.getElementById('order-detail-modal').classList.add('hidden');
}

function closeProductDetailModal() {
    document.getElementById('product-detail-modal').classList.add('hidden');
}

// Update order status
function updateOrderStatus(orderId) {
    const newStatus = prompt('Nhập trạng thái mới (pending/completed/cancelled):');
    
    if (!newStatus) return;
    
    const validStatuses = ['pending', 'completed', 'cancelled'];
    if (!validStatuses.includes(newStatus)) {
        alert('Trạng thái không hợp lệ');
        return;
    }
    
    fetch(`${API_BASE}/orders/${orderId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success || data.order) {
            alert('Cập nhật thành công');
            loadOrderReports();
            closeOrderDetailModal();
        } else {
            alert('Cập nhật thất bại: ' + (data.error || data.msg || 'Không xác định'));
        }
    })
    .catch(error => {
        alert('Lỗi: ' + error.message);
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
