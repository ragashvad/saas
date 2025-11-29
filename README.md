# Sustainability-as-a-Service (AI-Powered Platform)

A comprehensive, modular cloud platform for sustainability analytics, powered by IoT simulation, machine learning, and real-time monitoring.

## 🌟 Project Overview

This platform implements the **Sustainability-as-a-Service** concept, enabling businesses to monitor, optimize, and report their sustainability performance through:

- **IoT Integration**: Real-time data from energy meters, temperature sensors, occupancy detectors, and water meters
- **AI Analytics**: Machine learning for anomaly detection, predictive forecasting, and optimization
- **Cloud Architecture**: Scalable REST APIs for external system integration
- **Interactive Dashboard**: Comprehensive visualizations and reporting tools
- **ESG Compliance**: Automated Environmental, Social, and Governance reporting

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            User Interface Layer (Port 8501)                  │
│     Streamlit Dashboard │ External API Clients              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│             Service/API Layer (Port 5000)                    │
│   Flask REST APIs: /energy, /analytics, /esg, /billing     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Analytics Layer                            │
│  ML Models │ Predictions │ Anomaly Detection │ Optimization │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Integration Layer                          │
│         SQLite Database │ Time-Series Storage               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  IoT & Edge Layer                            │
│   Energy Meters │ Temp Sensors │ Occupancy │ Water Meters   │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### 📊 Real-time Monitoring
- Live sensor data from multiple IoT devices
- Energy consumption tracking (kWh)
- Temperature and humidity monitoring
- Occupancy detection and analytics
- Water usage monitoring
- Anomaly detection with severity scoring

### 🤖 AI-Powered Analytics
- **Anomaly Detection**: Isolation Forest ML algorithm
- **Predictive Forecasting**: 24-48 hour energy demand predictions
- **Optimization Engine**: AI-generated recommendations for energy savings
- **Carbon Footprint**: Comprehensive CO₂ emissions tracking
- **Sustainability Scoring**: 0-100 rating with letter grades

### 📈 Advanced Visualizations
- Interactive Plotly charts
- Real-time KPI dashboards
- Historical trend analysis
- Predictive forecasting graphs
- ESG compliance reports

### 🌍 ESG Reporting
- Environmental metrics (energy, carbon, water, waste)
- Social metrics (employee satisfaction, safety)
- Governance metrics (compliance, audits)
- Automated report generation (monthly/quarterly/yearly)
- Document upload with AI extraction

### 💡 Optimization Recommendations
- Peak load management
- Occupancy-based control
- HVAC optimization
- Power quality improvements
- Renewable energy evaluation
- ROI calculations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Installation

1. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   venv\Scripts\activate     # Windows
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install dashboard dependencies**
   ```bash
   cd ../dashboard
   pip install -r requirements.txt
   ```

### Running the Application

**Terminal 1 - Backend API Server:**
```bash
cd backend
source ../venv/bin/activate
python app.py
```
✅ Backend running at: **http://localhost:5000**

**Terminal 2 - Dashboard:**
```bash
cd dashboard
source ../venv/bin/activate
streamlit run dashboard.py
```
✅ Dashboard running at: **http://localhost:8501**

---

## 👤 Demo Users

| User ID | Password | Plan | Devices |
|---------|----------|------|---------|
| user1 | password1 | Basic | 5 |
| user2 | password2 | Pro | 20 |

---

## 📱 Dashboard Navigation

### 1. **Login**
   - Authenticate with demo credentials

### 2. **Dashboard**
   - Sustainability score overview
   - Real-time KPIs (energy, carbon, anomalies)
   - Score breakdown by factors

### 3. **Real-time Monitoring**
   - Live sensor data from all devices
   - Energy consumption by device (color-coded for anomalies)
   - Temperature and humidity readings
   - Occupancy distribution charts
   - Refresh button for latest data

### 4. **Analytics & Predictions**
   - 7-day historical energy trends
   - 6-48 hour demand forecasting
   - Carbon footprint calculator
   - Equivalent metrics (trees, km driven)

### 5. **Optimization**
   - AI-generated savings recommendations
   - Categorized by priority (High/Medium/Long-term)
   - Potential savings (kWh, $, %)
   - ROI period estimation

### 6. **ESG Reporting**
   - Generate comprehensive reports
   - Environmental, Social, Governance metrics
   - Upload documents for AI analysis
   - Download reports as JSON

### 7. **Billing**
   - View current subscription
   - Compare plan features
   - Upgrade subscription

---

## 🔌 API Endpoints

### Energy Monitoring
- `GET /energy/sensor_data/<user_id>` - Real-time sensor data
- `GET /energy/historical/<user_id>?hours=24` - Historical data
- `GET /energy/predict/<user_id>?forecast_hours=24` - Predictions
- `GET /energy/optimize/<user_id>` - Optimization recommendations
- `GET /energy/carbon_footprint/<user_id>` - Carbon analysis
- `GET /energy/sustainability_score/<user_id>` - Overall score
- `GET /energy/esg_report/<user_id>?timeframe=monthly` - ESG report
- `GET /energy/metrics/<user_id>?period=day` - Aggregated metrics

### User Management
- `POST /users/login` - User authentication

### Billing
- `GET /billing/plans` - Available plans
- `GET /billing/get_plan/<user_id>` - Current plan
- `POST /billing/upgrade` - Upgrade subscription

### ESG Compliance
- `POST /esg/upload` - Upload and analyze documents

