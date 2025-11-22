"""
Authentication middleware - Tham chiếu từ bài thực hành số 2
Xác thực token JWT từ authentication service
"""
from functools import wraps
from flask import request, jsonify, current_app
import jwt
import requests

def token_required(f):
    """Decorator để yêu cầu token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Lấy token từ header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            except IndexError:
                return jsonify({'message': 'Token không hợp lệ'}), 401
        
        if not token:
            return jsonify({'message': 'Token bị thiếu'}), 401
        
        try:
            # Xác thực token với authentication service
            auth_service_url = current_app.config.get('AUTH_SERVICE_URL', 'http://localhost:5002')
            verify_url = f"{auth_service_url}/auth/verify"
            
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(verify_url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # Lưu thông tin user vào request để sử dụng trong route
                request.current_user = data.get('user', {})
            else:
                return jsonify({'message': 'Token không hợp lệ hoặc đã hết hạn'}), 401
                
        except requests.exceptions.RequestException:
            # Nếu không kết nối được với auth service, thử verify token trực tiếp
            try:
                jwt_secret = current_app.config.get('JWT_SECRET_KEY')
                decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
                request.current_user = decoded
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token đã hết hạn'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token không hợp lệ'}), 401
        except Exception as e:
            return jsonify({'message': f'Lỗi xác thực: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

