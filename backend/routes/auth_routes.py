from flask import Blueprint, request, jsonify
from extensions import limiter, db
from models import User
from flask_jwt_extended import create_access_token
import bcrypt
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ---------------- #

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    )

    # create user
    new_user = User(
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ---------------- LOGIN ---------------- #

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # check password
    if bcrypt.checkpw(password.encode("utf-8"), user.password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# ---------------- FORGOT PASSWORD ---------------- #

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    token = secrets.token_hex(16)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)

    db.session.commit()

    return jsonify({
        "message": "Reset link generated",
        "token": token
    })


# ---------------- RESET PASSWORD ---------------- #

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    token = data.get("token")
    new_password = data.get("password")

    user = User.query.filter_by(reset_token=token).first()

    if not user:
        return jsonify({"message": "Invalid token"}), 400

    if user.reset_token_expiry < datetime.utcnow():
        return jsonify({"message": "Token expired"}), 400

    # hash new password with bcrypt
    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"), bcrypt.gensalt()
    )

    user.password = hashed_password
    user.reset_token = None
    user.reset_token_expiry = None

    db.session.commit()

    return jsonify({"message": "Password updated successfully"})