# dashboard/dashboard.py
import streamlit as st
import requests

st.set_page_config(page_title='Sustainability-as-a-Service', layout='wide')

BACKEND = "http://localhost:5000"

st.sidebar.title("SaaS Navigation")
nav = st.sidebar.radio("Go to", ["Login", "Dashboard", "Billing", "ESG Compliance"])

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
    st.title("Sustainability Dashboard")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    st.write(f"Welcome, {user_id}")
    try:
        resp = requests.get(f"{BACKEND}/energy/sensor_data/{user_id}", timeout=5)
    except Exception as e:
        st.error(f"Backend unreachable: {e}")
        return
    if resp.ok:
        data = resp.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Energy (kWh)", data['kpi']['total_energy'])
        col2.metric("Total Carbon (kg)", data['kpi']['total_carbon'])
        col3.metric("Anomalies", data['kpi']['anomalies'])
        st.subheader("Device data")
        st.table(data['raw'])
        st.subheader("Energy Prediction")
        st.write(f"Predicted next day usage: **{data['predict_next_day_kwh']} kWh**")
        st.line_chart(data["history_kwh"] + [data['predict_next_day_kwh']])
        st.subheader("AI Recommendations")
        for rec in data["recommendations"]:
            st.info(rec)

def billing_page():
    st.title("Billing & Subscription")
    user_id = st.session_state['user_id']
    if not user_id:
        st.warning("Please login first")
        return
    plans = requests.get(f"{BACKEND}/billing/plans").json()
    user_plan = requests.get(f"{BACKEND}/billing/get_plan/{user_id}").json().get("plan", "basic")
    st.write(f"Current subscription: **{user_plan.capitalize()}**")
    for plan, info in plans.items():
        st.write(f"### {plan.capitalize()} - ${info['price']}/mo")
        st.write("**Features:**", ", ".join(info['features']))
        if st.button(f"Upgrade to {plan.capitalize()}", key=plan) and plan != user_plan:
            r = requests.post(f"{BACKEND}/billing/upgrade", json={
                "user_id": user_id, "new_plan": plan
            })
            if r.ok:
                st.success(f"Upgraded to {plan.capitalize()}!")
            else:
                st.error("Upgrade failed")

def esg_tab():
    st.title("ESG/Compliance Analysis (AI-Powered)")
    st.write("Upload an ESG or sustainability report (text or CSV). The AI engine will extract and summarize KPIs.")
    uploaded_file = st.file_uploader("Upload ESG document")
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            r = requests.post(f"{BACKEND}/esg/upload", files=files, timeout=10)
        except Exception as e:
            st.error(f"Upload failed: {e}")
            return
        if r.ok:
            result = r.json()
            st.subheader("AI-generated ESG KPI Summary:")
            st.json(result)
        else:
            st.error("Upload or extraction failed.")

if nav == "Login":
    login_form()
elif nav == "Dashboard":
    dashboard_page()
elif nav == "Billing":
    billing_page()
elif nav == "ESG Compliance":
    esg_tab()