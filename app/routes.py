from flask import Blueprint, jsonify, request, session
from functools import wraps
from .models import inventory, users
from .external_api import fetch_product

inventory_bp = Blueprint("inventory", __name__)

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = session.get("user")
            if not user or user["role"] not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


@inventory_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "viewer")  # default role is viewer

    # Check if username already exists
    if any(u["username"] == username for u in users):
        return jsonify({"error": "Username already exists"}), 400

    new_id = max([u["id"] for u in users]) + 1 if users else 1
    new_user = {
        "id": new_id,
        "username": username,
        "password": password,  # plain text for now
        "role": role
    }
    users.append(new_user)
    return jsonify({"message": "User registered successfully", "user": new_user}), 201

# --- Auth routes ---
@inventory_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    session["user"] = {"username": user["username"], "role": user["role"]}
    return jsonify({"message": "Login successful", "role": user["role"]})

@inventory_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"})

# --- Inventory routes ---
@inventory_bp.route("/", methods=["GET"])
@role_required(["viewer", "staff", "admin"])
def get_inventory():
    return jsonify(inventory)

@inventory_bp.route("/", methods=["POST"])
@role_required(["staff", "admin"])
def add_item():
    data = request.json
    new_id = max([i["id"] for i in inventory]) + 1 if inventory else 1
    new_item = {
        "id": new_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands"),
        "ingredients_text": data.get("ingredients_text"),
        "price": data.get("price"),
        "stock": data.get("stock"),
        "barcode": data.get("barcode")
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
@role_required(["staff", "admin"])
def update_item(item_id):
    data = request.json
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return ("Item not found", 404)
    if "stock" in data:
        item["stock"] = data["stock"]
    if "price" in data:
        item["price"] = data["price"]
    return jsonify(item)

@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return ("Item not found", 404)
    inventory.remove(item)
    return jsonify({"message": "Item deleted"})
