"""
Configuration cho API Gateway
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Cấu hình chung"""
    PORT = int(os.getenv('PORT', 5004))
    DEBUG = True
    
    # External Services URLs
    PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:5001')
    ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5002')
    REPORT_SERVICE_URL = os.getenv('REPORT_SERVICE_URL', 'http://localhost:5003')
    
    # Default auth token for inter-service communication
    AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')
