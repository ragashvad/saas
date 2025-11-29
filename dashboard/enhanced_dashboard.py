# dashboard/enhanced_dashboard.py
"""
Enhanced Sustainability Dashboard with Pulsora-inspired UI
Modern, card-based layout with advanced features
"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Page configuration with custom theme
st.set_page_config(
    page_title='EcoMetrics | Enterprise Sustainability Platform',
    page_icon='🌱',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'About': "EcoMetrics - Enterprise Sustainability & Carbon Management Platform"
    }
)

# Custom CSS for modern, professional UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main theme colors */
    :root {
        --primary-blue: #2563eb;
        --primary-green: #059669;
        --neutral-50: #f9fafb;
        --neutral-100: #f3f4f6;
        --neutral-200: #e5e7eb;
        --neutral-700: #374151;
        --neutral-900: #111827;
    }
    
    /* Card styling - Natural shadows */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--neutral-200);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.2s;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--neutral-900);
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--neutral-700);
        text-transform: none;
        letter-spacing: 0;
    }
    
    /* Header styling - Professional */
    .main-header {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--neutral-900);
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--neutral-900);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Status badges - Refined */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar refinement */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid var(--neutral-200);
    }
    
    /* Button styling - Natural */
    .stButton>button {
        background: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.15s;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .stButton>button:hover {
        background: #1d4ed8;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    /* Metric containers */
    [data-testid="stMetricValue"] {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--neutral-900);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--neutral-700);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: var(--primary-blue);
    }
</style>
""", unsafe_allow_html=True)

BACKEND = "http://localhost:5000"

# Session state initialization
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

# Sidebar navigation
with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🌱</div>
        <div style='font-size: 1.25rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem;'>EcoMetrics</div>
        <div style='font-size: 0.75rem; color: #6b7280; font-weight: 500;'>Sustainability Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #e5e7eb;'>", unsafe_allow_html=True)
    
    if st.session_state['user_id']:
        st.markdown(f"""
        <div style='background: #f3f4f6; padding: 0.75rem; border-radius: 8px; margin-bottom: 1.5rem;'>
            <div style='font-size: 0.75rem; color: #6b7280; margin-bottom: 0.25rem;'>Logged in as</div>
            <div style='font-weight: 600; color: #111827;'>{st.session_state['user_id']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign Out", use_container_width=True):
            st.session_state['user_id'] = None
            st.rerun()
    
    st.markdown("<div style='font-size: 0.75rem; font-weight: 600; color: #6b7280; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;'>Navigation</div>", unsafe_allow_html=True)
    
    nav = st.radio(
        "Navigate to",
        [
            "Overview",
            "Carbon Footprint",
            "Supply Chain",
            "Climate Targets",
            "Analytics",
            "ESG Reports",
            "Settings"
        ],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Overview": "📊 Dashboard",
            "Carbon Footprint": "🌍 Carbon Footprint",
            "Supply Chain": "🔗 Supply Chain",
            "Climate Targets": "🎯 Climate Targets",
            "Analytics": "📈 Analytics",
            "ESG Reports": "📋 ESG Reports",
            "Settings": "⚙️ Settings"
        }.get(x, x)
    )
    
    st.markdown("<div style='margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='padding: 0.75rem; background: #f9fafb; border-radius: 8px; margin-bottom: 1rem;'>
        <div style='font-size: 0.75rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;'>Quick Links</div>
        <div style='font-size: 0.8rem;'>
            <a href='#' style='color: #2563eb; text-decoration: none; display: block; margin-bottom: 0.25rem;'>📚 Documentation</a>
            <a href='#' style='color: #2563eb; text-decoration: none; display: block; margin-bottom: 0.25rem;'>🔧 API Reference</a>
            <a href='#' style='color: #2563eb; text-decoration: none; display: block;'>💬 Support</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding-top: 1rem;'>
        <div style='font-size: 0.7rem; color: #9ca3af;'>EcoMetrics v2.0</div>
        <div style='font-size: 0.7rem; color: #9ca3af;'>© 2025 All rights reserved</div>
    </div>
    """, unsafe_allow_html=True)

def login_page():
    """Modern login interface"""
    st.markdown("<h1 class='main-header'>Welcome to EcoMetrics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; font-size: 1rem; margin-bottom: 3rem;'>Sign in to access your sustainability intelligence platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='metric-card' style='padding: 2rem;'>
            <h3 style='margin-bottom: 1.5rem; color: #111827;'>Sign In</h3>
        """, unsafe_allow_html=True)
        
        user_id = st.text_input("User ID", placeholder="Enter your user ID", label_visibility="visible")
        password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="visible")
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True):
            try:
                r = requests.post(f"{BACKEND}/users/login", json={
                    "user_id": user_id, "password": password
                }, timeout=5)
                if r.ok:
                    st.session_state["user_id"] = user_id
                    st.success("✓ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Connection error: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #f3f4f6; padding: 1rem; border-radius: 8px; margin-top: 1.5rem;'>
            <div style='font-size: 0.875rem; font-weight: 600; color: #111827; margin-bottom: 0.5rem;'>Demo Accounts</div>
            <div style='font-size: 0.875rem; color: #6b7280;'>
                • user1 / password1 (Basic Plan)<br>
                • user2 / password2 (Professional Plan)
            </div>
        </div>
        """, unsafe_allow_html=True)

