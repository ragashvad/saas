# dashboard/dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title='Sustainability-as-a-Service', layout='wide')

BACKEND = "http://localhost:5000"

st.sidebar.title("SaaS Navigation")
nav = st.sidebar.radio("Go to", [
    "Login", 
    "Dashboard", 
    "Real-time Monitoring",
    "Analytics & Predictions",
    "Optimization",
    "ESG Reporting",
    "Billing"
])

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

def login_form():
    st.subheader("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            r = requests.post(f"{BACKEND}/users/login", json={
                "user_id": user_id, "password": password
            }, timeout=5)
        except Exception as e:
            st.error(f"Backend unreachable: {e}")
            return
        if r.ok:
            st.session_state["user_id"] = user_id
            st.success("Logged in as " + user_id)
        else:
            st.error("Login failed!")

def dashboard_page():
    st.title("🌍 Sustainability Dashboard")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    
    st.write(f"Welcome, **{user_id}**")
    
    # Get sustainability score
    try:
        score_resp = requests.get(f"{BACKEND}/energy/sustainability_score/{user_id}", timeout=5)
        if score_resp.ok:
            score_data = score_resp.json()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sustainability Score", f"{score_data['overall_score']}/100")
            with col2:
                st.metric("Grade", score_data['grade'])
            with col3:
                st.metric("Benchmark", score_data['benchmark'])
            with col4:
                if score_data['overall_score'] >= 80:
                    st.success("Excellent Performance! 🌟")
                elif score_data['overall_score'] >= 60:
                    st.info("Good Progress 👍")
                else:
                    st.warning("Needs Improvement ⚠️")
            
            # Score breakdown
            st.subheader("Score Breakdown")
            factors_df = pd.DataFrame(score_data['factors'], columns=['Factor', 'Score'])
            fig = px.bar(factors_df, x='Factor', y='Score', 
                        title='Sustainability Factors',
                        color='Score',
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading score: {e}")
    
    # Get sensor data
    try:
        resp = requests.get(f"{BACKEND}/energy/sensor_data/{user_id}", timeout=5)
        if resp.ok:
            data = resp.json()
            
            st.subheader("📊 Real-time KPIs")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Energy (kWh)", data['kpi']['total_energy'])
            col2.metric("Total Carbon (kg)", data['kpi']['total_carbon'])
            col3.metric("Anomalies Detected", data['kpi']['anomalies'])
            col4.metric("Active Devices", data['kpi']['active_devices'])
            
            col5, col6 = st.columns(2)
            col5.metric("Avg Temperature (°C)", data['kpi']['avg_temperature'])
            col6.metric("Avg Occupancy", f"{data['kpi']['avg_occupancy']*100:.0f}%")
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

def realtime_monitoring():
    st.title("🔴 Real-time Monitoring")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    try:
        resp = requests.get(f"{BACKEND}/energy/sensor_data/{user_id}", timeout=5)
        if resp.ok:
            data = resp.json()
            
            # Energy meters
            st.subheader("⚡ Energy Meters")
            energy_df = pd.DataFrame(data['raw']['energy_meters'])
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=energy_df['device_id'],
                y=energy_df['energy_kwh'],
                name='Energy (kWh)',
                marker_color=['red' if anomaly else 'green' 
                            for anomaly in energy_df['anomaly']]
            ))
            fig.update_layout(title='Energy Consumption by Device', 
                            xaxis_title='Device', yaxis_title='kWh')
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(energy_df, use_container_width=True)
            
            # Temperature sensors
            st.subheader("🌡️ Temperature Sensors")
            temp_df = pd.DataFrame(data['raw']['temperature_sensors'])
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=temp_df['device_id'],
                y=temp_df['temperature_c'],
                name='Temperature',
                marker_color='orange'
            ))
            fig2.update_layout(title='Temperature Readings', 
                             xaxis_title='Sensor', yaxis_title='°C')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Occupancy sensors
            st.subheader("👥 Occupancy Sensors")
            occ_df = pd.DataFrame(data['raw']['occupancy_sensors'])
            
            fig3 = px.pie(occ_df, values='people_count', names='device_id',
                         title='People Distribution by Zone')
            st.plotly_chart(fig3, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading monitoring data: {e}")

def analytics_predictions():
    st.title("📈 Analytics & Predictions")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    
    # Historical data
    st.subheader("Historical Energy Consumption")
    try:
        hist_resp = requests.get(f"{BACKEND}/energy/historical/{user_id}?hours=168", timeout=5)
        if hist_resp.ok:
            hist_data = hist_resp.json()['historical_data']
            hist_df = pd.DataFrame(hist_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist_df['timestamp'],
                y=hist_df['total_energy_kwh'],
                mode='lines+markers',
                name='Energy',
                line=dict(color='blue', width=2)
            ))
            fig.update_layout(title='Energy Consumption - Last 7 Days',
                            xaxis_title='Time', yaxis_title='kWh')
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading historical data: {e}")
    
    # Predictions
    st.subheader("Energy Demand Forecast")
    forecast_hours = st.slider("Forecast Hours", 6, 48, 24)
    
    try:
        pred_resp = requests.get(
            f"{BACKEND}/energy/predict/{user_id}?forecast_hours={forecast_hours}", 
            timeout=5
        )
        if pred_resp.ok:
            pred_data = pred_resp.json()['predictions']
            pred_df = pd.DataFrame(pred_data)
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=pred_df['timestamp'],
                y=pred_df['predicted_energy_kwh'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='red', width=2, dash='dash')
            ))
            fig2.update_layout(title=f'Energy Forecast - Next {forecast_hours} Hours',
                             xaxis_title='Time', yaxis_title='Predicted kWh')
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading predictions: {e}")
    
    # Carbon footprint
    st.subheader("Carbon Footprint Analysis")
    try:
        carbon_resp = requests.get(f"{BACKEND}/energy/carbon_footprint/{user_id}", timeout=5)
        if carbon_resp.ok:
            carbon = carbon_resp.json()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Carbon (tons)", carbon['total_carbon_tons'])
            col2.metric("Equivalent Trees Needed", carbon['equivalent_trees'])
            col3.metric("Equivalent km Driven", f"{carbon['equivalent_km_driven']:,.0f}")
    except Exception as e:
        st.error(f"Error loading carbon data: {e}")

