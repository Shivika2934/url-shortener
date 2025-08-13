import os
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    click_count = db.Column(db.Integer, default=0)

# Generate short code
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

# Base URL (dynamic)
BASE_URL = os.environ.get('BASE_URL', None)  # Set this in Render environment variables

# ----------------- WEB ROUTES -----------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['url']
        if not long_url.startswith(('http://', 'https://')):
            long_url = 'http://' + long_url
        code = generate_short_code()
        new_url = URL(original_url=long_url, short_code=code)
        db.session.add(new_url)
        db.session.commit()
        # Use dynamic BASE_URL if available
        full_url = (BASE_URL.rstrip('/') + '/' + code) if BASE_URL else request.url_root.rstrip('/') + '/' + code
        return render_template('result.html', short_url=full_url)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.click_count += 1
        db.session.commit()
        return redirect(url.original_url)
    return "❌ URL not found!", 404

# ----------------- API ROUTES -----------------
@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400
    long_url = data['url']
    if not long_url.startswith(('http://', 'https://')):
        long_url = 'http://' + long_url
    code = generate_short_code()
    new_url = URL(original_url=long_url, short_code=code)
    db.session.add(new_url)
    db.session.commit()
    full_url = (BASE_URL.rstrip('/') + '/' + code) if BASE_URL else request.url_root.rstrip('/') + '/' + code
    return jsonify({
        "original_url": long_url,
        "short_url": full_url
    })

@app.route('/api/<short_code>', methods=['GET'])
def api_get_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return jsonify({
            "original_url": url.original_url,
            "short_code": url.short_code,
            "click_count": url.click_count
        })
    return jsonify({"error": "Short code not found"}), 404

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))  # Render sets this automatically
    app.run(host='0.0.0.0', port=port)
