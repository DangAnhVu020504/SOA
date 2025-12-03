/* Checkout.js - Shopping Cart and Checkout Scripts */

const API_BASE = '/api';
let cart = [];
let products = [];

// Initialize checkout page
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

// Load products from API
function loadProducts() {
    const productsList = document.getElementById('products-list');
    productsList.innerHTML = '<p class="loading">Đang tải sản phẩm...</p>';
    
    fetch(`${API_BASE}/products`)
        .then(response => response.json())
        .then(data => {
            products = Array.isArray(data) ? data : [];
            
            if (products.length === 0) {
                productsList.innerHTML = '<p class="empty-message">Không có sản phẩm nào</p>';
                return;
            }
            
            productsList.innerHTML = products.map(product => `
                <div class="product-card">
                    <div class="product-header">
                        <div class="product-image">📦</div>
                        <div class="product-name">${product.name}</div>
                    </div>
                    <div class="product-body">
                        <div class="product-price">${formatPrice(product.price)}</div>
                        <div class="product-stock">Tồn kho: <strong>${product.quantity}</strong></div>
                        <p>${product.description || ''}</p>
                        <div class="product-actions">
                            <input type="number" class="quantity-input" 
                                   id="qty-${product.id}" min="1" max="${product.quantity}" 
                                   value="1" placeholder="Số lượng">
                            <button class="btn btn-primary add-to-cart-btn" 
                                    onclick="addToCart(${product.id})">
                                Thêm vào giỏ
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Error:', error);
            productsList.innerHTML = `<p class="empty-message">Lỗi: ${error.message}</p>`;
        });
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const quantityInput = document.getElementById(`qty-${productId}`);
    const quantity = parseInt(quantityInput.value) || 1;
    
    if (quantity <= 0 || quantity > product.quantity) {
        alert('Số lượng không hợp lệ');
        return;
    }
    
    // Check if product already in cart
    const existingItem = cart.find(item => item.product_id === productId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            product_id: productId,
            product_name: product.name,
            price: product.price,
            quantity: quantity
        });
    }
    
    updateCartUI();
    quantityInput.value = 1;
}

// Update cart display
function updateCartUI() {
    const cartItems = document.getElementById('cart-items');
    const totalAmount = document.getElementById('total-amount');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-message">Giỏ hàng trống</p>';
        totalAmount.textContent = '0 VNĐ';
        return;
    }
    
    let total = 0;
    cartItems.innerHTML = cart.map((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        return `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.product_name}</div>
                    <div class="cart-item-detail">
                        Giá: ${formatPrice(item.price)} × ${item.quantity} = ${formatPrice(itemTotal)}
                    </div>
                </div>
                <div class="cart-item-total">${formatPrice(itemTotal)}</div>
                <button class="remove-item-btn" onclick="removeFromCart(${index})">
                    Xóa
                </button>
            </div>
        `;
    }).join('');
    
    totalAmount.textContent = formatPrice(total);
}

// Remove item from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartUI();
}

// Clear entire cart
function clearCart() {
    if (confirm('Bạn có chắc muốn xóa toàn bộ giỏ hàng?')) {
        cart = [];
        updateCartUI();
    }
}

// Submit order
function submitOrder() {
    const customerName = document.getElementById('customer-name').value.trim();
    const customerEmail = document.getElementById('customer-email').value.trim();
    
    // Validate
    if (!customerName) {
        alert('Vui lòng nhập tên khách hàng');
        return;
    }
    
    if (!customerEmail || !isValidEmail(customerEmail)) {
        alert('Vui lòng nhập email hợp lệ');
        return;
    }
    
    if (cart.length === 0) {
        alert('Giỏ hàng trống');
        return;
    }
    
    // Prepare order data
    const orderData = {
        customer_name: customerName,
        customer_email: customerEmail,
        items: cart.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity
        }))
    };
    
    // Submit order
    const checkoutBtn = document.getElementById('checkout-btn');
    checkoutBtn.disabled = true;
    checkoutBtn.textContent = 'Đang xử lý...';
    
    fetch(`${API_BASE}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success || data.order_id) {
            showOrderResult(data, true);
        } else {
            showOrderResult(data, false);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showOrderResult({ error: error.message }, false);
    })
    .finally(() => {
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = 'Đặt Hàng';
    });
}

// Show order result
function showOrderResult(result, success) {
    const orderResult = document.getElementById('order-result');
    const resultContent = document.getElementById('result-content');
    
    if (success) {
        const order = result.order || result;
        resultContent.innerHTML = `
            <div class="alert alert-success show">
                <strong>✅ Đặt hàng thành công!</strong>
            </div>
            <div class="result-content">
                <div class="result-item">
                    <span class="result-label">Mã đơn hàng:</span>
                    <span class="result-value">#${order.id}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Khách hàng:</span>
                    <span class="result-value">${order.customer_name}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Email:</span>
                    <span class="result-value">${order.customer_email}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Tổng tiền:</span>
                    <span class="result-value">${formatPrice(order.total_amount)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Trạng thái:</span>
                    <span class="result-value">${getStatusText(order.status)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Thời gian:</span>
                    <span class="result-value">${new Date(order.created_at).toLocaleString('vi-VN')}</span>
                </div>
                
                <h3 style="margin-top: 1.5rem; margin-bottom: 1rem;">Chi tiết sản phẩm:</h3>
                ${order.items && order.items.length > 0 ? order.items.map(item => `
                    <div class="result-item">
                        <div><strong>${item.product_name}</strong></div>
                        <div style="font-size: 0.9rem; color: #666;">
                            Số lượng: ${item.quantity} × ${formatPrice(item.unit_price)} = ${formatPrice(item.total_price)}
                        </div>
                    </div>
                `).join('') : ''}
            </div>
        `;
    } else {
        resultContent.innerHTML = `
            <div class="alert alert-error show">
                <strong>❌ Đặt hàng thất bại!</strong>
            </div>
            <div class="result-content">
                <p>${result.error || result.msg || 'Có lỗi xảy ra'}</p>
            </div>
        `;
    }
    
    // Scroll to result and hide previous sections
    document.getElementById('products-section').classList.add('hidden');
    document.getElementById('checkout-step-1').classList.add('hidden');
    orderResult.classList.remove('hidden');
    orderResult.scrollIntoView({ behavior: 'smooth' });
}

// Reset checkout form
function resetCheckout() {
    cart = [];
    document.getElementById('customer-name').value = '';
    document.getElementById('customer-email').value = '';
    document.getElementById('order-result').classList.add('hidden');
    document.getElementById('products-section').classList.remove('hidden');
    loadProducts();
    updateCartUI();
    window.scrollTo(0, 0);
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

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function getStatusText(status) {
    const statuses = {
        'pending': '⏳ Chờ xử lý',
        'completed': '✅ Hoàn thành',
        'cancelled': '❌ Đã hủy'
    };
    return statuses[status] || status;
}