def optimization_page():
    st.title("🎯 Energy Optimization")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    
    try:
        opt_resp = requests.get(f"{BACKEND}/energy/optimize/{user_id}", timeout=5)
        if opt_resp.ok:
            opt_data = opt_resp.json()
            
            # Savings potential
            st.subheader("💰 Savings Potential")
            col1, col2, col3 = st.columns(3)
            col1.metric("Potential Savings (kWh)", 
                       opt_data['total_savings_potential_kwh'])
            col2.metric("Cost Savings ($)", 
                       opt_data['total_savings_potential_cost'])
            col3.metric("ROI Period (months)", 
                       opt_data['roi_months'])
            
            # Recommendations
            st.subheader("📋 Optimization Recommendations")
            for rec in opt_data['recommendations']:
                with st.expander(f"🔹 {rec['category']} - Priority: {rec['priority']}"):
                    st.write(f"**Recommendation:** {rec['recommendation']}")
                    col_a, col_b = st.columns(2)
                    col_a.metric("Savings (kWh)", rec['potential_savings_kwh'])
                    col_b.metric("Savings (%)", f"{rec['potential_savings_percent']}%")
    except Exception as e:
        st.error(f"Error loading optimization: {e}")

def esg_reporting():
    st.title("📄 ESG Reporting")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    
    timeframe = st.selectbox("Select Timeframe", ["monthly", "quarterly", "yearly"])
    
    if st.button("Generate ESG Report"):
        try:
            esg_resp = requests.get(
                f"{BACKEND}/energy/esg_report/{user_id}?timeframe={timeframe}", 
                timeout=5
            )
            if esg_resp.ok:
                report = esg_resp.json()
                
                st.subheader(f"ESG Report - {timeframe.capitalize()}")
                st.caption(f"Generated: {report['report_date']}")
                
                # Environmental metrics
                with st.expander("🌱 Environmental Metrics", expanded=True):
                    env = report['environmental']
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Energy Consumption", f"{env['energy_consumption_kwh']} kWh")
                    col2.metric("Carbon Emissions", f"{env['carbon_emissions_kg']} kg")
                    col3.metric("Renewable Energy %", f"{env['renewable_energy_percent']}%")
                    
                    col4, col5 = st.columns(2)
                    col4.metric("Waste Reduction %", f"{env['waste_reduction_percent']}%")
                    col5.metric("Water Usage", f"{env['water_usage_liters']} L")
                
                # Social metrics
                with st.expander("👥 Social Metrics"):
                    social = report['social']
                    st.write(f"**Employee Satisfaction:** {social['employee_satisfaction']}/5")
                    st.write(f"**Safety Incidents:** {social['safety_incidents']}")
                    st.write(f"**Training Hours:** {social['training_hours']}")
                
                # Governance metrics
                with st.expander("⚖️ Governance Metrics"):
                    gov = report['governance']
                    st.write(f"**Compliance Score:** {gov['compliance_score']}/100")
                    st.write(f"**Audit Status:** {gov['audit_status']}")
                    st.write(f"**Policy Updates:** {gov['policy_updates']}")
                
                # Initiatives
                st.subheader("✅ Sustainability Initiatives")
                for initiative in report['sustainability_initiatives']:
                    st.success(f"✓ {initiative}")
                
                # Next steps
                st.subheader("🎯 Next Steps")
                for step in report['next_steps']:
                    st.info(f"→ {step}")
                    
                if st.button("📥 Download Report (JSON)"):
                    st.download_button(
                        label="Download",
                        data=str(report),
                        file_name=f"esg_report_{timeframe}_{user_id}.json",
                        mime="application/json"
                    )
        except Exception as e:
            st.error(f"Error generating report: {e}")
    
    # File upload for ESG analysis
    st.subheader("📤 Upload ESG Document for AI Analysis")
    uploaded_file = st.file_uploader("Upload ESG document (CSV/TXT)")
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            r = requests.post(f"{BACKEND}/esg/upload", files=files, timeout=10)
            if r.ok:
                result = r.json()
                st.success("Analysis complete!")
                st.json(result)
        except Exception as e:
            st.error(f"Upload failed: {e}")

