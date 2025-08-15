from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import secrets
import json
from datetime import datetime, timedelta
import subprocess
import tempfile
import base64
from PIL import Image
import io
import requests

# Face animation removed for cleaner, modern design
FACE_ANIMATION_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ascii_converter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Face animator removed for cleaner design
face_animator = None

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    tokens = db.Column(db.Integer, default=100)  # Starting tokens
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    def add_tokens(self, amount):
        self.tokens += amount
        db.session.commit()
    
    def use_tokens(self, amount):
        if self.tokens >= amount:
            self.tokens -= amount
            db.session.commit()
            return True
        return False

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    output_filename = db.Column(db.String(255), nullable=False)
    conversion_type = db.Column(db.String(50), nullable=False)  # 'gif' or 'ascii'
    settings = db.Column(db.Text)  # JSON string of conversion settings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tokens_used = db.Column(db.Integer, default=1)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html', face_animation_available=FACE_ANIMATION_AVAILABLE)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_conversions = Conversion.query.filter_by(user_id=current_user.id).order_by(Conversion.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', conversions=user_conversions)

@app.route('/converter')
@login_required
def converter():
    return render_template('converter.html', face_animation_available=FACE_ANIMATION_AVAILABLE)

@app.route('/api/convert', methods=['POST'])
@login_required
def convert_gif():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.gif'):
        return jsonify({'error': 'Only GIF files are supported'}), 400
    
    # Check if user has enough tokens
    tokens_needed = 1
    
    if current_user.tokens < tokens_needed:
        return jsonify({'error': f'Insufficient tokens. You need at least {tokens_needed} tokens to convert.'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Get conversion settings
        settings = {
            'scale': request.form.get('scale', '0.5'),
            'speed': request.form.get('speed', '1.0'),
            'inverse': request.form.get('inverse') == 'true',
            'color': request.form.get('color') == 'true',
            'size': request.form.get('size', '12'),
            'output_type': request.form.get('output_type', 'gif')
        }
        
        # Generate output filename
        output_filename = f"output_{timestamp}.{'gif' if settings['output_type'] == 'gif' else 'txt'}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Run conversion using the Python script
        cmd = [
            'python', 'new.py', filepath,
            '--scale', settings['scale'],
            '--speed', settings['speed'],
            '--size', settings['size']
        ]
        
        if settings['inverse']:
            cmd.append('--inverse')
        if settings['color']:
            cmd.append('--color')
        if settings['output_type'] == 'ascii':
            cmd.append('--ascii')
        
        cmd.extend(['--out', output_path])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return jsonify({'error': f'Conversion failed: {result.stderr}'}), 500
        
        # Deduct tokens and save conversion record
        current_user.use_tokens(tokens_needed)
        conversion = Conversion(
            user_id=current_user.id,
            original_filename=filename,
            output_filename=output_filename,
            conversion_type=settings['output_type'],
            settings=json.dumps(settings),
            tokens_used=tokens_needed
        )
        db.session.add(conversion)
        db.session.commit()
        
        # Return success with file info
        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'download_url': f'/download/{output_filename}',
            'tokens_remaining': current_user.tokens
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-gifs', methods=['POST'])
@login_required
def search_gifs():
    """Search for GIFs using GIPHY API"""
    try:
        query = request.json.get('query', '')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # GIPHY API endpoint (you'll need to get a free API key from https://developers.giphy.com/)
        # For demo purposes, we'll use a mock response
        # In production, replace with actual GIPHY API call
        
        # Mock GIF search results
        mock_gifs = [
            {
                'id': '1',
                'title': f'{query} GIF 1',
                'url': 'https://media.giphy.com/media/example1/giphy.gif',
                'preview_url': 'https://media.giphy.com/media/example1/giphy.gif',
                'size': '2.1 MB'
            },
            {
                'id': '2',
                'title': f'{query} GIF 2',
                'url': 'https://media.giphy.com/media/example2/giphy.gif',
                'preview_url': 'https://media.giphy.com/media/example2/giphy.gif',
                'size': '1.8 MB'
            },
            {
                'id': '3',
                'title': f'{query} GIF 3',
                'url': 'https://media.giphy.com/media/example3/giphy.gif',
                'preview_url': 'https://media.giphy.com/media/example3/giphy.gif',
                'size': '3.2 MB'
            }
        ]
        
        return jsonify({
            'success': True,
            'gifs': mock_gifs,
            'query': query
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-gif', methods=['POST'])
@login_required
def download_gif():
    """Download a GIF from search results"""
    try:
        gif_url = request.json.get('gif_url', '')
        if not gif_url:
            return jsonify({'error': 'GIF URL is required'}), 400
        
        # Download the GIF
        response = requests.get(gif_url, stream=True)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download GIF'}), 500
        
        # Save to uploads folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"downloaded_{timestamp}.gif"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'message': 'GIF downloaded successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/user/tokens')
@login_required
def get_user_tokens():
    return jsonify({'tokens': current_user.tokens})

@app.route('/api/user/profile')
@login_required
def get_user_profile():
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'name': current_user.name,
        'tokens': current_user.tokens,
        'created_at': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat()
    })

@app.route('/api/features')
def get_available_features():
    """Get available features"""
    return jsonify({
        'basic_conversion_cost': 1
    })

# Mock Gmail OAuth endpoints (in production, use proper OAuth)
@app.route('/auth/gmail')
def gmail_auth():
    # Simulate Gmail OAuth flow
    # In production, implement proper OAuth2 with Google
    return redirect(url_for('gmail_callback'))

@app.route('/auth/gmail/callback')
def gmail_callback():
    # Mock OAuth callback - in production, verify the OAuth token
    # For demo purposes, create a mock user
    mock_user = User.query.filter_by(email='demo@example.com').first()
    if not mock_user:
        mock_user = User(
            email='demo@example.com',
            name='Demo User',
            tokens=150  # Bonus tokens for Gmail users
        )
        db.session.add(mock_user)
        db.session.commit()
    
    login_user(mock_user)
    flash('Welcome! You received 50 bonus tokens for using Gmail!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 