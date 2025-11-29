# Sustainability-as-a-Service Platform - User Guide

## Introduction
Welcome to the Sustainability-as-a-Service (SaaS) platform! This comprehensive system helps businesses monitor, optimize, and report on their sustainability performance through IoT sensors, AI analytics, and cloud-based dashboards.

## System Features

### 🌍 Core Capabilities
1. **Real-time Monitoring**: Live data from energy meters, temperature sensors, occupancy sensors, and water meters
2. **AI-Powered Analytics**: Machine learning for anomaly detection and predictive analytics
3. **Energy Optimization**: Automated recommendations to reduce consumption and costs
4. **Carbon Footprint Tracking**: Comprehensive carbon emissions monitoring and reporting
5. **ESG Reporting**: Generate compliance reports for Environmental, Social, and Governance metrics
6. **Predictive Forecasting**: 24-48 hour energy demand predictions

### 📊 Key Performance Indicators (KPIs)
- Total Energy Consumption (kWh)
- Carbon Emissions (kg CO₂)
- Sustainability Score (0-100)
- Anomaly Detection Count
- Average Temperature & Occupancy
- Cost Savings Potential

---

## Getting Started

### Prerequisites
- Python 3.9+
- Web browser (Chrome, Firefox, Safari)
- Internet connection for dashboard access

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/saas
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   venv\Scripts\activate  # Windows
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install dashboard dependencies**
   ```bash
   cd ../dashboard
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Manual Start (Development)

**Terminal 1 - Backend Server:**
```bash
cd backend
source ../venv/bin/activate
python app.py
```
Backend runs at: http://localhost:5000

**Terminal 2 - Dashboard:**
```bash
cd dashboard
source ../venv/bin/activate
streamlit run dashboard.py
```
Dashboard runs at: http://localhost:8501

#### Option 2: Docker (Production)
```bash
docker-compose up -d
```

---

## Using the Dashboard

### 1. Login
- Open http://localhost:8501
- Use demo credentials:
  - **Basic User**: `user1` / `password1`
  - **Pro User**: `user2` / `password2`

### 2. Dashboard Overview
The main dashboard displays:
- **Sustainability Score**: Overall performance rating (0-100)
- **Score Grade**: Letter grade (A+ to D)
- **Real-time KPIs**: Energy, carbon, anomalies, devices
- **Environmental Factors**: Temperature, occupancy
- **Score Breakdown Chart**: Visual representation of factors

### 3. Real-time Monitoring
Navigate to "Real-time Monitoring" to view:
- **Energy Meters**: Bar chart showing consumption by device
  - Green bars: Normal operation
  - Red bars: Anomaly detected
- **Temperature Sensors**: Current temperature readings
- **Occupancy Sensors**: People count and distribution
- **Detailed Data Tables**: Raw sensor readings with timestamps

**Tip:** Click "🔄 Refresh Data" to get latest readings

### 4. Analytics & Predictions
View historical trends and forecasts:
- **Historical Consumption**: Line chart showing 7-day energy usage
- **Energy Forecast**: Predictive model for next 6-48 hours
- **Carbon Footprint**: Equivalent metrics (trees needed, km driven)

**How to use:**
- Adjust forecast slider to change prediction horizon
- Analyze patterns to identify peak usage times
- Compare historical vs. predicted values

### 5. Optimization Recommendations
Get AI-powered savings recommendations:
- **Savings Potential**: Total kWh and $ savings available
- **ROI Period**: Expected return on investment timeline
- **Categorized Recommendations**:
  - Peak Load Management
  - Occupancy-Based Control
  - HVAC Optimization
  - Power Quality Improvements
  - Renewable Energy Options

**Each recommendation shows:**
- Priority level (High/Medium/Long-term)
- Specific action items
- Potential savings (kWh and %)

### 6. ESG Reporting
Generate comprehensive sustainability reports:
1. Select timeframe (Monthly/Quarterly/Yearly)
2. Click "Generate ESG Report"
3. Review metrics:
   - **Environmental**: Energy, carbon, renewables, water
   - **Social**: Employee satisfaction, safety, training
   - **Governance**: Compliance, audits, policies
4. Download report as JSON for external use

**Upload Feature:**
- Upload existing ESG documents (CSV/TXT)
- AI extracts and summarizes KPIs automatically

### 7. Billing & Subscription
Manage your subscription plan:

| Plan | Price | Features |
|------|-------|----------|
| **Basic** | $29/mo | 5 devices, Basic analytics, Email support |
| **Pro** | $99/mo | 20 devices, Advanced AI, Real-time alerts, API access |
| **Enterprise** | $299/mo | Unlimited devices, Custom ML, 24/7 support, SLA |

**To upgrade:**
1. Navigate to "Billing"
2. Expand desired plan
3. Click "Upgrade to [Plan]"

---

## API Integration

### Accessing the API
Pro and Enterprise users can integrate via REST API:

**Base URL:** `http://localhost:5000`

