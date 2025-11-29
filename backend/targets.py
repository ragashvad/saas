# backend/targets.py
"""
Target Management & Progress Tracking (Pulsora-inspired)
Set climate targets, track progress, and plan reduction pathways
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import random

targets_bp = Blueprint('targets', __name__)

# Mock targets data
TARGETS = {
    "user1": {
        'primary_target': {
            'type': 'Net Zero',
            'baseline_year': 2020,
            'target_year': 2050,
            'baseline_emissions_kg': 150000,
            'current_emissions_kg': 126500,
            'reduction_achieved_percent': 15.7,
            'on_track': True
        },
        'interim_targets': [
            {'year': 2025, 'target_reduction': 20, 'current_progress': 15.7, 'status': 'On Track'},
            {'year': 2030, 'target_reduction': 40, 'current_progress': 15.7, 'status': 'Needs Action'},
            {'year': 2040, 'target_reduction': 70, 'current_progress': 15.7, 'status': 'Future'}
        ],
        'science_based': {
            'aligned': True,
            'framework': 'SBTi (1.5°C pathway)',
            'validation_status': 'Approved',
            'submission_date': '2024-03-15'
        }
    },
    "user2": {
        'primary_target': {
            'type': 'Carbon Neutral',
            'baseline_year': 2019,
            'target_year': 2035,
            'baseline_emissions_kg': 450000,
            'current_emissions_kg': 379500,
            'reduction_achieved_percent': 15.7,
            'on_track': True
        },
        'interim_targets': [
            {'year': 2025, 'target_reduction': 25, 'current_progress': 15.7, 'status': 'At Risk'},
            {'year': 2030, 'target_reduction': 50, 'current_progress': 15.7, 'status': 'Needs Action'},
            {'year': 2035, 'target_reduction': 100, 'current_progress': 15.7, 'status': 'Future'}
        ],
        'science_based': {
            'aligned': True,
            'framework': 'SBTi (Well Below 2°C)',
            'validation_status': 'In Review',
            'submission_date': '2024-08-20'
        }
    }
}

@targets_bp.route('/targets/<user_id>', methods=['GET'])
def get_targets(user_id):
    """Get climate targets and progress"""
    targets = TARGETS.get(user_id, TARGETS["user1"])
    
    # Calculate trajectory
    years_elapsed = 2025 - targets['primary_target']['baseline_year']
    years_total = targets['primary_target']['target_year'] - targets['primary_target']['baseline_year']
    expected_progress = (years_elapsed / years_total) * 100
    
    targets['trajectory_analysis'] = {
        'years_elapsed': years_elapsed,
        'years_remaining': years_total - years_elapsed,
        'expected_progress_percent': round(expected_progress, 1),
        'actual_progress_percent': targets['primary_target']['reduction_achieved_percent'],
        'ahead_behind': 'Ahead' if targets['primary_target']['reduction_achieved_percent'] > expected_progress else 'Behind'
    }
    
    return jsonify(targets)

@targets_bp.route('/reduction_pathway/<user_id>', methods=['GET'])
def get_reduction_pathway(user_id):
    """Get detailed reduction pathway and initiatives"""
    
    pathway = {
        'timeline': [
            {
                'year': 2025,
                'emissions_target_kg': 120000,
                'emissions_actual_kg': 126500,
                'initiatives': [
                    {'name': 'LED Lighting Upgrade', 'reduction_kg': 5000, 'status': 'Completed'},
                    {'name': 'Solar Panel Installation', 'reduction_kg': 15000, 'status': 'In Progress'},
                    {'name': 'Fleet Electrification Phase 1', 'reduction_kg': 8000, 'status': 'Planned'}
                ]
            },
            {
                'year': 2026,
                'emissions_target_kg': 105000,
                'emissions_actual_kg': None,
                'initiatives': [
                    {'name': 'Heat Pump Installation', 'reduction_kg': 12000, 'status': 'Planned'},
                    {'name': 'Supplier Engagement Program', 'reduction_kg': 18000, 'status': 'Planned'},
                    {'name': 'Waste-to-Energy System', 'reduction_kg': 6000, 'status': 'Under Review'}
                ]
            },
            {
                'year': 2027,
                'emissions_target_kg': 90000,
                'emissions_actual_kg': None,
                'initiatives': [
                    {'name': 'Building Automation System', 'reduction_kg': 10000, 'status': 'Planned'},
                    {'name': 'Renewable Energy PPA', 'reduction_kg': 25000, 'status': 'Planned'},
                    {'name': 'Circular Economy Initiative', 'reduction_kg': 8000, 'status': 'Planned'}
                ]
            }
        ],
        'by_category': {
            'Energy Efficiency': {'reduction_kg': 32000, 'percent': 35},
            'Renewable Energy': {'reduction_kg': 40000, 'percent': 44},
            'Electrification': {'reduction_kg': 8000, 'percent': 9},
            'Supply Chain': {'reduction_kg': 18000, 'percent': 20},
            'Waste Reduction': {'reduction_kg': 6000, 'percent': 7}
        },
        'investment_required': {
            'total_usd': 2500000,
            'by_year': [
                {'year': 2025, 'amount': 800000},
                {'year': 2026, 'amount': 950000},
                {'year': 2027, 'amount': 750000}
            ]
        }
    }
    
    return jsonify(pathway)

@targets_bp.route('/progress_tracking/<user_id>', methods=['GET'])
def get_progress_tracking(user_id):
    """Track progress against targets with detailed metrics"""
    
    progress = {
        'current_period': {
            'period': 'Q4 2025',
            'emissions_kg': 31625,  # Quarterly
            'target_kg': 30000,
            'variance_kg': 1625,
            'variance_percent': 5.4,
            'status': 'Slightly Over'
        },
        'ytd_performance': {
            'emissions_kg': 126500,
            'target_kg': 120000,
            'variance_kg': 6500,
            'variance_percent': 5.4,
            'initiatives_completed': 8,
            'initiatives_delayed': 2
        },
        'monthly_breakdown': [
            {'month': 'Jan', 'actual': 10800, 'target': 10000},
            {'month': 'Feb', 'actual': 9800, 'target': 10000},
            {'month': 'Mar', 'actual': 10500, 'target': 10000},
            {'month': 'Apr', 'actual': 10200, 'target': 10000},
            {'month': 'May', 'actual': 11000, 'target': 10000},
            {'month': 'Jun', 'actual': 10600, 'target': 10000},
            {'month': 'Jul', 'actual': 10900, 'target': 10000},
            {'month': 'Aug', 'actual': 10400, 'target': 10000},
            {'month': 'Sep', 'actual': 10300, 'target': 10000},
            {'month': 'Oct', 'actual': 10500, 'target': 10000},
            {'month': 'Nov', 'actual': 10200, 'target': 10000},
            {'month': 'Dec', 'actual': 11300, 'target': 10000}
        ],
        'key_drivers': [
            {'factor': 'Weather Impact', 'impact_kg': 3000, 'type': 'Increase'},
            {'factor': 'LED Upgrade', 'impact_kg': -5000, 'type': 'Decrease'},
            {'factor': 'Production Volume', 'impact_kg': 2500, 'type': 'Increase'},
            {'factor': 'Efficiency Improvements', 'impact_kg': -2000, 'type': 'Decrease'}
        ]
    }
    
    return jsonify(progress)

@targets_bp.route('/benchmarking/<user_id>', methods=['GET'])
def get_benchmarking(user_id):
    """Compare performance against industry benchmarks"""
    
    benchmarking = {
        'industry': 'Manufacturing',
        'company_size': 'Medium',
        'metrics': {
            'emissions_intensity': {
                'your_value': 2.5,  # kg CO2 per $ revenue
                'industry_avg': 3.2,
                'best_in_class': 1.8,
                'percentile': 68
            },
            'renewable_energy': {
                'your_value': 15,  # percent
                'industry_avg': 12,
                'best_in_class': 45,
                'percentile': 55
            },
            'scope3_coverage': {
                'your_value': 68,  # percent
                'industry_avg': 45,
                'best_in_class': 85,
                'percentile': 72
            },
            'target_ambition': {
                'your_value': 'SBTi 1.5°C',
                'industry_avg': 'SBTi 2°C',
                'best_in_class': 'Net Zero 2040',
                'percentile': 78
            }
        },
        'peer_comparison': {
            'better_than': 68,  # percent of peers
            'similar_to': 20,
            'worse_than': 12
        },
        'improvement_areas': [
            'Increase renewable energy usage',
            'Accelerate fleet electrification',
            'Enhance supplier engagement'
        ]
    }
    
    return jsonify(benchmarking)

@targets_bp.route('/carbon_budget/<user_id>', methods=['GET'])
def get_carbon_budget(user_id):
    """Calculate remaining carbon budget for target"""
    
    targets = TARGETS.get(user_id, TARGETS["user1"])
    current_year = 2025
    target_year = targets['primary_target']['target_year']
    years_remaining = target_year - current_year
    current_annual = targets['primary_target']['current_emissions_kg']
    
    # Simple linear reduction assumption
    total_budget = (current_annual * years_remaining) / 2  # Triangular area
    
    carbon_budget = {
        'total_budget_kg': int(total_budget),
        'years_remaining': years_remaining,
        'annual_budget_kg': int(total_budget / years_remaining),
        'current_annual_kg': current_annual,
        'required_reduction_rate_percent': round((current_annual / (total_budget / years_remaining) - 1) * 100, 1),
        'budget_breakdown': [
            {'year': year, 'budget_kg': int(current_annual * (1 - (year - current_year) / years_remaining))}
            for year in range(current_year, target_year + 1, 5)
        ],
        'risk_assessment': {
            'overshoot_risk': 'Medium',
            'confidence_level': 75,
            'key_assumptions': [
                'Linear reduction pathway',
                'No major business changes',
                'Initiatives delivered on time'
            ]
        }
    }
    
    return jsonify(carbon_budget)