def overview_page():
    """Enhanced overview dashboard"""
    user_id = st.session_state['user_id']
    
    st.markdown("<h1 class='main-header'>Dashboard Overview</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #6b7280; margin-bottom: 2rem;'>Welcome back, <strong>{user_id}</strong> • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>", unsafe_allow_html=True)
    
    # Top KPI cards
    try:
        score_resp = requests.get(f"{BACKEND}/energy/sustainability_score/{user_id}", timeout=5)
        carbon_resp = requests.get(f"{BACKEND}/energy/carbon_footprint/{user_id}", timeout=5)
        targets_resp = requests.get(f"{BACKEND}/targets/targets/{user_id}", timeout=5)
        
        if all([score_resp.ok, carbon_resp.ok, targets_resp.ok]):
            score_data = score_resp.json()
            carbon_data = carbon_resp.json()
            targets_data = targets_resp.json()
            
            # KPI Row - Professional metrics
            st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score = score_data['overall_score']
                grade = score_data['grade']
                grade_colors = {'A': '#059669', 'B': '#10b981', 'C': '#f59e0b', 'D': '#ef4444'}
                st.markdown(f"""
                <div class="metric-card">
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
                        <div style='color: #6b7280; font-size: 0.875rem; font-weight: 500;'>Sustainability Score</div>
                        <span style='background: {grade_colors.get(grade, '#6b7280')}; color: white; padding: 0.125rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;'>{grade}</span>
                    </div>
                    <div style='font-size: 2.25rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem;'>{score}<span style='font-size: 1.5rem; color: #9ca3af;'>/100</span></div>
                    <div style='font-size: 0.75rem; color: #059669; font-weight: 500;'>↑ 5 pts from last month</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_carbon = carbon_data['total_carbon_kg']
                st.markdown(f"""
                <div class="metric-card">
                    <div style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 1rem;'>Total Emissions</div>
                    <div style='font-size: 2.25rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem;'>{total_carbon/1000:.1f}<span style='font-size: 1rem; color: #9ca3af;'> tCO₂e</span></div>
                    <div style='font-size: 0.75rem; color: #ef4444; font-weight: 500;'>↓ 12% reduction YoY</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                progress = targets_data['primary_target']['reduction_achieved_percent']
                target_year = targets_data['primary_target']['target_year']
                st.markdown(f"""
                <div class="metric-card">
                    <div style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 1rem;'>Target Progress</div>
                    <div style='font-size: 2.25rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem;'>{progress}%</div>
                    <div style='background: #e5e7eb; height: 6px; border-radius: 3px; overflow: hidden; margin-bottom: 0.5rem;'>
                        <div style='background: #2563eb; height: 100%; width: {progress}%;'></div>
                    </div>
                    <div style='font-size: 0.75rem; color: #6b7280;'>Net Zero by {target_year}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                trees = carbon_data['equivalent_trees']
                st.markdown(f"""
                <div class="metric-card">
                    <div style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 1rem;'>Climate Impact</div>
                    <div style='font-size: 2.25rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem;'>{trees:.0f}</div>
                    <div style='font-size: 0.75rem; color: #6b7280;'>Trees required to offset</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 2.5rem 0 2rem 0;'></div>", unsafe_allow_html=True)
            
            # Main content area
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.markdown("<div class='section-header'>Emissions Trend Analysis</div>", unsafe_allow_html=True)
                hist_resp = requests.get(f"{BACKEND}/energy/historical/{user_id}?hours=168", timeout=5)
                if hist_resp.ok:
                    hist_data = hist_resp.json()['historical_data']
                    df = pd.DataFrame(hist_data)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=df['total_carbon_kg'],
                        mode='lines',
                        name='Carbon Emissions',
                        line=dict(color='#2563eb', width=2),
                        fill='tozeroy',
                        fillcolor='rgba(37, 99, 235, 0.1)'
                    ))
                    fig.update_layout(
                        height=300,
                        margin=dict(l=0, r=0, t=20, b=0),
                        xaxis_title="",
                        yaxis_title="Emissions (kg CO₂e)",
                        hovermode='x unified',
                        showlegend=False,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(family='Inter, sans-serif', size=12, color='#374151')
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col_right:
                st.markdown("<div class='section-header'>Climate Target Status</div>", unsafe_allow_html=True)
                
                target_type = targets_data['primary_target']['type']
                target_year = targets_data['primary_target']['target_year']
                is_on_track = targets_data['primary_target']['on_track']
                
                st.markdown(f"""
                <div class='metric-card' style='margin-bottom: 1rem;'>
                    <div style='color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;'>Commitment</div>
                    <div style='font-size: 1.25rem; font-weight: 600; color: #111827; margin-bottom: 0.5rem;'>{target_type}</div>
                    <div style='color: #6b7280; font-size: 0.875rem;'>Target year: {target_year}</div>
                </div>
                """, unsafe_allow_html=True)
                
                status_color = '#059669' if is_on_track else '#f59e0b'
                status_text = 'On Track' if is_on_track else 'Needs Attention'
                status_icon = '✓' if is_on_track else '⚠'
                
                st.markdown(f"""
                <div style='background: {status_color}15; border: 1px solid {status_color}; padding: 0.75rem; border-radius: 8px; margin-bottom: 1.5rem;'>
                    <div style='color: {status_color}; font-weight: 600; font-size: 0.875rem;'>{status_icon} {status_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='color: #374151; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.75rem;'>Performance Factors</div>", unsafe_allow_html=True)
                for factor, score in score_data['factors']:
                    st.markdown(f"""
                    <div style='margin-bottom: 0.75rem;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 0.25rem;'>
                            <span style='font-size: 0.8rem; color: #6b7280;'>{factor}</span>
                            <span style='font-size: 0.8rem; font-weight: 600; color: #111827;'>{score}</span>
                        </div>
                        <div style='background: #e5e7eb; height: 4px; border-radius: 2px; overflow: hidden;'>
                            <div style='background: #2563eb; height: 100%; width: {score}%;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Bottom section - More professional
            st.markdown("<div style='margin: 3rem 0 2rem 0;'></div>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("<div class='section-header'>Quick Actions</div>", unsafe_allow_html=True)
                st.markdown("""
                <div class='metric-card'>
                    <button style='width: 100%; background: white; border: 1px solid #e5e7eb; padding: 0.75rem; border-radius: 6px; text-align: left; cursor: pointer; margin-bottom: 0.5rem; font-family: Inter, sans-serif;'>
                        <div style='font-weight: 500; color: #111827; margin-bottom: 0.25rem;'>📊 Generate Monthly Report</div>
                        <div style='font-size: 0.75rem; color: #6b7280;'>Export comprehensive ESG report</div>
                    </button>
                    <button style='width: 100%; background: white; border: 1px solid #e5e7eb; padding: 0.75rem; border-radius: 6px; text-align: left; cursor: pointer; margin-bottom: 0.5rem; font-family: Inter, sans-serif;'>
                        <div style='font-weight: 500; color: #111827; margin-bottom: 0.25rem;'>📤 Upload Activity Data</div>
                        <div style='font-size: 0.75rem; color: #6b7280;'>Import energy, water, waste data</div>
                    </button>
                    <button style='width: 100%; background: white; border: 1px solid #e5e7eb; padding: 0.75rem; border-radius: 6px; text-align: left; cursor: pointer; font-family: Inter, sans-serif;'>
                        <div style='font-weight: 500; color: #111827; margin-bottom: 0.25rem;'>🔔 Configure Alerts</div>
                        <div style='font-size: 0.75rem; color: #6b7280;'>Set thresholds and notifications</div>
                    </button>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown("<div class='section-header'>Recent Activity</div>", unsafe_allow_html=True)
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 0.875rem; margin-bottom: 0.75rem;'>
                        <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                            <span style='color: #059669; margin-right: 0.5rem;'>✓</span>
                            <span style='color: #374151;'>Q4 Carbon Report completed</span>
                        </div>
                        <div style='font-size: 0.75rem; color: #9ca3af; margin-left: 1.25rem;'>2 hours ago</div>
                    </div>
                    <div style='font-size: 0.875rem; margin-bottom: 0.75rem;'>
                        <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                            <span style='color: #2563eb; margin-right: 0.5rem;'>⟳</span>
                            <span style='color: #374151;'>Supplier emissions data updated</span>
                        </div>
                        <div style='font-size: 0.75rem; color: #9ca3af; margin-left: 1.25rem;'>Yesterday at 3:45 PM</div>
                    </div>
                    <div style='font-size: 0.875rem; margin-bottom: 0.75rem;'>
                        <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                            <span style='color: #059669; margin-right: 0.5rem;'>📊</span>
                            <span style='color: #374151;'>New industry benchmark available</span>
                        </div>
                        <div style='font-size: 0.75rem; color: #9ca3af; margin-left: 1.25rem;'>3 days ago</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_c:
                st.markdown("<div class='section-header'>Monthly Objectives</div>", unsafe_allow_html=True)
                st.markdown("""
                <div class='metric-card'>
                    <div style='margin-bottom: 0.75rem;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;'>
                            <span style='font-size: 0.875rem; color: #374151;'>Reduce energy consumption</span>
                            <span style='font-size: 0.75rem; color: #059669; font-weight: 600;'>65%</span>
                        </div>
                        <div style='background: #e5e7eb; height: 4px; border-radius: 2px; overflow: hidden;'>
                            <div style='background: #059669; height: 100%; width: 65%;'></div>
                        </div>
                    </div>
                    <div style='margin-bottom: 0.75rem;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;'>
                            <span style='font-size: 0.875rem; color: #374151;'>Complete supplier surveys</span>
                            <span style='font-size: 0.75rem; color: #f59e0b; font-weight: 600;'>40%</span>
                        </div>
                        <div style='background: #e5e7eb; height: 4px; border-radius: 2px; overflow: hidden;'>
                            <div style='background: #f59e0b; height: 100%; width: 40%;'></div>
                        </div>
                    </div>
                    <div style='margin-bottom: 0.75rem;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;'>
                            <span style='font-size: 0.875rem; color: #374151;'>Update emission factors</span>
                            <span style='font-size: 0.75rem; color: #2563eb; font-weight: 600;'>80%</span>
                        </div>
                        <div style='background: #e5e7eb; height: 4px; border-radius: 2px; overflow: hidden;'>
                            <div style='background: #2563eb; height: 100%; width: 80%;'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

def carbon_accounting_page():
    """Detailed carbon accounting with Scope 1, 2, 3"""
    user_id = st.session_state['user_id']
    
    st.markdown("<h1 class='main-header'>Carbon Footprint Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 2rem;'>Comprehensive greenhouse gas emissions tracking across all scopes</p>", unsafe_allow_html=True)
    
    try:
        scope3_resp = requests.get(f"{BACKEND}/supply_chain/scope3/{user_id}", timeout=5)
        carbon_resp = requests.get(f"{BACKEND}/energy/carbon_footprint/{user_id}", timeout=5)
        
        if scope3_resp.ok and carbon_resp.ok:
            scope3_data = scope3_resp.json()
            carbon_data = carbon_resp.json()
            
            # Scopes comparison
            st.markdown("### 📊 Emissions by Scope")
            col1, col2, col3 = st.columns(3)
            
            scopes = scope3_data['comparison']
            total = scopes['scope1'] + scopes['scope2'] + scopes['scope3']
            
            with col1:
                pct = (scopes['scope1'] / total * 100)
                st.metric("Scope 1 (Direct)", f"{scopes['scope1']:,.0f} kg", f"{pct:.1f}%")
            
            with col2:
                pct = (scopes['scope2'] / total * 100)
                st.metric("Scope 2 (Energy)", f"{scopes['scope2']:,.0f} kg", f"{pct:.1f}%")
            
            with col3:
                pct = (scopes['scope3'] / total * 100)
                st.metric("Scope 3 (Value Chain)", f"{scopes['scope3']:,.0f} kg", f"{pct:.1f}%")
            
            # Pie chart
            fig = px.pie(
                values=[scopes['scope1'], scopes['scope2'], scopes['scope3']],
                names=['Scope 1', 'Scope 2', 'Scope 3'],
                title='Emissions Distribution',
                color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Scope 3 breakdown
            st.markdown("### 🔗 Scope 3 Category Breakdown")
            scope3_df = pd.DataFrame(scope3_data['categories'])
            
            fig2 = px.bar(
                scope3_df,
                x='name',
                y='emissions_kg',
                color='percentage',
                title='Scope 3 by Category',
                labels={'emissions_kg': 'Emissions (kg CO₂e)', 'name': 'Category'},
                color_continuous_scale='Viridis'
            )
            fig2.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Data quality
            st.markdown("### 📈 Data Quality Assessment")
            quality = scope3_data['data_quality']
            col_a, col_b, col_c = st.columns(3)
            
            col_a.metric("Primary Data", f"{quality['primary_data']}%", "Measured")
            col_b.metric("Secondary Data", f"{quality['secondary_data']}%", "Industry Avg")
            col_c.metric("Estimated Data", f"{quality['estimated_data']}%", "Calculated")
            
            st.progress(quality['primary_data']/100, text=f"Overall Quality: {quality['primary_data'] + quality['secondary_data']*0.5:.0f}%")
    
    except Exception as e:
        st.error(f"Error loading carbon data: {e}")

def supply_chain_page():
    """Supply chain emissions and supplier management"""
    user_id = st.session_state['user_id']
    
    st.markdown("<h1 class='main-header'>Supply Chain Emissions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 2rem;'>Track and manage Scope 3 emissions across your value chain</p>", unsafe_allow_html=True)
    
    try:
        suppliers_resp = requests.get(f"{BACKEND}/supply_chain/suppliers/{user_id}", timeout=5)
        engagement_resp = requests.get(f"{BACKEND}/supply_chain/supplier_engagement/{user_id}", timeout=5)
        value_chain_resp = requests.get(f"{BACKEND}/supply_chain/value_chain/{user_id}", timeout=5)
        
        if suppliers_resp.ok:
            supplier_data = suppliers_resp.json()
            
            # Supplier KPIs
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Suppliers", supplier_data['total_suppliers'])
            col2.metric("Verified", supplier_data['verified_suppliers'])
            col3.metric("Total Emissions", f"{supplier_data['total_emissions_kg']:,.0f} kg")
            
            if engagement_resp.ok:
                engagement = engagement_resp.json()
                col4.metric("Response Rate", f"{engagement['response_rate']}%")
            
            # Suppliers table
            st.markdown("### 📋 Supplier List")
            suppliers_df = pd.DataFrame(supplier_data['suppliers'])
            
            # Add status badges with HTML
            def status_badge(status):
                if status == 'verified':
                    return '✅ Verified'
                return '⏳ Pending'
            
            suppliers_df['Status'] = suppliers_df['status'].apply(status_badge)
            
            st.dataframe(
                suppliers_df[['name', 'category', 'emissions_kg', 'Status']],
                use_container_width=True,
                height=300
            )
            
            # Category breakdown
            st.markdown("### 📊 Emissions by Category")
            cat_data = supplier_data['by_category']
            cat_df = pd.DataFrame([
                {'Category': k, 'Suppliers': v['count'], 'Emissions': v['emissions']}
                for k, v in cat_data.items()
            ])
            
            fig = px.bar(
                cat_df,
                x='Category',
                y='Emissions',
                color='Suppliers',
                title='Supplier Emissions by Category'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Value chain analysis
            if value_chain_resp.ok:
                value_chain = value_chain_resp.json()
                
                st.markdown("### 🔗 Value Chain Emissions")
                col_a, col_b, col_c = st.columns(3)
                
                col_a.metric("Upstream", f"{value_chain['upstream']['total_emissions_kg']:,.0f} kg")
                col_b.metric("Operations", f"{value_chain['operations']['total_emissions_kg']:,.0f} kg")
                col_c.metric("Downstream", f"{value_chain['downstream']['total_emissions_kg']:,.0f} kg")
                
                # Hotspots
                st.markdown("### 🔥 Emission Hotspots")
                hotspots_df = pd.DataFrame(value_chain['upstream']['hotspots'])
                
                for idx, row in hotspots_df.iterrows():
                    with st.expander(f"🎯 {row['name']} - {row['emissions_kg']:,.0f} kg CO₂e"):
                        st.write(f"**Reduction Potential:** {row['reduction_potential']}%")
                        st.progress(row['reduction_potential']/100)
    
    except Exception as e:
        st.error(f"Error loading supply chain data: {e}")

def targets_progress_page():
    """Target management and progress tracking"""
    user_id = st.session_state['user_id']
    
    st.markdown("<h1 class='main-header'>Climate Targets & Progress</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 2rem;'>Monitor progress toward net-zero commitments and reduction goals</p>", unsafe_allow_html=True)
    
    try:
        targets_resp = requests.get(f"{BACKEND}/targets/targets/{user_id}", timeout=5)
        progress_resp = requests.get(f"{BACKEND}/targets/progress_tracking/{user_id}", timeout=5)
        pathway_resp = requests.get(f"{BACKEND}/targets/reduction_pathway/{user_id}", timeout=5)
        
        if targets_resp.ok:
            targets_data = targets_resp.json()
            
            # Primary target
            st.markdown("### 🎯 Primary Climate Target")
            target = targets_data['primary_target']
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Target Type", target['type'])
            col2.metric("Target Year", target['target_year'])
            col3.metric("Progress", f"{target['reduction_achieved_percent']}%")
            col4.metric("Status", "✅ On Track" if target['on_track'] else "⚠️ At Risk")
            
            # Progress bar
            st.progress(target['reduction_achieved_percent']/100, 
                       text=f"{target['reduction_achieved_percent']}% of target achieved")
            
            # Science-based target info
            sbt = targets_data['science_based']
            st.info(f"**Science-Based Target:** {sbt['framework']} | Status: {sbt['validation_status']}")
            
            # Interim targets
            st.markdown("### 📅 Interim Targets")
            interim_df = pd.DataFrame(targets_data['interim_targets'])
            
            for idx, row in interim_df.iterrows():
                col_a, col_b, col_c = st.columns([1, 2, 1])
                col_a.write(f"**{row['year']}**")
                col_b.progress(row['current_progress']/row['target_reduction'], 
                              text=f"{row['current_progress']}% / {row['target_reduction']}%")
                
                if row['status'] == 'On Track':
                    col_c.success(row['status'])
                elif row['status'] == 'At Risk':
                    col_c.warning(row['status'])
                else:
                    col_c.info(row['status'])
            
            # Reduction pathway
            if pathway_resp.ok:
                pathway_data = pathway_resp.json()
                
                st.markdown("### 🛤️ Reduction Pathway")
                timeline_df = pd.DataFrame([
                    {
                        'Year': item['year'],
                        'Target': item['emissions_target_kg'],
                        'Actual': item['emissions_actual_kg'] if item['emissions_actual_kg'] else None
                    }
                    for item in pathway_data['timeline']
                ])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timeline_df['Year'],
                    y=timeline_df['Target'],
                    mode='lines+markers',
                    name='Target',
                    line=dict(color='#667eea', width=3, dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=timeline_df['Year'],
                    y=timeline_df['Actual'],
                    mode='lines+markers',
                    name='Actual',
                    line=dict(color='#10b981', width=3)
                ))
                fig.update_layout(height=400, xaxis_title="Year", yaxis_title="Emissions (kg CO₂e)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Initiatives
                st.markdown("### 💡 Reduction Initiatives")
                for year_data in pathway_data['timeline'][:2]:  # Show first 2 years
                    with st.expander(f"📆 {year_data['year']} Initiatives"):
                        for init in year_data['initiatives']:
                            status_emoji = {'Completed': '✅', 'In Progress': '🔄', 'Planned': '📅', 'Under Review': '🔍'}
                            st.write(f"{status_emoji.get(init['status'], '•')} **{init['name']}**: {init['reduction_kg']:,.0f} kg CO₂e")
        
        # Progress tracking
        if progress_resp.ok:
            progress_data = progress_resp.json()
            
            st.markdown("### 📊 Monthly Performance")
            monthly_df = pd.DataFrame(progress_data['monthly_breakdown'])
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=monthly_df['month'], y=monthly_df['actual'], name='Actual', marker_color='#667eea'))
            fig.add_trace(go.Scatter(x=monthly_df['month'], y=monthly_df['target'], name='Target', 
                                    line=dict(color='#ef4444', width=2, dash='dash')))
            fig.update_layout(height=300, xaxis_title="Month", yaxis_title="Emissions (kg CO₂e)")
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading targets: {e}")

def analytics_insights_page():
    """Advanced analytics and insights"""
    user_id = st.session_state['user_id']
    
    st.markdown("<h1 class='main-header'>Sustainability Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 2rem;'>AI-powered insights and predictive analytics for smarter sustainability decisions</p>", unsafe_allow_html=True)
    
    try:
        # Get data from various endpoints
        analytics_resp = requests.get(f"{BACKEND}/analytics/{user_id}", timeout=5)
        energy_resp = requests.get(f"{BACKEND}/energy/real_time/{user_id}", timeout=5)
        
        # Predictive Analytics
        st.markdown("### 🔮 Predictive Analytics")
        
        if analytics_resp.ok:
            analytics_data = analytics_resp.json()
            
            col1, col2, col3 = st.columns(3)
            
            # Generate predictions
            pred_next_month = analytics_data.get('emissions_7d', 500) * 4.3
            pred_next_quarter = pred_next_month * 3
            pred_eoy = pred_next_month * 12
            
            with col1:
                st.markdown("""
                <div class='metric-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
                    <div class='metric-value'>{:,.0f} kg</div>
                    <div class='metric-label'>Next Month Forecast</div>
                </div>
                """.format(pred_next_month), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='metric-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
                    <div class='metric-value'>{:,.0f} kg</div>
                    <div class='metric-label'>Q1 2026 Projection</div>
                </div>
                """.format(pred_next_quarter), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class='metric-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
                    <div class='metric-value'>{:,.0f} kg</div>
                    <div class='metric-label'>End of Year Projection</div>
                </div>
                """.format(pred_eoy), unsafe_allow_html=True)
        
        # Anomaly Detection
        st.markdown("### 🚨 Anomaly Detection")
        
        if energy_resp.ok:
            energy_data = energy_resp.json()
            
            # Simulate anomaly detection
            anomalies = []
            if energy_data.get('total_consumption', 0) > 800:
                anomalies.append({
                    'type': 'High Energy Consumption',
                    'severity': 'Warning',
                    'value': energy_data['total_consumption'],
                    'message': f"Energy consumption ({energy_data['total_consumption']:.1f} kWh) is 15% above normal"
                })
            
            if energy_data.get('carbon_intensity', 0) > 0.5:
                anomalies.append({
                    'type': 'High Carbon Intensity',
                    'severity': 'Alert',
                    'value': energy_data['carbon_intensity'],
                    'message': f"Carbon intensity ({energy_data['carbon_intensity']:.3f} kg/kWh) exceeds threshold"
                })
            
            # Add some sample anomalies for demo
            anomalies.extend([
                {
                    'type': 'Temperature Spike',
                    'severity': 'Info',
                    'value': 28.5,
                    'message': 'Zone 2 temperature reached 28.5°C at 14:30'
                },
                {
                    'type': 'Water Usage Pattern',
                    'severity': 'Warning',
                    'value': 245,
                    'message': 'Unusual water usage detected in Building B (245L spike)'
                }
            ])
            
            for anomaly in anomalies:
                severity_colors = {
                    'Alert': '🔴',
                    'Warning': '🟡',
                    'Info': '🔵'
                }
                emoji = severity_colors.get(anomaly['severity'], '⚪')
                
                with st.expander(f"{emoji} {anomaly['type']} - {anomaly['severity']}"):
                    st.write(anomaly['message'])
                    st.caption(f"Detected at {datetime.now().strftime('%H:%M:%S')}")
        
        # Performance Insights
        st.markdown("### 💡 Performance Insights")
        
        insights = [
            {
                'icon': '📉',
                'title': 'Energy Efficiency Opportunity',
                'description': 'HVAC systems running 12% longer than optimal. Potential savings: 450 kg CO₂e/month',
                'action': 'Optimize HVAC schedule',
                'impact': 'High'
            },
            {
                'icon': '🔋',
                'title': 'Renewable Energy Recommendation',
                'description': 'Your facility has 85% solar potential. Installing 50kW panels could offset 30% of emissions',
                'action': 'Request solar assessment',
                'impact': 'High'
            },
            {
                'icon': '💧',
                'title': 'Water Conservation Alert',
                'description': 'Water usage up 8% this week. Check for leaks in Zone 3',
                'action': 'Schedule maintenance',
                'impact': 'Medium'
            },
            {
                'icon': '🚗',
                'title': 'Fleet Optimization',
                'description': 'Employee commute represents 22% of Scope 3. Consider shuttle service or remote work',
                'action': 'Review commute policy',
                'impact': 'Medium'
            }
        ]
        
        for insight in insights:
            impact_color = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}
            
            with st.container():
                st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; 
                            border-left: 4px solid {impact_color[insight['impact']]}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                    <h4>{insight['icon']} {insight['title']}</h4>
                    <p style='color: #666; margin: 0.5rem 0;'>{insight['description']}</p>
                    <div style='margin-top: 1rem;'>
                        <span style='background: {impact_color[insight['impact']]}; color: white; 
                                     padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem;'>
                            {insight['impact']} Impact
                        </span>
                        <span style='margin-left: 1rem; color: #667eea; font-weight: 500;'>
                            → {insight['action']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Benchmark Comparison
        st.markdown("### 📊 Industry Benchmarking")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            benchmark_data = pd.DataFrame({
                'Metric': ['Energy Intensity', 'Carbon Intensity', 'Water Usage', 'Waste Diversion'],
                'Your Facility': [85, 72, 68, 55],
                'Industry Average': [65, 60, 70, 50],
                'Top Quartile': [90, 85, 85, 75]
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Your Facility',
                x=benchmark_data['Metric'],
                y=benchmark_data['Your Facility'],
                marker_color='#667eea'
            ))
            fig.add_trace(go.Bar(
                name='Industry Average',
                x=benchmark_data['Metric'],
                y=benchmark_data['Industry Average'],
                marker_color='#94a3b8'
            ))
            fig.add_trace(go.Bar(
                name='Top Quartile',
                x=benchmark_data['Metric'],
                y=benchmark_data['Top Quartile'],
                marker_color='#10b981'
            ))
            
            fig.update_layout(
                barmode='group',
                height=350,
                title='Performance vs. Industry',
                yaxis_title='Score (0-100)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            st.markdown("#### 🏆 Your Rankings")
            
            rankings = [
                {'metric': 'Energy Efficiency', 'rank': '15th percentile', 'trend': 'up'},
                {'metric': 'Carbon Reduction', 'rank': '22nd percentile', 'trend': 'up'},
                {'metric': 'Water Management', 'rank': '48th percentile', 'trend': 'down'},
                {'metric': 'Waste Management', 'rank': '38th percentile', 'trend': 'up'}
            ]
            
            for r in rankings:
                trend_emoji = '📈' if r['trend'] == 'up' else '📉'
                st.markdown(f"""
                <div style='padding: 0.75rem; background: #f8fafc; border-radius: 6px; margin-bottom: 0.5rem;'>
                    <strong>{r['metric']}</strong><br>
                    <span style='color: #667eea; font-size: 1.25rem;'>{r['rank']}</span> {trend_emoji}
                </div>
                """, unsafe_allow_html=True)
        
        # Cost Analysis
        st.markdown("### 💰 Cost & ROI Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Energy Cost", "$2,450/mo", "-8%")
        col2.metric("Carbon Tax Liability", "$1,200/mo", "+12%")
        col3.metric("Potential Savings", "$850/mo", "From recommendations")
        col4.metric("ROI on Initiatives", "18 months", "Average payback")
        
    except Exception as e:
        st.error(f"Error loading analytics: {e}")
        st.info("💡 Using demo data for analytics visualization")

def esg_reporting_page():
    """ESG reporting and compliance"""
    user_id = st.session_state['user_id']
    
    st.markdown("<h1 class='main-header'>ESG Reporting & Compliance</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 2rem;'>Comprehensive ESG performance tracking and regulatory compliance management</p>", unsafe_allow_html=True)
    
    try:
        # Get ESG data
        esg_resp = requests.get(f"{BACKEND}/esg/report/{user_id}", timeout=5)
        
        # ESG Score Overview
        st.markdown("### 🎯 ESG Performance Score")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
                <div class='metric-value'>72</div>
                <div class='metric-label'>Overall ESG Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #10b981 0%, #059669 100%);'>
                <div class='metric-value'>78</div>
                <div class='metric-label'>Environmental (E)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);'>
                <div class='metric-value'>68</div>
                <div class='metric-label'>Social (S)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);'>
                <div class='metric-value'>70</div>
                <div class='metric-label'>Governance (G)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ESG Breakdown
        st.markdown("### 📊 Score Breakdown by Category")
        
        esg_categories = pd.DataFrame({
            'Category': [
                'Carbon Emissions', 'Energy Use', 'Water Management', 'Waste & Recycling',
                'Employee Safety', 'Diversity & Inclusion', 'Community Engagement',
                'Board Composition', 'Ethics & Compliance', 'Risk Management'
            ],
            'Score': [82, 75, 68, 71, 85, 62, 58, 72, 78, 65],
            'Type': ['E', 'E', 'E', 'E', 'S', 'S', 'S', 'G', 'G', 'G']
        })
        
        fig = px.bar(
            esg_categories,
            x='Score',
            y='Category',
            color='Type',
            orientation='h',
            title='ESG Category Scores (0-100)',
            color_discrete_map={'E': '#10b981', 'S': '#3b82f6', 'G': '#f59e0b'}
        )
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Reporting Frameworks
        st.markdown("### 📋 Reporting Frameworks & Compliance")
        
        frameworks = [
            {
                'name': 'GRI Standards',
                'status': 'Compliant',
                'completeness': 85,
                'last_updated': '2025-11-15',
                'color': '#10b981'
            },
            {
                'name': 'CDP Climate',
                'status': 'In Progress',
                'completeness': 62,
                'last_updated': '2025-11-20',
                'color': '#f59e0b'
            },
            {
                'name': 'TCFD',
                'status': 'Partial',
                'completeness': 48,
                'last_updated': '2025-10-30',
                'color': '#f59e0b'
            },
            {
                'name': 'SASB',
                'status': 'Compliant',
                'completeness': 92,
                'last_updated': '2025-11-25',
                'color': '#10b981'
            },
            {
                'name': 'EU CSRD',
                'status': 'Not Started',
                'completeness': 15,
                'last_updated': '2025-09-01',
                'color': '#ef4444'
            }
        ]
        
        for fw in frameworks:
            with st.container():
                col_a, col_b, col_c = st.columns([2, 3, 1])
                
                with col_a:
                    st.markdown(f"**{fw['name']}**")
                    st.caption(f"Updated: {fw['last_updated']}")
                
                with col_b:
                    st.progress(fw['completeness']/100, text=f"{fw['completeness']}% Complete")
                
                with col_c:
                    st.markdown(f"<span style='background: {fw['color']}; color: white; padding: 0.25rem 0.75rem; "
                               f"border-radius: 12px; font-size: 0.875rem;'>{fw['status']}</span>", 
                               unsafe_allow_html=True)
                
                st.markdown("---")
        
        # Key Metrics & KPIs
        st.markdown("### 📈 Key Environmental Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Carbon & Energy")
            metrics_df = pd.DataFrame({
                'Metric': ['Total GHG Emissions', 'Scope 1', 'Scope 2', 'Scope 3', 'Energy Consumption', 'Renewable %'],
                'Value': ['15,420 tCO₂e', '3,200 tCO₂e', '4,800 tCO₂e', '7,420 tCO₂e', '2.4 GWh', '35%'],
                'YoY Change': ['-12%', '-8%', '-15%', '-10%', '-6%', '+18%']
            })
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Resource Management")
            resources_df = pd.DataFrame({
                'Metric': ['Water Consumption', 'Waste Generated', 'Waste Recycled', 'Hazardous Waste', 'Land Use', 'Biodiversity Impact'],
                'Value': ['45,200 m³', '850 tonnes', '485 tonnes', '12 tonnes', '2.4 hectares', 'Low'],
                'YoY Change': ['-5%', '-9%', '+22%', '-15%', 'No change', 'Improved']
            })
            st.dataframe(resources_df, use_container_width=True, hide_index=True)
        
        # Report Generation
        st.markdown("### 📄 Generate Reports")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📊 Generate Annual Report", use_container_width=True):
                st.success("✅ Annual ESG Report generated! Download ready.")
                st.download_button(
                    label="Download PDF",
                    data="Sample ESG Report Content",
                    file_name="ESG_Annual_Report_2025.pdf",
                    mime="application/pdf"
                )
        
        with col_b:
            if st.button("📋 Export CDP Response", use_container_width=True):
                st.success("✅ CDP Climate questionnaire exported!")
                st.download_button(
                    label="Download Excel",
                    data="CDP Response Data",
                    file_name="CDP_Climate_2025.xlsx",
                    mime="application/vnd.ms-excel"
                )
        
        with col_c:
            if st.button("🎯 TCFD Report", use_container_width=True):
                st.success("✅ TCFD disclosure report ready!")
                st.download_button(
                    label="Download PDF",
                    data="TCFD Report Content",
                    file_name="TCFD_Disclosure_2025.pdf",
                    mime="application/pdf"
                )
        
        # Recommendations
        st.markdown("### 💡 Improvement Recommendations")
        
        recommendations = [
            {
                'area': 'Environmental',
                'priority': 'High',
                'recommendation': 'Increase renewable energy to 50% by 2026 to improve CDP score',
                'impact': '12-point ESG score improvement'
            },
            {
                'area': 'Social',
                'priority': 'Medium',
                'recommendation': 'Enhance diversity reporting with intersectional data',
                'impact': '8-point Social score improvement'
            },
            {
                'area': 'Governance',
                'priority': 'High',
                'recommendation': 'Publish climate risk assessment aligned with TCFD',
                'impact': 'Achieve TCFD compliance'
            },
            {
                'area': 'Environmental',
                'priority': 'Low',
                'recommendation': 'Implement biodiversity impact assessment',
                'impact': 'GRI compliance enhancement'
            }
        ]
        
        for rec in recommendations:
            priority_colors = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}
            
            with st.expander(f"{'🔴' if rec['priority']=='High' else '🟡' if rec['priority']=='Medium' else '🟢'} "
                           f"{rec['area']}: {rec['recommendation'][:50]}..."):
                st.write(f"**Full Recommendation:** {rec['recommendation']}")
                st.write(f"**Expected Impact:** {rec['impact']}")
                st.markdown(f"<span style='background: {priority_colors[rec['priority']]}; color: white; "
                           f"padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem;'>"
                           f"{rec['priority']} Priority</span>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading ESG data: {e}")
        st.info("💡 Displaying sample ESG reporting data")

# Main navigation logic
if not st.session_state['user_id']:
    login_page()
else:
    if nav == "Overview":
        overview_page()
    elif nav == "Carbon Footprint":
        carbon_accounting_page()
    elif nav == "Supply Chain":
        supply_chain_page()
    elif nav == "Climate Targets":
        targets_progress_page()
    elif nav == "Analytics":
        analytics_insights_page()
    elif nav == "ESG Reports":
        esg_reporting_page()
    elif nav == "Settings":
        st.markdown("<h1 class='main-header'>Platform Settings</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6b7280; margin-bottom: 2rem;'>Configure your account preferences and platform settings</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #111827; margin-bottom: 1rem;'>Account Settings</h3>
            <p style='color: #6b7280; font-size: 0.875rem;'>User profile, notifications, and security settings will be available in the next update.</p>
        </div>
        """, unsafe_allow_html=True)
