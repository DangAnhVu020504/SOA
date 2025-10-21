import datetime

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:02052004@localhost:3306/productdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key-change-this"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
