# backend/analytics.py
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import re

def fit_anomaly_model():
    X = np.random.normal(20, 5, (1000, 1))
    model = IsolationForest(contamination=0.05, random_state=0)
    model.fit(X)
    return model

def fit_predictive_model():
    X = np.arange(30).reshape(-1, 1)
    y = 25 + 0.7 * X.squeeze() + np.random.normal(0, 2, X.shape[0])
    model = LinearRegression()
    model.fit(X, y)
    return model

anomaly_model = fit_anomaly_model()
predictive_model = fit_predictive_model()

def detect_anomalies(energy_kwh_values):
    if len(energy_kwh_values) == 0:
        return []
    values = np.array(energy_kwh_values).reshape(-1, 1)
    preds = anomaly_model.predict(values)
    return [True if p == -1 else False for p in preds]

def predict_next_day(total_last_30days):
    if not total_last_30days:
        return 0.0
    pred = predictive_model.predict([[len(total_last_30days)]])
    return float(pred[0])

def get_recommendations(sensor_data, anomaly_flags):
    recs = []
    if sum(anomaly_flags) > 0:
        recs.append(f"Found {sum(anomaly_flags)} anomaly/anomalies: inspect devices.")
    avg_usage = np.mean([d['energy_kwh'] for d in sensor_data]) if sensor_data else 0.0
    if avg_usage > 30:
        recs.append("High average usage. Consider optimization or load shifting.")
    if sum([d.get('carbon_kg', 0) for d in sensor_data]) > 40:
        recs.append("Carbon footprint is high: evaluate renewable sources.")
    if not recs:
        recs.append("No significant issues detected.")
    return recs

# ESG extraction
ESG_KEYWORDS = {
    'energy': ['energy', 'kwh', 'electricity'],
    'carbon': ['carbon', 'co2', 'emission'],
    'waste': ['waste', 'recycle'],
    'water': ['water', 'consumption']
}

def extract_esg_kpis(text):
    results = {k: 0.0 for k in ESG_KEYWORDS}
    for k, keywords in ESG_KEYWORDS.items():
        for word in keywords:
            matches = re.findall(fr"{word}[^0-9]*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
            if matches:
                results[k] += sum([float(m) for m in matches])
    return results