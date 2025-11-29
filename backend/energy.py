# backend/energy.py
from flask import Blueprint, jsonify, request
from iot_simulator import simulator
from advanced_analytics import analytics_engine
from data_storage import data_store

energy_bp = Blueprint('energy', __name__)

@energy_bp.route('/sensor_data/<user_id>', methods=['GET'])
def get_sensor_data(user_id):
    """Get real-time sensor data from all IoT devices"""
    # Get live sensor readings
    sensor_data = simulator.get_all_sensor_data()
    
    # Store readings in database
    for reading in sensor_data['energy_meters']:
        data_store.store_energy_reading(user_id, reading)
    for reading in sensor_data['temperature_sensors']:
        data_store.store_temperature_reading(user_id, reading)
    for reading in sensor_data['occupancy_sensors']:
        data_store.store_occupancy_reading(user_id, reading)
    
    # Detect anomalies
    anomaly_flags, severity_scores = analytics_engine.detect_anomalies(
        sensor_data['energy_meters']
    )
    
    # Add anomaly info to energy readings
    for i, reading in enumerate(sensor_data['energy_meters']):
        reading['anomaly'] = bool(anomaly_flags[i])
        reading['severity'] = round(float(severity_scores[i]), 1)
    
    # Calculate KPIs
    total_energy = sum(d['energy_kwh'] for d in sensor_data['energy_meters'])
    total_carbon = sum(d['carbon_kg'] for d in sensor_data['energy_meters'])
    
    kpi = {
        "total_energy": round(float(total_energy), 2),
        "total_carbon": round(float(total_carbon), 2),
        "anomalies": int(sum(anomaly_flags)),
        "active_devices": int(len(sensor_data['energy_meters'])),
        "avg_temperature": round(float(
            sum(d['temperature_c'] for d in sensor_data['temperature_sensors']) / 
            len(sensor_data['temperature_sensors'])), 1
        ),
        "avg_occupancy": round(float(
            sum(d['occupancy_rate'] for d in sensor_data['occupancy_sensors']) / 
            len(sensor_data['occupancy_sensors'])), 2
        )
    }
    
    return jsonify({
        "raw": sensor_data,
        "kpi": kpi,
        "timestamp": sensor_data['timestamp']
    })

@energy_bp.route('/historical/<user_id>', methods=['GET'])
def get_historical_data(user_id):
    """Get historical energy consumption data"""
    hours = request.args.get('hours', default=24, type=int)
    
    # Get historical data from simulator
    historical = simulator.get_historical_data(days=hours//24 or 1)
    
    return jsonify({
        "historical_data": historical,
        "count": len(historical)
    })

@energy_bp.route('/predict/<user_id>', methods=['GET'])
def predict_energy(user_id):
    """Predict future energy demand"""
    hours = request.args.get('forecast_hours', default=24, type=int)
    
    # Get historical data
    historical = simulator.get_historical_data(days=2)
    
    # Generate predictions
    predictions = analytics_engine.predict_energy_demand(historical, forecast_hours=hours)
    
    return jsonify({
        "predictions": predictions,
        "forecast_hours": hours
    })

@energy_bp.route('/optimize/<user_id>', methods=['GET'])
def get_optimization(user_id):
    """Get energy optimization recommendations"""
    # Get current sensor data
    sensor_data = simulator.get_all_sensor_data()
    
    # Generate optimization recommendations
    optimization = analytics_engine.optimize_energy_usage(
        sensor_data['energy_meters'],
        sensor_data['occupancy_sensors'],
        sensor_data['temperature_sensors']
    )
    
    return jsonify(optimization)

@energy_bp.route('/carbon_footprint/<user_id>', methods=['GET'])
def get_carbon_footprint(user_id):
    """Calculate comprehensive carbon footprint"""
    sensor_data = simulator.get_all_sensor_data()
    
    carbon_data = analytics_engine.calculate_carbon_footprint(
        sensor_data['energy_meters']
    )
    
    return jsonify(carbon_data)

@energy_bp.route('/sustainability_score/<user_id>', methods=['GET'])
def get_sustainability_score(user_id):
    """Get overall sustainability score"""
    sensor_data = simulator.get_all_sensor_data()
    carbon_data = analytics_engine.calculate_carbon_footprint(
        sensor_data['energy_meters']
    )
    
    score = analytics_engine.calculate_sustainability_score(
        sensor_data['energy_meters'],
        carbon_data,
        sensor_data.get('water_meters')
    )
    
    # Store score in database
    data_store.store_sustainability_score(user_id, {
        'total_energy_kwh': sum(d['energy_kwh'] for d in sensor_data['energy_meters']),
        'total_carbon_kg': carbon_data['total_carbon_kg'],
        'overall_score': score['overall_score'],
        'grade': score['grade']
    })
    
    return jsonify(score)

@energy_bp.route('/esg_report/<user_id>', methods=['GET'])
def get_esg_report(user_id):
    """Generate comprehensive ESG report"""
    sensor_data = simulator.get_all_sensor_data()
    carbon_data = analytics_engine.calculate_carbon_footprint(
        sensor_data['energy_meters']
    )
    
    timeframe = request.args.get('timeframe', default='monthly', type=str)
    
    report = analytics_engine.generate_esg_report(
        sensor_data['energy_meters'],
        carbon_data,
        timeframe=timeframe
    )
    
    return jsonify(report)

@energy_bp.route('/metrics/<user_id>', methods=['GET'])
def get_aggregated_metrics(user_id):
    """Get aggregated metrics from database"""
    period = request.args.get('period', default='day', type=str)
    
    metrics = data_store.get_aggregated_metrics(user_id, period=period)
    
    return jsonify(metrics)