def billing_page():
    st.title("💳 Billing & Subscription")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    
    try:
        plans = requests.get(f"{BACKEND}/billing/plans").json()
        user_plan = requests.get(f"{BACKEND}/billing/get_plan/{user_id}").json().get("plan", "basic")
        
        st.write(f"Current subscription: **{user_plan.capitalize()}**")
        
        for plan, info in plans.items():
            with st.expander(f"{plan.capitalize()} - ${info['price']}/mo"):
                st.write("**Features:**")
                for feature in info['features']:
                    st.write(f"✓ {feature}")
                if st.button(f"Upgrade to {plan.capitalize()}", key=plan) and plan != user_plan:
                    r = requests.post(f"{BACKEND}/billing/upgrade", json={
                        "user_id": user_id, "new_plan": plan
                    })
                    if r.ok:
                        st.success(f"Upgraded to {plan.capitalize()}!")
                        st.rerun()
    except Exception as e:
        st.error(f"Error loading billing: {e}")

# Navigation routing
if nav == "Login":
    login_form()
elif nav == "Dashboard":
    dashboard_page()
elif nav == "Real-time Monitoring":
    realtime_monitoring()
elif nav == "Analytics & Predictions":
    analytics_predictions()
elif nav == "Optimization":
    optimization_page()
elif nav == "ESG Reporting":
    esg_reporting()
elif nav == "Billing":
    billing_page()