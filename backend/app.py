# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from billing import billing_bp
from users import users_bp
from energy import energy_bp
from esg_ai import esg_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(billing_bp, url_prefix='/billing')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(energy_bp, url_prefix='/energy')
app.register_blueprint(esg_bp, url_prefix='/esg')

@app.route('/')
def index():
    return jsonify({'status': 'OK', 'message': 'Sustainability SaaS backend running'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)