# API Documentation - Sustainability-as-a-Service Platform

## Overview
This document provides comprehensive API documentation for the Sustainability-as-a-Service (SaaS) platform. The platform offers cloud-based sustainability monitoring, analytics, and optimization services.

## Base URL
```
http://localhost:5000
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   User Interface Layer                       │
│         (Streamlit Dashboard / External Clients)             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service/API Layer                         │
│      Flask REST APIs - Energy, Analytics, ESG, Billing      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analytics Layer                           │
│   Energy Prediction │ Anomaly Detection │ Optimization      │
│   Carbon Footprint  │ ESG Scoring │ ML Models              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Data Integration Layer                        │
│         SQLite Database │ Time-Series Storage               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   IoT & Edge Layer                           │
│   Energy Meters │ Temperature Sensors │ Occupancy Sensors   │
│   Water Meters  │ Simulated IoT Devices                     │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

### 1. User Management (`/users`)

#### POST `/users/login`
Authenticate user and create session.

**Request:**
```json
{
  "user_id": "user1",
  "password": "password1"
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "user1",
  "plan": "basic"
}
```

---

### 2. Energy Monitoring (`/energy`)

#### GET `/energy/sensor_data/<user_id>`
Get real-time sensor data from all IoT devices.

**Response:**
```json
{
  "raw": {
    "energy_meters": [{
      "device_id": "energy_meter_1",
      "timestamp": "2025-11-29T10:30:00",
      "energy_kwh": 25.3,
      "voltage_v": 223.5,
      "current_a": 113.2,
      "power_factor": 0.892,
      "carbon_kg": 7.6,
      "carbon_intensity": 0.3,
      "anomaly": false,
      "severity": 12.5
    }],
    "temperature_sensors": [{
      "device_id": "temp_sensor_1",
      "timestamp": "2025-11-29T10:30:00",
      "temperature_c": 22.3,
      "humidity_percent": 48.5,
      "hvac_status": "idle"
    }],
    "occupancy_sensors": [{
      "device_id": "occupancy_sensor_1",
      "timestamp": "2025-11-29T10:30:00",
      "people_count": 8,
      "occupancy_rate": 0.75,
      "motion_detected": true
    }],
    "water_meters": [{
      "device_id": "water_meter_1",
      "timestamp": "2025-11-29T10:30:00",
      "flow_rate_lpm": 1.8,
      "total_liters": 125.5,
      "leak_detected": false
    }]
  },
  "kpi": {
    "total_energy": 126.5,
    "total_carbon": 38.0,
    "anomalies": 1,
    "active_devices": 5,
    "avg_temperature": 22.1,
    "avg_occupancy": 0.72
  },
  "timestamp": "2025-11-29T10:30:00"
}
```

#### GET `/energy/historical/<user_id>?hours=24`
Get historical energy consumption data.

**Query Parameters:**
- `hours` (optional): Number of hours of history (default: 24)

**Response:**
```json
{
  "historical_data": [{
    "timestamp": "2025-11-28T10:00:00",
    "total_energy_kwh": 120.5,
    "total_carbon_kg": 36.2,
    "hour": 10
  }],
  "count": 24
}
```

#### GET `/energy/predict/<user_id>?forecast_hours=24`
Predict future energy demand.

**Query Parameters:**
- `forecast_hours` (optional): Hours to forecast (default: 24)

**Response:**
```json
{
  "predictions": [{
    "timestamp": "2025-11-29T11:00:00",
    "predicted_energy_kwh": 128.3,
    "confidence": "medium"
  }],
  "forecast_hours": 24
}
```

#### GET `/energy/optimize/<user_id>`
Get energy optimization recommendations.

**Response:**
```json
{
  "recommendations": [{
    "category": "Peak Load Management",
    "priority": "High",
    "recommendation": "Consider load shifting during peak hours",
    "potential_savings_kwh": 15.5,
    "potential_savings_percent": 15
  }],
  "total_savings_potential_kwh": 45.2,
  "total_savings_potential_cost": 5.42,
  "roi_months": 18
}
```

#### GET `/energy/carbon_footprint/<user_id>`
Calculate comprehensive carbon footprint.

**Response:**
```json
{
  "total_kwh": 126.5,
  "total_carbon_kg": 38.0,
  "total_carbon_tons": 0.038,
  "carbon_intensity": 0.3,
  "equivalent_trees": 1.8,
  "equivalent_km_driven": 316.7
}
```

#### GET `/energy/sustainability_score/<user_id>`
Get overall sustainability score.

**Response:**
```json
{
  "overall_score": 78.5,
  "grade": "B+",
  "factors": [
    ["Energy Efficiency", 82.3],
    ["Carbon Footprint", 75.1]
  ],
  "benchmark": "Industry Average"
}
```

#### GET `/energy/esg_report/<user_id>?timeframe=monthly`
Generate comprehensive ESG report.

**Query Parameters:**
- `timeframe` (optional): "monthly", "quarterly", or "yearly" (default: "monthly")

**Response:**
```json
{
  "report_date": "2025-11-29T10:30:00",
  "timeframe": "monthly",
  "environmental": {
    "energy_consumption_kwh": 3795.0,
    "carbon_emissions_kg": 1140.0,
    "renewable_energy_percent": 15,
    "waste_reduction_percent": 8,
    "water_usage_liters": 1500
  },
  "social": {
    "employee_satisfaction": 4.2,
    "safety_incidents": 0,
    "training_hours": 120
  },
  "governance": {
    "compliance_score": 95,
    "audit_status": "Passed",
    "policy_updates": 3
  },
  "sustainability_initiatives": [
    "LED lighting upgrade completed",
    "Smart HVAC system implementation"
  ],
  "next_steps": [
    "Install solar panels",
    "Achieve carbon neutrality by 2030"
  ]
}
```

#### GET `/energy/metrics/<user_id>?period=day`
Get aggregated metrics from database.

**Query Parameters:**
- `period` (optional): "day", "week", or "month" (default: "day")

**Response:**
```json
{
  "period": "day",
  "device_count": 5,
  "total_energy_kwh": 126.5,
  "avg_energy_kwh": 25.3,
  "peak_energy_kwh": 42.1,
  "total_carbon_kg": 38.0,
  "avg_temperature_c": 22.1,
  "avg_humidity_percent": 48.5,
  "avg_occupancy_rate": 0.72
}
```

---

### 3. Billing & Subscription (`/billing`)

#### GET `/billing/plans`
Get available subscription plans.

**Response:**
```json
{
  "basic": {
    "price": 29,
    "features": ["5 devices", "Basic analytics", "Email support"]
  },
  "pro": {
    "price": 99,
    "features": ["20 devices", "Advanced AI", "Real-time alerts", "API access"]
  },
  "enterprise": {
    "price": 299,
    "features": ["Unlimited devices", "Custom ML models", "24/7 support", "SLA"]
  }
}
```

#### GET `/billing/get_plan/<user_id>`
Get user's current plan.

**Response:**
```json
{
  "plan": "pro",
  "devices_limit": 20
}
```

#### POST `/billing/upgrade`
Upgrade user subscription.

**Request:**
```json
{
  "user_id": "user1",
  "new_plan": "pro"
}
```

**Response:**
```json
{
  "status": "success",
  "new_plan": "pro"
}
```

---

### 4. ESG Compliance (`/esg`)

#### POST `/esg/upload`
Upload and analyze ESG document.

**Request:** Multipart form data with file upload

**Response:**
```json
{
  "filename": "sample_esg_report.csv",
  "kpis": {
    "energy": 1250.5,
    "carbon": 375.2,
    "waste": 85.0,
    "water": 1500.0
  }
}
```

---

## Data Models

### Energy Reading
```json
{
  "device_id": "string",
  "timestamp": "ISO 8601 datetime",
  "energy_kwh": "float",
  "voltage_v": "float",
  "current_a": "float",
  "power_factor": "float (0-1)",
  "carbon_kg": "float",
  "carbon_intensity": "float",
  "anomaly": "boolean",
  "severity": "float (0-100)"
}
```

### Temperature Reading
```json
{
  "device_id": "string",
  "timestamp": "ISO 8601 datetime",
  "temperature_c": "float",
  "humidity_percent": "float",
  "hvac_status": "string (on/idle/off)"
}
```

### Occupancy Reading
```json
{
  "device_id": "string",
  "timestamp": "ISO 8601 datetime",
  "people_count": "integer",
  "occupancy_rate": "float (0-1)",
  "motion_detected": "boolean"
}
```

---

## Authentication
Currently using simple user_id/password authentication. In production, implement:
- JWT tokens
- OAuth 2.0
- API keys for external integrations

---

## Rate Limiting
- Basic plan: 100 requests/hour
- Pro plan: 1000 requests/hour
- Enterprise plan: Unlimited

---

## Error Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Resource Not Found
- `500`: Internal Server Error

---

## Example Integration

### Python Client
```python
import requests

BASE_URL = "http://localhost:5000"

# Login
response = requests.post(f"{BASE_URL}/users/login", json={
    "user_id": "user1",
    "password": "password1"
})

# Get sensor data
data = requests.get(f"{BASE_URL}/energy/sensor_data/user1").json()
print(f"Total Energy: {data['kpi']['total_energy']} kWh")

# Get predictions
predictions = requests.get(
    f"{BASE_URL}/energy/predict/user1?forecast_hours=48"
).json()
```

### JavaScript Client
```javascript
const BASE_URL = 'http://localhost:5000';

// Get sensor data
fetch(`${BASE_URL}/energy/sensor_data/user1`)
  .then(response => response.json())
  .then(data => {
    console.log('Total Energy:', data.kpi.total_energy);
  });
```

---

## Support
For technical support, contact: support@sustainability-saas.com

**Documentation Version:** 1.0  
**Last Updated:** November 29, 2025
