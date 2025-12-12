import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Sustainability-as-a-Service", layout="wide")
st.set_page_config(page_title="Sustainability-as-a-Service", layout="wide")

# ---- Global App Styling (shell similar to enterprise dashboards) ----
st.markdown("""
<style>

/* App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f5f2 0%, #c4eee2 40%, #89d6c8 100%);
}

/* Top header bar (light teal) */
[data-testid="stHeader"] {
    background: #8ad4c0 !important;  
    color: #00332b;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

/* Smaller cleaner header */
header[data-testid="stHeader"] div {
    height: 3rem;
}

/* Sidebar: soft light green-grey */
[data-testid="stSidebar"] {
    background-color: #cdeae3 !important;
    color: #00332b !important;
    border-right: 1px solid #b7d8d0;
}

/* Sidebar text + radio buttons */
[data-testid="stSidebar"] * {
    color: #00332b !important;
    font-size: 14px;
}

/* Main content white card */
.block-container {
    background: rgba(255, 255, 255, 0.96);
    padding: 1.8rem 2.2rem;
    border-radius: 16px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.15);
}

/* Metrics card */
[data-testid="stMetric"] {
    background-color: #f7fffc;
    padding: 0.8rem 1rem;
    border-radius: 12px;
    border: 1px solid #d2efe7;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

/* Section titles */
h2, h3 {
    font-weight: 600;
    color: #005849;
}

/* All text elements - ensure dark color */
p, span, div, label {
    color: #1a1a1a;
}

/* Streamlit text elements */
[data-testid="stMarkdownContainer"] p,
[data-testid="stText"] {
    color: #1a1a1a;
}

/* Metric labels and values */
[data-testid="stMetricLabel"] {
    color: #005849 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #013220 !important;
    font-weight: 700;
}

/* Remove extra top padding */
main .block-container {
    padding-top: 1.2rem;
}

</style>
""", unsafe_allow_html=True)


BACKEND = "http://localhost:5000"

# -------------------------------------------------------------------
# Sidebar navigation + session state
# -------------------------------------------------------------------
st.sidebar.title("SaaS Navigation")
nav = st.sidebar.radio(
    "Go to",
    [
        "Login",
        "Dashboard",
        "Real-time Monitoring",
        "Analytics & Predictions",
        "Optimization",
        "ESG Reporting",
        "Billing",
    ],
)

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None


# -------------------------------------------------------------------
# Login
# -------------------------------------------------------------------
def login_form():
    st.subheader("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            r = requests.post(
                f"{BACKEND}/users/login",
                json={"user_id": user_id, "password": password},
                timeout=5,
            )
        except Exception as e:
            st.error(f"Backend unreachable: {e}")
            return
        if r.ok:
            st.session_state["user_id"] = user_id
            st.success("Logged in as " + user_id)
        else:
            st.error("Login failed!")


