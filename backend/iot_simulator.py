# backend/iot_simulator.py
"""
IoT & Edge Layer Simulator
Simulates smart sensors: energy meters, temperature, occupancy, water usage
"""
import random
import time
from datetime import datetime, timedelta
import json

class IoTSensorSimulator:
    """Simulates various IoT sensors for sustainability monitoring"""
    
    def __init__(self, num_energy_meters=5, num_temp_sensors=3, num_occupancy_sensors=2):
        self.energy_meters = [f"energy_meter_{i+1}" for i in range(num_energy_meters)]
        self.temp_sensors = [f"temp_sensor_{i+1}" for i in range(num_temp_sensors)]
        self.occupancy_sensors = [f"occupancy_sensor_{i+1}" for i in range(num_occupancy_sensors)]
        self.water_meters = ["water_meter_1", "water_meter_2"]
        
    def generate_energy_reading(self, device_id, time_of_day=None):
        """Generate realistic energy meter reading"""
        if time_of_day is None:
            time_of_day = datetime.now().hour
        
        # Simulate daily patterns (higher during business hours)
        base_load = 15.0
        if 8 <= time_of_day <= 18:  # Business hours
            peak_factor = 1.5 + random.uniform(-0.2, 0.3)
        elif 18 <= time_of_day <= 22:  # Evening
            peak_factor = 1.2 + random.uniform(-0.1, 0.2)
        else:  # Night
            peak_factor = 0.6 + random.uniform(-0.1, 0.1)
        
        energy_kwh = base_load * peak_factor + random.gauss(0, 2)
        voltage = 220 + random.uniform(-5, 5)
        current = energy_kwh / voltage * 1000  # Approximate current
        power_factor = random.uniform(0.85, 0.95)
        
        # Carbon intensity (kg CO2 per kWh) - varies by time and renewable mix
        carbon_intensity = 0.3 + random.uniform(-0.05, 0.05)
        if 10 <= time_of_day <= 16:  # More solar during midday
            carbon_intensity *= 0.8
        
        return {
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "energy_kwh": round(energy_kwh, 2),
            "voltage_v": round(voltage, 2),
            "current_a": round(current, 2),
            "power_factor": round(power_factor, 3),
            "carbon_kg": round(energy_kwh * carbon_intensity, 2),
            "carbon_intensity": round(carbon_intensity, 3)
        }
    
    def generate_temperature_reading(self, device_id):
        """Generate temperature sensor reading"""
        # Simulate HVAC-controlled environment
        base_temp = 22.0  # Target temperature
        temp = base_temp + random.gauss(0, 1.5)
        humidity = 45 + random.gauss(0, 10)
        
        return {
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "temperature_c": round(temp, 1),
            "humidity_percent": round(max(20, min(80, humidity)), 1),
            "hvac_status": "on" if abs(temp - base_temp) > 2 else "idle"
        }
    
    def generate_occupancy_reading(self, device_id, time_of_day=None):
        """Generate occupancy sensor reading"""
        if time_of_day is None:
            time_of_day = datetime.now().hour
        
        # Simulate occupancy patterns
        if 9 <= time_of_day <= 17:  # Business hours
            occupancy_rate = random.uniform(0.6, 0.9)
        elif 7 <= time_of_day <= 9 or 17 <= time_of_day <= 19:
            occupancy_rate = random.uniform(0.3, 0.6)
        else:
            occupancy_rate = random.uniform(0.0, 0.2)
        
        people_count = int(occupancy_rate * random.randint(8, 12))
        
        return {
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "people_count": people_count,
            "occupancy_rate": round(occupancy_rate, 2),
            "motion_detected": people_count > 0
        }
    
    def generate_water_reading(self, device_id):
        """Generate water meter reading"""
        flow_rate = random.uniform(0.5, 3.0)  # L/min
        total_liters = random.uniform(50, 200)
        
        return {
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "flow_rate_lpm": round(flow_rate, 2),
            "total_liters": round(total_liters, 1),
            "leak_detected": flow_rate > 2.5
        }
    
    def get_all_sensor_data(self):
        """Get readings from all sensors"""
        current_hour = datetime.now().hour
        
        data = {
            "energy_meters": [
                self.generate_energy_reading(meter, current_hour) 
                for meter in self.energy_meters
            ],
            "temperature_sensors": [
                self.generate_temperature_reading(sensor) 
                for sensor in self.temp_sensors
            ],
            "occupancy_sensors": [
                self.generate_occupancy_reading(sensor, current_hour) 
                for sensor in self.occupancy_sensors
            ],
            "water_meters": [
                self.generate_water_reading(meter) 
                for meter in self.water_meters
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return data
    
    def get_historical_data(self, days=30, interval_hours=1):
        """Generate historical sensor data for time-series analysis"""
        history = []
        now = datetime.now()
        
        for i in range(days * 24 // interval_hours):
            timestamp = now - timedelta(hours=i * interval_hours)
            hour = timestamp.hour
            
            # Aggregate energy data
            total_energy = sum(
                self.generate_energy_reading(meter, hour)["energy_kwh"] 
                for meter in self.energy_meters
            )
            total_carbon = sum(
                self.generate_energy_reading(meter, hour)["carbon_kg"] 
                for meter in self.energy_meters
            )
            
            history.append({
                "timestamp": timestamp.isoformat(),
                "total_energy_kwh": round(total_energy, 2),
                "total_carbon_kg": round(total_carbon, 2),
                "hour": hour
            })
        
        return list(reversed(history))  # Oldest first

# Global simulator instance
simulator = IoTSensorSimulator()
