"""
Cấu hình cho dịch vụ báo cáo
"""
import os
from datetime import timedelta

class Config:
    """Cấu hình cơ bản"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Database configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '02052004'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'reporting_service'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JWT Configuration (cho authentication service từ bài TH2)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ALGORITHM = 'HS256'
    
    # Authentication service URL (tham chiếu từ bài TH2)
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL') or 'http://localhost:5002'
    
    # Port cho reporting service
    PORT = int(os.environ.get('PORT') or 5003)