**Example: Get Sensor Data**
```bash
curl http://localhost:5000/energy/sensor_data/user1
```

**Example: Get Predictions**
```bash
curl http://localhost:5000/energy/predict/user1?forecast_hours=24
```

See `docs/API_DOCUMENTATION.md` for complete API reference.

---

## Understanding Metrics

### Sustainability Score
- **90-100 (A+/A)**: Excellent - Industry leader
- **80-89 (A-/B+)**: Good - Above average performance
- **70-79 (B/B-)**: Satisfactory - Meeting standards
- **60-69 (C+/C)**: Needs improvement
- **Below 60 (D)**: Critical - Immediate action required

### Anomaly Detection
The system uses Isolation Forest ML algorithm to detect:
- Unusual energy spikes
- Equipment malfunction
- Voltage irregularities
- Abnormal consumption patterns

**Severity Scores:**
- 0-30: Low risk
- 31-60: Medium risk
- 61-100: High risk (immediate attention needed)

### Carbon Intensity
- Measured in kg CO₂ per kWh
- Varies by time of day (solar reduces daytime intensity)
- Typical range: 0.25-0.35 kg/kWh

---

## Best Practices

### Daily Operations
1. Check dashboard each morning for anomalies
2. Review real-time monitoring during peak hours
3. Respond to high-severity anomalies immediately
4. Track sustainability score trends

### Weekly Activities
1. Review 7-day historical trends
2. Analyze optimization recommendations
3. Implement 1-2 quick wins from suggestions
4. Check forecast accuracy

### Monthly Tasks
1. Generate ESG report
2. Review progress toward goals
3. Adjust strategies based on analytics
4. Share reports with stakeholders

### Optimization Tips
- **Peak Load Management**: Shift non-critical loads to off-peak hours
- **Occupancy Control**: Automate lighting/HVAC in unused areas
- **Temperature Settings**: Maintain 21-23°C range
- **Equipment Maintenance**: Address anomalies promptly
- **Renewable Energy**: Evaluate solar/wind feasibility

---

## Troubleshooting

### Backend Not Starting
```bash
# Check if port 5000 is in use
lsof -i :5000
# Kill process if needed
kill -9 <PID>
```

### Dashboard Connection Error
1. Verify backend is running (http://localhost:5000)
2. Check firewall settings
3. Restart both services

### No Data Showing
1. Login with valid credentials
2. Wait 5-10 seconds for sensor simulation
3. Click "Refresh Data" button

### Slow Performance
1. Clear browser cache
2. Reduce forecast_hours parameter
3. Use "day" instead of "month" for historical queries

---

## Data Storage

### Database Location
- SQLite database: `backend/data/sustainability.db`
- Historical data retained for 90 days
- Automatic cleanup of old records

### Backup Recommendations
```bash
# Backup database
cp backend/data/sustainability.db backup/sustainability_$(date +%Y%m%d).db
```

---

## Support & Resources

### Documentation
- `README.md` - Quick start guide
- `docs/API_DOCUMENTATION.md` - Complete API reference
- `docs/cloud_deployment.md` - Cloud deployment guide
- `docs/USER_GUIDE.md` - This document

### Demo Data
- Sample ESG report: `sample_data/sample_esg_report.csv`

### Contact
- Technical Support: support@sustainability-saas.com
- Sales: sales@sustainability-saas.com
- Documentation: docs@sustainability-saas.com

---

## Seminar Project Information

This platform demonstrates the concept outlined in "Doing Sustainable Business? Sustainability-as-a-Service" seminar proposal:

### System Architecture Implementation
✅ **IoT & Edge Layer**: Simulated sensors (energy, temperature, occupancy, water)  
✅ **Data Integration Layer**: SQLite database with REST API access  
✅ **Analytics Layer**: ML models for predictions, anomaly detection, optimization  
✅ **Service Layer**: Flask REST APIs for external system integration  
✅ **User Interface Layer**: Streamlit dashboard with comprehensive visualizations  

### Technologies Used
- **Cloud Platform**: Ready for AWS/Azure deployment
- **Data Pipeline**: REST APIs, Python, Flask
- **Analytics**: Pandas, Scikit-learn, ML algorithms
- **Visualization**: Streamlit, Plotly charts
- **Storage**: SQLite (upgradable to InfluxDB/PostgreSQL)

### Expected Outcomes Achieved
✅ Conceptual cloud architecture diagram  
✅ Working prototype with IoT-to-dashboard flow  
✅ Comprehensive API documentation  
✅ System feasibility demonstration  
✅ Scalability for commercial deployment  

---

**Version:** 1.0  
**Last Updated:** November 29, 2025  
**Platform:** Sustainability-as-a-Service MVP
