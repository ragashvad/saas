# backend/esg_ai.py
from flask import Blueprint, request, jsonify
import pandas as pd
from analytics import extract_esg_kpis

esg_bp = Blueprint('esg_bp', __name__)

@esg_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    f = request.files['file']
    try:
        content = f.read().decode('utf-8', errors='ignore')
    except Exception:
        return jsonify({'error': 'Unable to read file'}), 400
    if f.filename.lower().endswith('.csv'):
        try:
            df = pd.read_csv(pd.compat.StringIO(content))
            text = ' '.join(df.astype(str).values.flatten())
        except Exception:
            text = content
    else:
        text = content
    kpis = extract_esg_kpis(text)
    total_found = any(v > 0 for v in kpis.values())
    summary = f"Extracted ESG KPIs: {kpis}" if total_found else "No ESG KPIs detected."
    return jsonify({
        "kpis": kpis,
        "summary": summary
    })