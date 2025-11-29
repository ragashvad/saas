# Quick Start Guide - Sustainability-as-a-Service

## 🚀 5-Minute Setup

### Step 1: Verify Installation
```bash
cd /home/linux/saas
ls -la
# You should see: backend/ dashboard/ docs/ sample_data/
```

### Step 2: Check Servers
Both servers should already be running:

✅ **Backend API**: http://localhost:5000  
✅ **Dashboard**: http://localhost:8501

### Step 3: Access Dashboard
Open your browser and navigate to: **http://localhost:8501**

---

## 🎯 First Login

Use demo credentials:
- **Username**: `user1`
- **Password**: `password1`

Click "Login" button.

---

## 📊 Quick Tour (2 minutes)

### 1. Dashboard Overview
After login, you'll see:
- **Sustainability Score**: 70-85 (typical range)
- **Grade**: B+ to A-
- **Real-time KPIs**: Energy, Carbon, Anomalies
- **Score Breakdown Chart**: Visual factors

### 2. Real-time Monitoring
Click "Real-time Monitoring" in sidebar:
- View live energy consumption (bar chart)
- Green bars = Normal | Red bars = Anomaly detected
- Temperature and occupancy data
- Click "🔄 Refresh Data" for latest readings

### 3. Analytics & Predictions
Click "Analytics & Predictions":
- See 7-day historical energy trends
- Adjust forecast slider (6-48 hours)
- View carbon footprint equivalents

### 4. Optimization
Click "Optimization":
- See AI-generated recommendations
- Check potential savings (kWh and $)
- Review ROI period

### 5. ESG Reporting
Click "ESG Reporting":
- Select timeframe (Monthly/Quarterly/Yearly)
- Click "Generate ESG Report"
- Review Environmental, Social, Governance metrics
- Try uploading: `sample_data/sample_esg_report.csv`

---

## 🔧 If Servers Aren't Running

### Restart Backend
```bash
cd /home/linux/saas/backend
source ../venv/bin/activate
python app.py
```
Should show: `Running on http://127.0.0.1:5000`

### Restart Dashboard (in new terminal)
```bash
cd /home/linux/saas/dashboard
source ../venv/bin/activate
streamlit run dashboard.py
```
Should show: `Local URL: http://localhost:8501`

---

## 🎓 Demo Scenarios

### Scenario 1: Monitor Energy (1 min)
1. Login as user1
2. Go to "Real-time Monitoring"
3. Observe energy bars (some may be red = anomaly)
4. Note the anomaly count in KPIs
5. Click refresh to see new data

### Scenario 2: Get Predictions (1 min)
1. Go to "Analytics & Predictions"
2. Look at the historical line chart
3. Adjust forecast slider to 48 hours
4. See predicted energy demand curve
5. Note carbon footprint metrics below

### Scenario 3: Optimize Costs (2 min)
1. Go to "Optimization"
2. See potential savings summary (top)
3. Expand each recommendation category
4. Note High-priority items first
5. Check ROI period estimate

### Scenario 4: Generate Report (2 min)
1. Go to "ESG Reporting"
2. Select "Monthly" timeframe
3. Click "Generate ESG Report"
4. Expand Environmental/Social/Governance sections
5. See sustainability initiatives and next steps

---

## 🔑 Key Features to Showcase

### Real-time Data
- 12 simulated IoT sensors
- Energy meters (5 devices)
- Temperature sensors (3 devices)
- Occupancy sensors (2 devices)
- Water meters (2 devices)

### AI Analytics
- Anomaly detection (Isolation Forest)
- Energy forecasting (Random Forest)
- Optimization recommendations
- Sustainability scoring (0-100)

### Visualizations
- Interactive Plotly charts
- Color-coded anomalies
- Historical trends
- Predictive forecasts

### Business Model
- Basic: $29/mo (5 devices)
- Pro: $99/mo (20 devices)
- Enterprise: $299/mo (unlimited)

---

## 📱 API Testing (Optional)

Try these curl commands:

```bash
# Get sensor data
curl http://localhost:5000/energy/sensor_data/user1

# Get predictions
curl http://localhost:5000/energy/predict/user1?forecast_hours=24

# Get sustainability score
curl http://localhost:5000/energy/sustainability_score/user1

# Get optimization recommendations
curl http://localhost:5000/energy/optimize/user1
```

---

## 💡 Tips

### Best Viewing
- Use Chrome or Firefox
- Full screen recommended
- Dashboard auto-scales to screen size

### Data Refresh
- Click "🔄 Refresh Data" for new readings
- Sensor data simulates time-of-day patterns
- Anomalies appear randomly (10% rate)

### User Comparison
Try both accounts to see differences:
- `user1` (Basic): 5 devices
- `user2` (Pro): 20 devices

### Navigation
Use sidebar to switch between sections:
- Login → Dashboard → Monitoring → Analytics → Optimization → ESG → Billing

---

## 📚 Full Documentation

For detailed information:
- **User Guide**: `docs/USER_GUIDE.md`
- **API Docs**: `docs/API_DOCUMENTATION.md`
- **Project Summary**: `docs/PROJECT_SUMMARY.md`
- **Main README**: `README.md`

---

## ⚠️ Troubleshooting

### Dashboard Not Loading?
1. Check backend is running (http://localhost:5000)
2. Restart both servers (see "If Servers Aren't Running")
3. Clear browser cache

### "Backend unreachable" Error?
1. Verify backend terminal shows "Running on http://127.0.0.1:5000"
2. Check firewall isn't blocking port 5000
3. Try restarting backend

### No Data Showing?
1. Make sure you're logged in
2. Wait 2-3 seconds for simulation
3. Click "Refresh Data" button

### Slow Performance?
1. Use shorter time periods (day vs month)
2. Reduce forecast hours (24 vs 48)
3. Close other browser tabs

---

## 🎉 You're Ready!

The platform is fully operational. Explore all features and see how Sustainability-as-a-Service can transform business sustainability monitoring!

**Happy Exploring! 🌍**

---

**Quick Links:**
- Dashboard: http://localhost:8501
- API: http://localhost:5000
- Credentials: user1/password1 or user2/password2
