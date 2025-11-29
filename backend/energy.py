# backend/energy.py
from flask import Blueprint, jsonify
from analytics import detect_anomalies, predict_next_day, get_recommendations
import random

energy_bp = Blueprint('energy', __name__)

def simulate_energy_data(num_devices=3):
    data = []
    for i in range(num_devices):
        val = round(random.uniform(10, 40), 2)
        carbon = round(val * random.uniform(0.25, 0.35), 2)
        device = {
            "device_id": f"meter_{i+1}",
            "energy_kwh": val,
            "carbon_kg": carbon,
        }
        data.append(device)
    return data

@energy_bp.route('/sensor_data/<user_id>', methods=['GET'])
def get_sensor_data(user_id):
    num_devices = 10 if user_id == "user2" else 3
    data = simulate_energy_data(num_devices=num_devices)
    energies = [d["energy_kwh"] for d in data]
    anomaly_flags = detect_anomalies(energies)
    for d, anomaly in zip(data, anomaly_flags):
        d["anomaly"] = anomaly
    kpi = {
        "total_energy": round(sum(energies), 2),
        "total_carbon": round(sum(d["carbon_kg"] for d in data), 2),
        "anomalies": int(sum(anomaly_flags))
    }
    random_hist = [round(random.uniform(18, 35), 2) for _ in range(30)]
    next_day_pred = predict_next_day(random_hist)
    recs = get_recommendations(data, anomaly_flags)
    return jsonify({
        "raw": data,
        "kpi": kpi,
        "predict_next_day_kwh": round(next_day_pred, 2),
        "recommendations": recs,
        "history_kwh": random_hist
    })