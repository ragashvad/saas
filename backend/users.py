# backend/users.py
from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)

users = {
    "user1": {
        "name": "Alice SME",
        "email": "alice@example.com",
        "password": "password1",
        "plan": "basic",
    },
    "user2": {
        "name": "Bob Enterprise",
        "email": "bob@example.com",
        "password": "password2",
        "plan": "pro",
    },
}

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    password = data.get('password')
    user = users.get(user_id)
    if user and user["password"] == password:
        user_copy = user.copy()
        user_copy.pop("password", None)
        return jsonify({"login": "success", "user_id": user_id, "user": user_copy})
    return jsonify({"login": "failed"}), 401

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"status": "failed", "message": "user_id required"}), 400
    if user_id in users:
        return jsonify({"status": "exists"})
    users[user_id] = {
        "name": data.get('name', ''),
        "email": data.get('email', ''),
        "password": data.get('password', ''),
        "plan": "basic",
    }
    return jsonify({"status": "registered", "user_id": user_id})