# backend/billing.py
from flask import Blueprint, jsonify, request

billing_bp = Blueprint('billing', __name__)

PLANS = {
    "basic": {
        "price": 0,
        "limits": {"sites": 1, "devices": 3},
        "features": ["Basic KPIs", "Community support"],
    },
    "pro": {
        "price": 49,
        "limits": {"sites": 5, "devices": 20},
        "features": ["Advanced analytics", "Email reports", "Priority support"],
    },
    "enterprise": {
        "price": "custom",
        "limits": {"sites": "unlimited", "devices": "unlimited"},
        "features": ["Custom modules", "White-label", "SLA support"],
    },
}

user_plans = {"user1": "basic", "user2": "pro"}

@billing_bp.route('/plans', methods=['GET'])
def get_plans():
    return jsonify(PLANS)

@billing_bp.route('/get_plan/<user_id>', methods=['GET'])
def get_plan(user_id):
    plan = user_plans.get(user_id, "basic")
    plan_info = PLANS.get(plan, PLANS["basic"])
    return jsonify({"plan": plan, "info": plan_info})

@billing_bp.route('/upgrade', methods=['POST'])
def upgrade():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    new_plan = data.get('new_plan')
    if not user_id or not new_plan:
        return jsonify({"status": "failed", "message": "user_id and new_plan required"}), 400
    if new_plan in PLANS:
        user_plans[user_id] = new_plan
        return jsonify({"status": "success", "plan": new_plan})
    return jsonify({"status": "failed", "message": "Plan not found"}), 400