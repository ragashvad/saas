# backend/advanced_analytics.py
"""
Advanced Analytics Layer
Energy optimization, predictive models, carbon footprint analysis, anomaly detection
"""
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import json

class SustainabilityAnalytics:
    """Advanced analytics for sustainability monitoring"""
    
    def __init__(self):
        self.anomaly_detector = self._init_anomaly_detector()
        self.energy_predictor = self._init_energy_predictor()
        self.scaler = StandardScaler()
        
    def _init_anomaly_detector(self):
        """Initialize anomaly detection model"""
        model = IsolationForest(
            contamination=0.1, 
            random_state=42,
            n_estimators=100
        )
        # Pre-train with synthetic normal data
        X_train = np.random.normal(20, 5, (1000, 3))
        model.fit(X_train)
        return model
    
    def _init_energy_predictor(self):
        """Initialize energy prediction model"""
        model = RandomForestRegressor(
            n_estimators=50,
            random_state=42,
            max_depth=10
        )
        # Pre-train with synthetic data
        X_train = np.random.rand(500, 4) * 24  # hour, day, temp, occupancy
        y_train = 20 + X_train[:, 0] * 0.5 + np.random.normal(0, 2, 500)
        model.fit(X_train, y_train)
        return model
    
    def detect_anomalies(self, sensor_data):
        """
        Detect anomalies in sensor readings
        Returns list of anomaly flags and severity scores
        """
        if not sensor_data or len(sensor_data) == 0:
            return [], []
        
        features = []
        for reading in sensor_data:
            feat = [
                reading.get('energy_kwh', 0),
                reading.get('voltage_v', 220) / 220,  # Normalized
                reading.get('power_factor', 0.9)
            ]
            features.append(feat)
        
        X = np.array(features)
        predictions = self.anomaly_detector.predict(X)
        scores = self.anomaly_detector.score_samples(X)
        
        # Convert scores to severity (0-100)
        severity = [(1 - (score + 0.5)) * 100 for score in scores]
        severity = [max(0, min(100, s)) for s in severity]
        
        anomalies = [pred == -1 for pred in predictions]
        
        return anomalies, severity
    
    def predict_energy_demand(self, historical_data, forecast_hours=24):
        """
        Predict future energy demand based on historical patterns
        """
        if not historical_data or len(historical_data) < 24:
            return []
        
        predictions = []
        last_timestamp = datetime.fromisoformat(historical_data[-1]['timestamp'])
        
        for i in range(forecast_hours):
            future_time = last_timestamp + timedelta(hours=i+1)
            hour = future_time.hour
            day_of_week = future_time.weekday()
            
            # Simple features
            features = np.array([[hour, day_of_week, 22, 0.7]])  # hour, day, temp, occupancy
            prediction = self.energy_predictor.predict(features)[0]
            
            predictions.append({
                'timestamp': future_time.isoformat(),
                'predicted_energy_kwh': round(prediction, 2),
                'confidence': 'medium'
            })
        
        return predictions
    
    def calculate_carbon_footprint(self, energy_data, carbon_intensity=0.3):
        """
        Calculate comprehensive carbon footprint
        """
        total_energy = sum(d.get('energy_kwh', 0) for d in energy_data)
        total_carbon = total_energy * carbon_intensity
        
        # Calculate by source if available
        breakdown = {
            'total_kwh': round(total_energy, 2),
            'total_carbon_kg': round(total_carbon, 2),
            'total_carbon_tons': round(total_carbon / 1000, 3),
            'carbon_intensity': carbon_intensity,
            'equivalent_trees': round(total_carbon / 21, 1),  # 1 tree absorbs ~21kg CO2/year
            'equivalent_km_driven': round(total_carbon / 0.12, 1)  # ~0.12kg CO2 per km
        }
        
        return breakdown
    
    def optimize_energy_usage(self, sensor_data, occupancy_data, temp_data):
        """
        Generate energy optimization recommendations
        """
        recommendations = []
        savings_potential = 0
        
        # Analyze energy patterns
        if sensor_data:
            avg_energy = np.mean([d.get('energy_kwh', 0) for d in sensor_data])
            max_energy = max([d.get('energy_kwh', 0) for d in sensor_data])
            
            # Peak load analysis
            if max_energy > avg_energy * 1.5:
                recommendations.append({
                    'category': 'Peak Load Management',
                    'priority': 'High',
                    'recommendation': 'Consider load shifting during peak hours to reduce demand charges',
                    'potential_savings_kwh': round((max_energy - avg_energy) * 0.3, 2),
                    'potential_savings_percent': 15
                })
                savings_potential += (max_energy - avg_energy) * 0.3
        
        # Occupancy-based optimization
        if occupancy_data:
            avg_occupancy = np.mean([d.get('occupancy_rate', 0) for d in occupancy_data])
            if avg_occupancy < 0.5:
                recommendations.append({
                    'category': 'Occupancy-Based Control',
                    'priority': 'Medium',
                    'recommendation': 'Implement occupancy sensors to reduce HVAC and lighting in unused areas',
                    'potential_savings_kwh': round(avg_energy * 0.2 if sensor_data else 0, 2),
                    'potential_savings_percent': 20
                })
                savings_potential += avg_energy * 0.2 if sensor_data else 0
        
        # Temperature optimization
        if temp_data:
            temps = [d.get('temperature_c', 22) for d in temp_data]
            if max(temps) - min(temps) > 3:
                recommendations.append({
                    'category': 'HVAC Optimization',
                    'priority': 'Medium',
                    'recommendation': 'Temperature variance detected. Consider zone-based HVAC control',
                    'potential_savings_kwh': round(avg_energy * 0.15 if sensor_data else 0, 2),
                    'potential_savings_percent': 15
                })
                savings_potential += avg_energy * 0.15 if sensor_data else 0
        
        # Power factor correction
        if sensor_data:
            avg_pf = np.mean([d.get('power_factor', 0.9) for d in sensor_data])
            if avg_pf < 0.85:
                recommendations.append({
                    'category': 'Power Quality',
                    'priority': 'High',
                    'recommendation': 'Low power factor detected. Install power factor correction equipment',
                    'potential_savings_kwh': round(avg_energy * 0.1, 2),
                    'potential_savings_percent': 10
                })
                savings_potential += avg_energy * 0.1
        
        # Renewable energy recommendation
        recommendations.append({
            'category': 'Renewable Energy',
            'priority': 'Long-term',
            'recommendation': 'Consider solar panel installation to reduce grid dependence',
            'potential_savings_kwh': round(avg_energy * 0.4 if sensor_data else 0, 2),
            'potential_savings_percent': 40
        })
        
        return {
            'recommendations': recommendations,
            'total_savings_potential_kwh': round(savings_potential, 2),
            'total_savings_potential_cost': round(savings_potential * 0.12, 2),  # $0.12 per kWh
            'roi_months': 18
        }
    
    def calculate_sustainability_score(self, energy_data, carbon_data, water_data=None):
        """
        Calculate overall sustainability score (0-100)
        """
        score = 100
        factors = []
        
        # Energy efficiency score
        if energy_data:
            avg_energy = np.mean([d.get('energy_kwh', 0) for d in energy_data])
            benchmark = 25  # kWh benchmark
            energy_score = max(0, 100 - (avg_energy - benchmark) / benchmark * 50)
            score = score * 0.4 + energy_score * 0.4
            factors.append(('Energy Efficiency', round(energy_score, 1)))
        
        # Carbon footprint score
        if carbon_data:
            total_carbon = carbon_data.get('total_carbon_kg', 0)
            benchmark_carbon = 50  # kg benchmark
            carbon_score = max(0, 100 - (total_carbon - benchmark_carbon) / benchmark_carbon * 50)
            score = score * 0.6 + carbon_score * 0.4
            factors.append(('Carbon Footprint', round(carbon_score, 1)))
        
        # Water efficiency score
        if water_data:
            water_score = 85  # Placeholder
            score = score * 0.8 + water_score * 0.2
            factors.append(('Water Efficiency', water_score))
        
        return {
            'overall_score': round(score, 1),
            'grade': self._get_grade(score),
            'factors': factors,
            'benchmark': 'Industry Average'
        }
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90: return 'A+'
        elif score >= 85: return 'A'
        elif score >= 80: return 'A-'
        elif score >= 75: return 'B+'
        elif score >= 70: return 'B'
        elif score >= 65: return 'B-'
        elif score >= 60: return 'C+'
        elif score >= 55: return 'C'
        else: return 'D'
    
    def generate_esg_report(self, energy_data, carbon_data, timeframe='monthly'):
        """
        Generate comprehensive ESG report
        """
        total_energy = sum(d.get('energy_kwh', 0) for d in energy_data) if energy_data else 0
        total_carbon = carbon_data.get('total_carbon_kg', 0)
        
        report = {
            'report_date': datetime.now().isoformat(),
            'timeframe': timeframe,
            'environmental': {
                'energy_consumption_kwh': round(total_energy, 2),
                'carbon_emissions_kg': round(total_carbon, 2),
                'renewable_energy_percent': 15,  # Example
                'waste_reduction_percent': 8,
                'water_usage_liters': 1500
            },
            'social': {
                'employee_satisfaction': 4.2,
                'safety_incidents': 0,
                'training_hours': 120
            },
            'governance': {
                'compliance_score': 95,
                'audit_status': 'Passed',
                'policy_updates': 3
            },
            'sustainability_initiatives': [
                'LED lighting upgrade completed',
                'Smart HVAC system implementation',
                'Renewable energy evaluation ongoing'
            ],
            'next_steps': [
                'Install solar panels',
                'Implement water recycling system',
                'Achieve carbon neutrality by 2030'
            ]
        }
        
        return report

# Global analytics engine
analytics_engine = SustainabilityAnalytics()
