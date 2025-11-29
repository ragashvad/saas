# backend/supply_chain.py
"""
Supply Chain & Scope 3 Emissions Module (Pulsora-inspired)
Tracks supplier emissions, value chain analytics, and Scope 3 calculations
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import random

supply_chain_bp = Blueprint('supply_chain', __name__)

# Mock supplier data
SUPPLIERS = {
    "user1": [
        {"id": "SUP001", "name": "Energy Provider Corp", "category": "Utilities", "emissions_kg": 15000, "status": "verified"},
        {"id": "SUP002", "name": "Raw Materials Ltd", "category": "Materials", "emissions_kg": 8500, "status": "pending"},
        {"id": "SUP003", "name": "Logistics Express", "category": "Transportation", "emissions_kg": 12300, "status": "verified"},
    ],
    "user2": [
        {"id": "SUP001", "name": "Energy Provider Corp", "category": "Utilities", "emissions_kg": 45000, "status": "verified"},
        {"id": "SUP002", "name": "Raw Materials Ltd", "category": "Materials", "emissions_kg": 25500, "status": "verified"},
        {"id": "SUP003", "name": "Logistics Express", "category": "Transportation", "emissions_kg": 36900, "status": "verified"},
        {"id": "SUP004", "name": "Manufacturing Co", "category": "Production", "emissions_kg": 28000, "status": "verified"},
        {"id": "SUP005", "name": "Packaging Solutions", "category": "Materials", "emissions_kg": 12000, "status": "pending"},
        {"id": "SUP006", "name": "IT Services Inc", "category": "Services", "emissions_kg": 3500, "status": "verified"},
    ]
}

@supply_chain_bp.route('/suppliers/<user_id>', methods=['GET'])
def get_suppliers(user_id):
    """Get supplier list with emissions data"""
    suppliers = SUPPLIERS.get(user_id, SUPPLIERS["user1"])
    
    total_emissions = sum(s['emissions_kg'] for s in suppliers)
    verified_count = sum(1 for s in suppliers if s['status'] == 'verified')
    
    # Calculate by category
    by_category = {}
    for supplier in suppliers:
        cat = supplier['category']
        if cat not in by_category:
            by_category[cat] = {'count': 0, 'emissions': 0}
        by_category[cat]['count'] += 1
        by_category[cat]['emissions'] += supplier['emissions_kg']
    
    return jsonify({
        'suppliers': suppliers,
        'total_suppliers': len(suppliers),
        'total_emissions_kg': total_emissions,
        'verified_suppliers': verified_count,
        'by_category': by_category
    })

@supply_chain_bp.route('/scope3/<user_id>', methods=['GET'])
def get_scope3_emissions(user_id):
    """Calculate Scope 3 emissions breakdown"""
    
    # Scope 3 categories (GHG Protocol)
    scope3_data = {
        'categories': [
            {'id': 1, 'name': 'Purchased Goods & Services', 'emissions_kg': 25000, 'percentage': 35},
            {'id': 2, 'name': 'Capital Goods', 'emissions_kg': 8000, 'percentage': 11},
            {'id': 3, 'name': 'Fuel & Energy Activities', 'emissions_kg': 15000, 'percentage': 21},
            {'id': 4, 'name': 'Upstream Transportation', 'emissions_kg': 12000, 'percentage': 17},
            {'id': 5, 'name': 'Waste Generated', 'emissions_kg': 3000, 'percentage': 4},
            {'id': 6, 'name': 'Business Travel', 'emissions_kg': 5000, 'percentage': 7},
            {'id': 7, 'name': 'Employee Commuting', 'emissions_kg': 3500, 'percentage': 5},
        ],
        'total_scope3_kg': 71500,
        'data_quality': {
            'primary_data': 45,  # percentage
            'secondary_data': 35,
            'estimated_data': 20
        },
        'comparison': {
            'scope1': 12000,
            'scope2': 38000,
            'scope3': 71500
        }
    }
    
    # Adjust for user tier
    if user_id == "user2":
        scope3_data['total_scope3_kg'] *= 3
        for cat in scope3_data['categories']:
            cat['emissions_kg'] *= 3
        scope3_data['comparison']['scope1'] *= 3
        scope3_data['comparison']['scope2'] *= 3
        scope3_data['comparison']['scope3'] *= 3
    
    return jsonify(scope3_data)

@supply_chain_bp.route('/value_chain/<user_id>', methods=['GET'])
def get_value_chain_analytics(user_id):
    """Value chain emissions analytics"""
    
    value_chain = {
        'upstream': {
            'total_emissions_kg': 45000,
            'suppliers_count': len(SUPPLIERS.get(user_id, SUPPLIERS["user1"])),
            'hotspots': [
                {'name': 'Raw Material Extraction', 'emissions_kg': 18000, 'reduction_potential': 25},
                {'name': 'Manufacturing', 'emissions_kg': 15000, 'reduction_potential': 15},
                {'name': 'Transportation', 'emissions_kg': 12000, 'reduction_potential': 30}
            ]
        },
        'operations': {
            'total_emissions_kg': 50000,
            'facilities_count': 3,
            'breakdown': [
                {'facility': 'Main Plant', 'emissions_kg': 25000},
                {'facility': 'Warehouse A', 'emissions_kg': 15000},
                {'facility': 'Office HQ', 'emissions_kg': 10000}
            ]
        },
        'downstream': {
            'total_emissions_kg': 28000,
            'categories': [
                {'name': 'Product Use', 'emissions_kg': 18000},
                {'name': 'End-of-Life', 'emissions_kg': 10000}
            ]
        },
        'total_value_chain_kg': 123000,
        'reduction_roadmap': [
            {'year': 2025, 'target_reduction': 10, 'initiatives': 3},
            {'year': 2026, 'target_reduction': 25, 'initiatives': 5},
            {'year': 2027, 'target_reduction': 40, 'initiatives': 7},
            {'year': 2030, 'target_reduction': 65, 'initiatives': 12}
        ]
    }
    
    return jsonify(value_chain)

@supply_chain_bp.route('/supplier_engagement/<user_id>', methods=['GET'])
def get_supplier_engagement(user_id):
    """Supplier engagement and data collection status"""
    
    suppliers = SUPPLIERS.get(user_id, SUPPLIERS["user1"])
    
    engagement_data = {
        'response_rate': 75,  # percentage
        'data_completeness': 68,
        'avg_response_time_days': 12,
        'suppliers': [
            {
                **supplier,
                'last_updated': f"2025-{random.randint(10, 11)}-{random.randint(1, 28):02d}",
                'data_quality_score': random.randint(70, 95),
                'engagement_level': random.choice(['High', 'Medium', 'Low'])
            }
            for supplier in suppliers
        ],
        'outstanding_requests': [
            {'supplier': 'Raw Materials Ltd', 'request_type': 'Emissions Data', 'days_overdue': 5},
            {'supplier': 'Packaging Solutions', 'request_type': 'Energy Consumption', 'days_overdue': 12}
        ]
    }
    
    return jsonify(engagement_data)

@supply_chain_bp.route('/reduction_opportunities/<user_id>', methods=['GET'])
def get_reduction_opportunities(user_id):
    """Identify emission reduction opportunities in supply chain"""
    
    opportunities = {
        'high_impact': [
            {
                'category': 'Supplier Engagement',
                'opportunity': 'Switch to renewable energy suppliers',
                'potential_reduction_kg': 12000,
                'cost_impact': 'Neutral',
                'timeframe': '6 months',
                'difficulty': 'Medium'
            },
            {
                'category': 'Transportation',
                'opportunity': 'Optimize logistics routes and consolidate shipments',
                'potential_reduction_kg': 8500,
                'cost_impact': 'Savings',
                'timeframe': '3 months',
                'difficulty': 'Low'
            },
            {
                'category': 'Materials',
                'opportunity': 'Source lower-carbon materials',
                'potential_reduction_kg': 6000,
                'cost_impact': 'Increase 5%',
                'timeframe': '12 months',
                'difficulty': 'High'
            }
        ],
        'quick_wins': [
            {
                'opportunity': 'Digital supplier engagement platform',
                'reduction_kg': 500,
                'implementation_time': '1 month'
            },
            {
                'opportunity': 'Optimize packaging materials',
                'reduction_kg': 1200,
                'implementation_time': '2 months'
            }
        ],
        'total_potential_reduction_kg': 28200,
        'total_potential_reduction_percent': 23
    }
    
    return jsonify(opportunities)
