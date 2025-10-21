import os
from decimal import Decimal, InvalidOperation
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from models import db, Product
from auth import jwt_required_external
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"

db.init_app(app)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

# 1) GET /products: Lấy danh sách tất cả sản phẩm
@app.get("/products")
@jwt_required_external
def list_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return jsonify([p.to_dict() for p in products]), 200

# 2) GET /products/:id: Lấy chi tiết sản phẩm
@app.get("/products/<int:product_id>")
@jwt_required_external
def get_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

# 3) POST /products: Thêm sản phẩm mới
@app.post("/products")
@jwt_required_external
def create_product():
    data = request.get_json() or {}

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    quantity = data.get("quantity")

    # Validate cơ bản
    if not name:
        return jsonify({"msg": "name is required"}), 400
    try:
        price = Decimal(str(price))
        if price < 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return jsonify({"msg": "price must be a non-negative number"}), 400
    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"msg": "quantity must be a non-negative integer"}), 400

    product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

# 4) PUT /products/:id: Cập nhật sản phẩm
@app.put("/products/<int:product_id>")
@jwt_required_external
def update_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    data = request.get_json() or {}

    name = data.get("name", product.name)
    description = data.get("description", product.description)
    price = data.get("price", product.price)
    quantity = data.get("quantity", product.quantity)

    # Validate
    if not name:
        return jsonify({"msg": "name cannot be empty"}), 400
    try:
        price = Decimal(str(price))
        if price < 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return jsonify({"msg": "price must be a non-negative number"}), 400
    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"msg": "quantity must be a non-negative integer"}), 400

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()
    return jsonify(product.to_dict()), 200

# 5) DELETE /products/:id: Xóa sản phẩm
@app.delete("/products/<int:product_id>")
@jwt_required_external
def delete_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
