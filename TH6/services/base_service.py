"""
Base Service - Lớp cơ sở cho các service khác
"""
import requests
from config import Config
import os

class BaseService:
    """Lớp cơ sở cho tất cả các service"""
    
    def __init__(self, service_url):
        self.service_url = service_url
        self.auth_token = os.getenv('AUTH_TOKEN', '')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
    
    def _make_request(self, method, endpoint, data=None, params=None):
        """
        Thực hiện HTTP request đến external service
        
        Args:
            method: GET, POST, PUT, DELETE
            endpoint: URL endpoint
            data: Body data (cho POST/PUT)
            params: Query parameters
            
        Returns:
            tuple: (response_data, status_code)
        """
        try:
            url = f"{self.service_url}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, timeout=10)
            else:
                return {'error': 'Invalid method'}, 400
            
            # Xử lý response
            if response.status_code >= 200 and response.status_code < 300:
                try:
                    return response.json(), response.status_code
                except:
                    return {}, response.status_code
            else:
                try:
                    error_data = response.json()
                except:
                    error_data = {'error': response.text}
                return error_data, response.status_code
                
        except requests.exceptions.Timeout:
            return {'error': 'Service timeout'}, 503
        except requests.exceptions.ConnectionError:
            return {'error': 'Cannot connect to service'}, 503
        except Exception as e:
            return {'error': str(e)}, 500
