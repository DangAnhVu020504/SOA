from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import hashlib
import base64
import re
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Anhvu02052004%40@localhost:3306/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cấu hình JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-this'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)


# Model
class User(db.Model):
    __tablename__ = 'users'
    IdUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)  # lưu MD5
    Token = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {"IdUser": self.IdUser, "UserName": self.UserName}


# Helper
def is_md5_hex(s: str) -> bool:
    """Kiểm tra chuỗi có phải md5 hex hay không"""
    return bool(re.fullmatch(r"[0-9a-fA-F]{32}", s))


# API
# Đăng ký user mới (lưu password dạng MD5)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("userName")
    password = data.get("password")  # plain text

    if not username or not password:
        return jsonify({"msg": "userName and password required"}), 400

    if User.query.filter_by(UserName=username).first():
        return jsonify({"msg": "User already exists"}), 400

    md5_hex = hashlib.md5(password.encode()).hexdigest()
    new_user = User(UserName=username, Password=md5_hex)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created", "user": new_user.to_dict()}), 201


# Đăng nhập
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("userName")
    pwd_sent = data.get("password")

    if not username or not pwd_sent:
        return jsonify({"msg": "userName and password required"}), 400

    user = User.query.filter_by(UserName=username).first()
    if not user:
        return jsonify({"msg": "Bad credentials"}), 401

    # kiểm tra password
    if is_md5_hex(pwd_sent):
        client_md5 = pwd_sent.lower()
    else:
        try:
            raw = base64.b64decode(pwd_sent).decode("utf-8")
            client_md5 = hashlib.md5(raw.encode()).hexdigest()
        except Exception:
            return jsonify({"msg": "Password format not recognized"}), 400

    if client_md5 != user.Password.lower():
        return jsonify({"msg": "Bad credentials"}), 401

    # tạo JWT token
    claims = {"userId": user.IdUser}
    access_token = create_access_token(identity=user.UserName, additional_claims=claims)

    user.Token = access_token
    db.session.commit()

    return jsonify(access_token=access_token, token_type="Bearer"), 200


# Xác thực token
@app.route("/auth", methods=["GET"])
@jwt_required()
def auth():
    identity = get_jwt_identity()
    return jsonify({"msg": "Token valid", "user": identity}), 200


# Hello World
@app.route("/hello", methods=["GET"])
@jwt_required()
def hello():
    identity = get_jwt_identity()
    return jsonify({"msg": f"Hello World, {identity}!"}), 200


# Main
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
