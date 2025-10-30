import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-default-secret-key')
# Example: use PostgreSQL on Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///animecosplay.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Routes
@app.route('/')
def home():
    # If you have an HTML template file, use render_template; else return direct HTML
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Anime Cosplay</title>
      <style>
        body { background-color: #f8f8f8; font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #ff4081; }
      </style>
    </head>
    <body>
      <h1>Welcome to Anime Cosplay!</h1>
      <p>Your anime costume store.</p>
      <script>console.log("Anime Cosplay loaded!");</script>
    </body>
    </html>
    """

# Add more routes e.g. register, login, CRUD etc.
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'Missing username or password'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'User already exists'}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        from flask_jwt_extended import create_access_token
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'msg': 'Bad username or password'}), 401

if __name__ == '__main__':
    # On Render it will use gunicorn; locally we run debug
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
    