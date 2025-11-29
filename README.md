# Sustainability-as-a-Service (AI-Powered MVP)

A plug-and-play modular platform for sustainability analytics, powered by IoT simulation and AI.

Quick Start — Run Locally
1. Prereqs
   - Python 3.9+
   - (Recommended) Virtualenv:
     - Linux/macOS: python -m venv venv && source venv/bin/activate
     - Windows: python -m venv venv && venv\Scripts\activate

2. Backend
   cd backend
   pip install -r requirements.txt
   python app.py
   Backend runs at http://localhost:5000

3. Dashboard
   Open a new terminal:
   cd dashboard
   pip install -r requirements.txt
   streamlit run dashboard.py
   Dashboard runs at http://localhost:8501

Demo users:
- user1 / password1 (basic)
- user2 / password2 (pro)

ESG demo:
- Go to ESG Compliance tab, upload sample_data/sample_esg_report.csv

Docker & Cloud:
See docs/cloud_deployment.md for Docker and cloud deployment steps.

Project layout:
- backend/  — Flask API (users, billing, energy, analytics, esg)
- dashboard/ — Streamlit frontend
- docs/ — cloud deployment notes
- sample_data/ — sample ESG csv

License: MIT