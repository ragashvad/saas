# backend/data_storage.py
"""
Data Integration Layer
Handles data persistence and time-series storage
"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import sqlite3
from pathlib import Path

class DataStore:
    """Simple data storage using SQLite for persistence"""
    
    def __init__(self, db_path='data/sustainability.db'):
        self.db_path = db_path
        Path(os.path.dirname(db_path)).mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Energy readings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                energy_kwh REAL,
                voltage_v REAL,
                current_a REAL,
                power_factor REAL,
                carbon_kg REAL,
                carbon_intensity REAL
            )
        ''')
        
        # Temperature readings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                temperature_c REAL,
                humidity_percent REAL,
                hvac_status TEXT
            )
        ''')
        
        # Occupancy readings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS occupancy_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                people_count INTEGER,
                occupancy_rate REAL,
                motion_detected INTEGER
            )
        ''')
        
        # Water readings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS water_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                flow_rate_lpm REAL,
                total_liters REAL,
                leak_detected INTEGER
            )
        ''')
        
        # Sustainability metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sustainability_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                total_energy_kwh REAL,
                total_carbon_kg REAL,
                sustainability_score REAL,
                grade TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_energy_reading(self, user_id, reading):
        """Store energy meter reading"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO energy_readings 
            (user_id, device_id, timestamp, energy_kwh, voltage_v, current_a, 
             power_factor, carbon_kg, carbon_intensity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            reading.get('device_id'),
            reading.get('timestamp'),
            reading.get('energy_kwh'),
            reading.get('voltage_v'),
            reading.get('current_a'),
            reading.get('power_factor'),
            reading.get('carbon_kg'),
            reading.get('carbon_intensity')
        ))
        
        conn.commit()
        conn.close()
    
    def store_temperature_reading(self, user_id, reading):
        """Store temperature sensor reading"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO temperature_readings 
            (user_id, device_id, timestamp, temperature_c, humidity_percent, hvac_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            reading.get('device_id'),
            reading.get('timestamp'),
            reading.get('temperature_c'),
            reading.get('humidity_percent'),
            reading.get('hvac_status')
        ))
        
        conn.commit()
        conn.close()
    
    def store_occupancy_reading(self, user_id, reading):
        """Store occupancy sensor reading"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO occupancy_readings 
            (user_id, device_id, timestamp, people_count, occupancy_rate, motion_detected)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            reading.get('device_id'),
            reading.get('timestamp'),
            reading.get('people_count'),
            reading.get('occupancy_rate'),
            1 if reading.get('motion_detected') else 0
        ))
        
        conn.commit()
        conn.close()
    
    def get_energy_history(self, user_id, hours=24):
        """Retrieve energy consumption history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        cursor.execute('''
            SELECT timestamp, SUM(energy_kwh) as total_energy, SUM(carbon_kg) as total_carbon
            FROM energy_readings
            WHERE user_id = ? AND timestamp > ?
            GROUP BY timestamp
            ORDER BY timestamp
        ''', (user_id, cutoff))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'timestamp': row[0],
                'total_energy_kwh': round(row[1], 2),
                'total_carbon_kg': round(row[2], 2)
            }
            for row in rows
        ]
    
    def get_aggregated_metrics(self, user_id, period='day'):
        """Get aggregated sustainability metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if period == 'day':
            hours = 24
        elif period == 'week':
            hours = 168
        elif period == 'month':
            hours = 720
        else:
            hours = 24
        
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # Energy metrics
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT device_id) as device_count,
                SUM(energy_kwh) as total_energy,
                AVG(energy_kwh) as avg_energy,
                MAX(energy_kwh) as peak_energy,
                SUM(carbon_kg) as total_carbon
            FROM energy_readings
            WHERE user_id = ? AND timestamp > ?
        ''', (user_id, cutoff))
        
        energy_row = cursor.fetchone()
        
        # Temperature metrics
        cursor.execute('''
            SELECT 
                AVG(temperature_c) as avg_temp,
                AVG(humidity_percent) as avg_humidity
            FROM temperature_readings
            WHERE user_id = ? AND timestamp > ?
        ''', (user_id, cutoff))
        
        temp_row = cursor.fetchone()
        
        # Occupancy metrics
        cursor.execute('''
            SELECT 
                AVG(occupancy_rate) as avg_occupancy
            FROM occupancy_readings
            WHERE user_id = ? AND timestamp > ?
        ''', (user_id, cutoff))
        
        occupancy_row = cursor.fetchone()
        
        conn.close()
        
        return {
            'period': period,
            'device_count': energy_row[0] or 0,
            'total_energy_kwh': round(energy_row[1] or 0, 2),
            'avg_energy_kwh': round(energy_row[2] or 0, 2),
            'peak_energy_kwh': round(energy_row[3] or 0, 2),
            'total_carbon_kg': round(energy_row[4] or 0, 2),
            'avg_temperature_c': round(temp_row[0] or 22, 1) if temp_row else 22,
            'avg_humidity_percent': round(temp_row[1] or 50, 1) if temp_row else 50,
            'avg_occupancy_rate': round(occupancy_row[0] or 0, 2) if occupancy_row else 0
        }
    
    def store_sustainability_score(self, user_id, score_data):
        """Store sustainability score"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sustainability_metrics 
            (user_id, timestamp, total_energy_kwh, total_carbon_kg, 
             sustainability_score, grade)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            datetime.now().isoformat(),
            score_data.get('total_energy_kwh', 0),
            score_data.get('total_carbon_kg', 0),
            score_data.get('overall_score', 0),
            score_data.get('grade', 'N/A')
        ))
        
        conn.commit()
        conn.close()
    
    def clear_old_data(self, days=90):
        """Clear data older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        for table in ['energy_readings', 'temperature_readings', 
                      'occupancy_readings', 'water_readings']:
            cursor.execute(f'DELETE FROM {table} WHERE timestamp < ?', (cutoff,))
        
        conn.commit()
        conn.close()

# Global data store instance
data_store = DataStore()