**Full API Documentation:** See `docs/API_DOCUMENTATION.md`

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (REST API)
- **ML/Analytics**: Scikit-learn, Pandas, NumPy
- **Database**: SQLite (upgradable to PostgreSQL/InfluxDB)
- **IoT Simulation**: Custom Python simulator

### Frontend
- **Dashboard**: Streamlit
- **Visualizations**: Plotly, Pandas
- **HTTP Client**: Requests

### Analytics
- **Anomaly Detection**: Isolation Forest
- **Prediction**: Random Forest Regressor, Linear Regression
- **Optimization**: Rule-based + ML hybrid

### Deployment
- **Local**: Python virtual environment
- **Docker**: Dockerfile.txt available
- **Cloud**: AWS/Azure ready (see `docs/cloud_deployment.md`)

---

## 📊 Project Structure

```
saas/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── energy.py                 # Energy monitoring endpoints
│   ├── analytics.py              # Legacy analytics
│   ├── advanced_analytics.py     # ML models & optimization
│   ├── iot_simulator.py          # IoT sensor simulation
│   ├── data_storage.py           # Database layer
│   ├── billing.py                # Subscription management
│   ├── users.py                  # User authentication
│   ├── esg_ai.py                 # ESG document analysis
│   ├── requirements.txt          # Python dependencies
│   └── data/                     # SQLite database
├── dashboard/
│   ├── dashboard.py              # Streamlit UI
│   ├── requirements.txt          # Dashboard dependencies
├── docs/
│   ├── API_DOCUMENTATION.md      # Complete API reference
│   ├── USER_GUIDE.md             # User manual
│   └── cloud_deployment.md       # Cloud setup guide
├── sample_data/
│   └── sample_esg_report.csv     # Sample ESG data
├── README.md                     # This file
└── LICENSE.txt
```

---

## 📖 Documentation

- **[API Documentation](docs/API_DOCUMENTATION.md)**: Complete REST API reference
- **[User Guide](docs/USER_GUIDE.md)**: Detailed platform usage instructions
- **[Cloud Deployment](docs/cloud_deployment.md)**: AWS/Azure deployment steps

---

## 🎯 Seminar Project Alignment

This platform implements the **"Doing Sustainable Business? Sustainability-as-a-Service"** seminar proposal:

### ✅ Objectives Achieved
1. ✅ Integrated cloud platform architecture
2. ✅ APIs connecting IoT devices to dashboards
3. ✅ Working prototype with simulated data
4. ✅ Business model demonstration (Basic/Pro/Enterprise)

### ✅ System Architecture (5 Layers)
1. ✅ **IoT & Edge Layer**: Energy, temperature, occupancy, water sensors
2. ✅ **Data Integration Layer**: SQLite + REST APIs
3. ✅ **Analytics Layer**: ML models, predictions, optimization
4. ✅ **Service Layer**: Flask REST APIs
5. ✅ **User Interface Layer**: Streamlit dashboard

### ✅ Expected Outcomes
1. ✅ Cloud architecture diagram (see above)
2. ✅ Working prototype (IoT → Analytics → Dashboard)
3. ✅ API documentation (see `docs/API_DOCUMENTATION.md`)
4. ✅ Feasibility evaluation (demonstrated via MVP)

---

## 💼 Business Model

### Subscription Tiers

| Feature | Basic ($29/mo) | Pro ($99/mo) | Enterprise ($299/mo) |
|---------|----------------|--------------|----------------------|
| Devices | 5 | 20 | Unlimited |
| Analytics | Basic | Advanced AI | Custom ML Models |
| Predictions | 24 hours | 48 hours | Custom timeframes |
| API Access | ❌ | ✅ | ✅ with SLA |
| Support | Email | Priority | 24/7 Dedicated |
| Reports | Monthly | Real-time | Custom |

---

## 🔮 Future Enhancements

- [ ] MQTT protocol integration for real IoT devices
- [ ] InfluxDB for time-series optimization
- [ ] Grafana dashboard integration
- [ ] Mobile app (iOS/Android)
- [ ] Multi-tenancy support
- [ ] Advanced ML models (LSTM, Prophet)
- [ ] Real-time alerting system
- [ ] Integration with renewable energy APIs
- [ ] Blockchain for carbon credit tracking
- [ ] ISO 14001 compliance automation

---

## 🤝 Contributing

This is a seminar project demonstrating Sustainability-as-a-Service concepts. For production deployment:

1. Replace SQLite with production database (PostgreSQL/InfluxDB)
2. Implement proper authentication (OAuth, JWT)
3. Add HTTPS/SSL certificates
4. Set up monitoring and logging
5. Implement rate limiting
6. Add comprehensive testing

---

## 📄 License

MIT License - See `LICENSE.txt`

---

## 📧 Contact & Support

- **Documentation Issues**: See `docs/` folder
- **API Questions**: Refer to `docs/API_DOCUMENTATION.md`
- **User Guide**: See `docs/USER_GUIDE.md`

---

## 🌟 Impact Statement

This platform demonstrates how **data-driven cloud services** can:
- ✅ Reduce energy consumption through optimization
- ✅ Enhance transparency via real-time monitoring
- ✅ Make sustainability accessible to businesses of all sizes
- ✅ Provide actionable insights through AI analytics
- ✅ Automate ESG compliance reporting
- ✅ Drive digital sustainability transformation

**Built for the Future. Sustainable by Design.** 🌍

---

**Version:** 2.0 (Enhanced)  
**Last Updated:** November 29, 2025  
**Seminar Topic:** Doing Sustainable Business? Sustainability-as-a-Service