// Global variables
let authToken = localStorage.getItem('authToken');
let authServiceUrl = localStorage.getItem('authServiceUrl') || 'http://localhost:5002';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateAuthUI();
});

// Authentication functions
function getToken() {
    return localStorage.getItem('authToken');
}

function setToken(token) {
    localStorage.setItem('authToken', token);
    authToken = token;
    updateAuthUI();
}

function clearToken() {
    localStorage.removeItem('authToken');
    authToken = null;
    updateAuthUI();
}

function getAuthHeaders() {
    const token = getToken();
    if (!token) {
        return {};
    }
    return {
        'Authorization': `Bearer ${token}`
    };
}

function updateAuthUI() {
    const token = getToken();
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const userInfo = document.getElementById('user-info');

    if (token) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
        if (userInfo) {
            userInfo.style.display = 'inline-block';
            userInfo.textContent = '✓ Đã đăng nhập';
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (userInfo) userInfo.style.display = 'none';
    }
}

function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
    const savedUrl = localStorage.getItem('authServiceUrl');
    if (savedUrl) {
        document.getElementById('authServiceUrl').value = savedUrl;
    }
}

function closeLogin() {
    document.getElementById('loginModal').style.display = 'none';
    document.getElementById('loginError').style.display = 'none';
    document.getElementById('loginForm').reset();
}

function logout() {
    if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
        clearToken();
        window.location.reload();
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const authUrl = document.getElementById('authServiceUrl').value || 'http://localhost:5002';

    // Save auth service URL
    localStorage.setItem('authServiceUrl', authUrl);
    authServiceUrl = authUrl;

    const errorDiv = document.getElementById('loginError');
    errorDiv.style.display = 'none';

    try {
        const response = await fetch(`${authUrl}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok && data.token) {
            setToken(data.token);
            closeLogin();
            showSuccess('Đăng nhập thành công!');
            // Reload page to refresh data
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            // Try alternative login endpoint
            const altResponse = await fetch(`${authUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const altData = await altResponse.json();

            if (altResponse.ok && altData.token) {
                setToken(altData.token);
                closeLogin();
                showSuccess('Đăng nhập thành công!');
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                errorDiv.textContent = data.message || altData.message || 'Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.';
                errorDiv.style.display = 'block';
            }
        }
    } catch (error) {
        errorDiv.textContent = `Lỗi kết nối: ${error.message}. Vui lòng kiểm tra URL của authentication service.`;
        errorDiv.style.display = 'block';
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

function showSuccess(message) {
    // Remove existing success message if any
    const existing = document.querySelector('.success-message');
    if (existing) {
        existing.remove();
    }

    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    document.body.appendChild(successDiv);

    setTimeout(() => {
        successDiv.style.animation = 'slideInRight 0.3s reverse';
        setTimeout(() => {
            successDiv.remove();
        }, 300);
    }, 3000);
}

// Close modals when clicking outside
window.onclick = function(event) {
    const loginModal = document.getElementById('loginModal');
    if (event.target == loginModal) {
        closeLogin();
    }
}

