from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import timedelta
from flask_limiter.errors import RateLimitExceeded

from extensions import db, jwt, cors, limiter
from routes.auth_routes import auth_bp
from routes.quiz_routes import quiz_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# -----------------------------
# CONFIGURATION
# -----------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///neuroquiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "this_is_a_super_secure_jwt_secret_key_for_my_project_12345"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# -----------------------------
# INITIALIZE EXTENSIONS
# -----------------------------

db.init_app(app)
jwt.init_app(app)
cors.init_app(app)
limiter.init_app(app)

# -----------------------------
# REGISTER BLUEPRINTS
# -----------------------------

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(quiz_bp, url_prefix="/quiz")

# -----------------------------
# RATE LIMIT ERROR HANDLER
# -----------------------------

@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    return jsonify({"error": "Too many requests"}), 429

# -----------------------------
# CREATE DATABASE TABLES
# -----------------------------

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Backend is running"

# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)