# -------------------------------------------------------------------
# Dashboard (improved UI)
# -------------------------------------------------------------------
def dashboard_page():
    # CSS + header
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(90deg, #b8e8dc, #d4f4ea);
            padding: 16px 22px;
            border-radius: 14px;
            color: #013220;
            margin-bottom: 18px;
            border: 1px solid #a0d5c8;
        }
        .main-header h1 {
            margin: 0;
            font-size: 26px;
            color: #013220;
            font-weight: 700;
        }
        .main-header p {
            margin: 4px 0 0 0;
            font-size: 13px;
            color: #005849;
            opacity: 0.9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please login first from the **Login** page on the left.")
        return

    st.markdown(
        f"""
        <div class="main-header">
            <h1>🌍 Sustainability Command Center</h1>
            <p>
                Welcome, <b>{user_id}</b> &nbsp;·&nbsp;
                Live overview of energy, carbon, anomalies and device health.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_data = None  # will fill if API works

    # Top: score + KPIs
    score_col, kpi_col = st.columns([1, 2])

    # ------- Score block -------
    try:
        score_resp = requests.get(
            f"{BACKEND}/energy/sustainability_score/{user_id}", timeout=5
        )
        if score_resp.ok:
            score_data = score_resp.json()
            with score_col:
                st.subheader("Overall Sustainability Score")
                st.metric("Score", f"{score_data['overall_score']}/100")
                st.metric("Grade", score_data["grade"])

                if score_data["overall_score"] >= 80:
                    st.success("Excellent performance 🌟 – ahead of benchmarks.")
                elif score_data["overall_score"] >= 60:
                    st.info("Good progress 👍 – room for further gains.")
                else:
                    st.warning("Needs improvement ⚠️ – focus on high-impact actions.")
        else:
            with score_col:
                st.error("Could not load sustainability score.")
    except Exception as e:
        with score_col:
            st.error(f"Error loading score: {e}")

    # ------- KPI block -------
    try:
        resp = requests.get(
            f"{BACKEND}/energy/sensor_data/{user_id}", timeout=5
        )
        if resp.ok:
            data = resp.json()
            with kpi_col:
                st.subheader("📊 Key Performance Indicators (last reading)")

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Energy (kWh)", data["kpi"]["total_energy"])
                k2.metric("Carbon (kg)", data["kpi"]["total_carbon"])
                k3.metric("Anomalies", data["kpi"]["anomalies"])
                k4.metric("Active Devices", data["kpi"]["active_devices"])

                k5, k6 = st.columns(2)
                k5.metric("Avg Temperature (°C)", data["kpi"]["avg_temperature"])
                k6.metric(
                    "Avg Occupancy",
                    f"{data['kpi']['avg_occupancy'] * 100:.0f}%",
                )

                # Quick insight
                st.markdown("#### 🧠 Quick insight (auto summary)")
                issues = []

                if data["kpi"]["anomalies"] > 0:
                    issues.append("• Anomalies detected in current energy usage.")
                if data["kpi"]["total_carbon"] > 0:
                    issues.append(
                        "• Carbon emissions are being generated by current demand."
                    )
                if data["kpi"]["avg_occupancy"] > 0.7:
                    issues.append(
                        "• High occupancy – check HVAC and lighting schedules."
                    )

                if not issues:
                    st.success(
                        "System looks healthy – no major issues detected in this snapshot."
                    )
                else:
                    st.warning("\n".join(issues))
        else:
            with kpi_col:
                st.error("Could not load KPI data.")
    except Exception as e:
        with kpi_col:
            st.error(f"Error loading dashboard KPIs: {e}")

    st.markdown("---")

    # ------- Score breakdown chart -------
    st.subheader("Score breakdown by sustainability dimension")
    try:
        if score_data is None:
            score_resp = requests.get(
                f"{BACKEND}/energy/sustainability_score/{user_id}", timeout=5
            )
            if score_resp.ok:
                score_data = score_resp.json()

        if score_data is not None:
            factors_df = pd.DataFrame(
                score_data["factors"], columns=["Factor", "Score"]
            )
            fig = px.bar(
                factors_df,
                x="Factor",
                y="Score",
                title="Contribution of each factor to overall score",
                color="Score",
                color_continuous_scale="Greens",
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                yaxis_title="Score (0–100)",
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading score breakdown: {e}")


# -------------------------------------------------------------------
# Real-time Monitoring (improved UI)
# -------------------------------------------------------------------
def realtime_monitoring():
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please login first from the Login page.")
        return

    # Page header
    st.markdown(
        """
        <style>
        .rt-header {
            background: linear-gradient(90deg, #b8dce8, #d4eef4);
            padding: 14px 20px;
            border-radius: 14px;
            color: #004b7a;
            margin-bottom: 16px;
            border: 1px solid #a0c8d8;
        }
        .rt-header h2 {
            margin: 0;
            font-size: 22px;
            color: #004b7a;
            font-weight: 700;
        }
        .rt-header p {
            margin: 4px 0 0 0;
            font-size: 13px;
            color: #005870;
            opacity: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(
            """
            <div class="rt-header">
                <h2>🔴 Real-time Monitoring</h2>
                <p>Live view of energy, temperature and occupancy across your site.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_col2:
        st.write("")
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # Load data once
    try:
        resp = requests.get(
            f"{BACKEND}/energy/sensor_data/{user_id}", timeout=5
        )
        if not resp.ok:
            st.error("Could not load real-time data.")
            return
        data = resp.json()
    except Exception as e:
        st.error(f"Backend error: {e}")
        return

    # KPI summary
    st.subheader("📊 Live Summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Energy (kWh)", data["kpi"]["total_energy"])
    c2.metric("Carbon (kg)", data["kpi"]["total_carbon"])
    c3.metric("Anomalies", data["kpi"]["anomalies"])
    c4.metric("Active Devices", data["kpi"]["active_devices"])
    c5.metric("Avg Temp (°C)", data["kpi"]["avg_temperature"])

    st.markdown("---")

    left, right = st.columns([2, 2])

    # LEFT: Energy meters
    with left:
        st.subheader("⚡ Energy Meters")
        energy_df = pd.DataFrame(data["raw"]["energy_meters"])

        fig_energy = go.Figure()
        fig_energy.add_trace(
            go.Bar(
                x=energy_df["device_id"],
                y=energy_df["energy_kwh"],
                marker_color=[
                    "red" if anomaly else "green"
                    for anomaly in energy_df["anomaly"]
                ],
            )
        )
        fig_energy.update_layout(
            title="Energy Consumption by Device",
            xaxis_title="Device",
            yaxis_title="kWh",
        )
        st.plotly_chart(fig_energy, use_container_width=True)

        st.caption("🔴 Red = Anomaly detected. Green = Normal device behavior.")
        st.dataframe(energy_df, use_container_width=True)

    # RIGHT: Temperature + Occupancy
    with right:
        st.subheader("🌡️ Temperature Sensors")
        temp_df = pd.DataFrame(data["raw"]["temperature_sensors"])

        fig_temp = go.Figure()
        fig_temp.add_trace(
            go.Bar(
                x=temp_df["device_id"],
                y=temp_df["temperature_c"],
            )
        )
        fig_temp.update_layout(
            title="Temperature by Sensor",
            xaxis_title="Sensor",
            yaxis_title="°C",
        )
        st.plotly_chart(fig_temp, use_container_width=True)

        st.subheader("👥 Occupancy Sensors")
        occ_df = pd.DataFrame(data["raw"]["occupancy_sensors"])

        fig_occ = px.pie(
            occ_df,
            values="people_count",
            names="device_id",
            hole=0.4,
            title="People Distribution by Zone",
        )
        st.plotly_chart(fig_occ, use_container_width=True)


# -------------------------------------------------------------------
# The remaining pages are copied from the original dashboard.py
# (no UI changes yet – we can improve them later)
# -------------------------------------------------------------------
def analytics_predictions():
    st.title("📈 Analytics & Predictions")
    user_id = st.session_state["user_id"]
    if not user_id:
        st.warning("Please login first")
        return

    # Historical data
    st.subheader("Historical Energy Consumption")
    try:
        hist_resp = requests.get(
            f"{BACKEND}/energy/historical/{user_id}?hours=168", timeout=5
        )
        if hist_resp.ok:
            hist_data = hist_resp.json()["historical_data"]
            hist_df = pd.DataFrame(hist_data)

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=hist_df["timestamp"],
                    y=hist_df["total_energy_kwh"],
                    mode="lines+markers",
                    name="Energy",
                    line=dict(color="blue", width=2),
                )
            )
            fig.update_layout(
                title="Energy Consumption - Last 7 Days",
                xaxis_title="Time",
                yaxis_title="kWh",
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading historical data: {e}")

    # Predictions
    st.subheader("Energy Demand Forecast")
    forecast_hours = st.slider("Forecast Hours", 6, 48, 24)

    try:
        pred_resp = requests.get(
            f"{BACKEND}/energy/predict/{user_id}?forecast_hours={forecast_hours}",
            timeout=5,
        )
        if pred_resp.ok:
            pred_data = pred_resp.json()["predictions"]
            pred_df = pd.DataFrame(pred_data)

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=pred_df["timestamp"],
                    y=pred_df["predicted_energy_kwh"],
                    mode="lines+markers",
                    name="Forecast",
                    line=dict(color="red", width=2, dash="dash"),
                )
            )
            fig2.update_layout(
                title=f"Energy Forecast - Next {forecast_hours} Hours",
                xaxis_title="Time",
                yaxis_title="Predicted kWh",
            )
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading predictions: {e}")

    # Carbon footprint
    st.subheader("Carbon Footprint Analysis")
    try:
        carbon_resp = requests.get(
            f"{BACKEND}/energy/carbon_footprint/{user_id}", timeout=5
        )
        if carbon_resp.ok:
            carbon = carbon_resp.json()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Carbon (tons)", carbon["total_carbon_tons"])
            col2.metric("Equivalent Trees Needed", carbon["equivalent_trees"])
            col3.metric(
                "Equivalent km Driven", f"{carbon['equivalent_km_driven']:,.0f}"
            )
    except Exception as e:
        st.error(f"Error loading carbon data: {e}")


def optimization_page():
    st.title("🎯 Energy Optimization")
    user_id = st.session_state["user_id"]
    if not user_id:
        st.warning("Please login first")
        return

    try:
        opt_resp = requests.get(
            f"{BACKEND}/energy/optimize/{user_id}", timeout=5
        )
        if opt_resp.ok:
            opt_data = opt_resp.json()

            # Savings potential
            st.subheader("💰 Savings Potential")
            col1, col2, col3 = st.columns(3)
            col1.metric(
                "Potential Savings (kWh)",
                opt_data["total_savings_potential_kwh"],
            )
            col2.metric(
                "Cost Savings ($)", opt_data["total_savings_potential_cost"]
            )
            col3.metric("ROI Period (months)", opt_data["roi_months"])

            # Recommendations
            st.subheader("📋 Optimization Recommendations")
            for rec in opt_data["recommendations"]:
                with st.expander(
                    f"🔹 {rec['category']} - Priority: {rec['priority']}"
                ):
                    st.write(f"**Recommendation:** {rec['recommendation']}")
                    col_a, col_b = st.columns(2)
                    col_a.metric("Savings (kWh)", rec["potential_savings_kwh"])
                    col_b.metric(
                        "Savings (%)",
                        f"{rec['potential_savings_percent']}%",
                    )
    except Exception as e:
        st.error(f"Error loading optimization: {e}")


def esg_reporting():
    st.title("📄 ESG Reporting")
    user_id = st.session_state["user_id"]
    if not user_id:
        st.warning("Please login first")
        return

    timeframe = st.selectbox("Select Timeframe", ["monthly", "quarterly", "yearly"])

    if st.button("Generate ESG Report"):
        try:
            esg_resp = requests.get(
                f"{BACKEND}/energy/esg_report/{user_id}?timeframe={timeframe}",
                timeout=5,
            )
            if esg_resp.ok:
                report = esg_resp.json()

                st.subheader(f"ESG Report - {timeframe.capitalize()}")
                st.caption(f"Generated: {report['report_date']}")

                # Environmental metrics
                with st.expander("🌱 Environmental Metrics", expanded=True):
                    env = report["environmental"]
                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "Energy Consumption",
                        f"{env['energy_consumption_kwh']} kWh",
                    )
                    col2.metric(
                        "Carbon Emissions",
                        f"{env['carbon_emissions_kg']} kg",
                    )
                    col3.metric(
                        "Renewable Energy %",
                        f"{env['renewable_energy_percent']}%",
                    )

                    col4, col5 = st.columns(2)
                    col4.metric(
                        "Waste Reduction %",
                        f"{env['waste_reduction_percent']}%",
                    )
                    col5.metric(
                        "Water Usage", f"{env['water_usage_liters']} L"
                    )

                # Social metrics
                with st.expander("👥 Social Metrics"):
                    social = report["social"]
                    st.write(
                        f"**Employee Satisfaction:** {social['employee_satisfaction']}/5"
                    )
                    st.write(
                        f"**Safety Incidents:** {social['safety_incidents']}"
                    )
                    st.write(
                        f"**Training Hours:** {social['training_hours']}"
                    )

                # Governance metrics
                with st.expander("⚖️ Governance Metrics"):
                    gov = report["governance"]
                    st.write(
                        f"**Compliance Score:** {gov['compliance_score']}/100"
                    )
                    st.write(f"**Audit Status:** {gov['audit_status']}")
                    st.write(
                        f"**Policy Updates:** {gov['policy_updates']}"
                    )

                # Initiatives
                st.subheader("✅ Sustainability Initiatives")
                for initiative in report["sustainability_initiatives"]:
                    st.success(f"✓ {initiative}")

                # Next steps
                st.subheader("🎯 Next Steps")
                for step in report["next_steps"]:
                    st.info(f"→ {step}")

                if st.button("📥 Download Report (JSON)"):
                    st.download_button(
                        label="Download",
                        data=str(report),
                        file_name=f"esg_report_{timeframe}_{user_id}.json",
                        mime="application/json",
                    )
        except Exception as e:
            st.error(f"Error generating report: {e}")

    # File upload for ESG analysis
    st.subheader("📤 Upload ESG Document for AI Analysis")
    uploaded_file = st.file_uploader("Upload ESG document (CSV/TXT)")
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            r = requests.post(
                f"{BACKEND}/esg/upload", files=files, timeout=10
            )
            if r.ok:
                result = r.json()
                st.success("Analysis complete!")
                st.json(result)
        except Exception as e:
            st.error(f"Upload failed: {e}")


def billing_page():
    st.title("💳 Billing & Subscription")
    user_id = st.session_state["user_id"]
    if not user_id:
        st.warning("Please login first")
        return

    try:
        plans = requests.get(f"{BACKEND}/billing/plans").json()
        user_plan = (
            requests.get(f"{BACKEND}/billing/get_plan/{user_id}")
            .json()
            .get("plan", "basic")
        )

        st.write(f"Current subscription: **{user_plan.capitalize()}**")

        for plan, info in plans.items():
            with st.expander(f"{plan.capitalize()} - ${info['price']}/mo"):
                st.write("**Features:**")
                for feature in info["features"]:
                    st.write(f"✓ {feature}")
                if (
                    st.button(
                        f"Upgrade to {plan.capitalize()}", key=plan
                    )
                    and plan != user_plan
                ):
                    r = requests.post(
                        f"{BACKEND}/billing/upgrade",
                        json={"user_id": user_id, "new_plan": plan},
                    )
                    if r.ok:
                        st.success(f"Upgraded to {plan.capitalize()}!")
                        st.rerun()
    except Exception as e:
        st.error(f"Error loading billing: {e}")


# -------------------------------------------------------------------
# Navigation routing
# -------------------------------------------------------------------
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
