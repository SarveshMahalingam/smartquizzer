from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, QuizResult, QuizAttempt, Achievement
import requests
import random

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


# --------------------------------------------------
# Generate Quiz
# --------------------------------------------------
@quiz_bp.route("/generate", methods=["POST"])
def generate_quiz():

    data = request.json

    category = data.get("category")
    amount = data.get("amount")
    difficulty = data.get("difficulty")

    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type=multiple"

    response = requests.get(url).json()

    questions = []

    for q in response["results"]:

        options = q["incorrect_answers"] + [q["correct_answer"]]
        random.shuffle(options)

        questions.append({
            "question": q["question"],
            "options": options,
            "answer": q["correct_answer"]
        })

    return jsonify({"questions": questions})


# --------------------------------------------------
# Submit Quiz
# --------------------------------------------------
@quiz_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_quiz():

    data = request.get_json()

    selected = data.get("selected_answer")
    correct = data.get("correct_answer")

    score = 1 if selected == correct else 0

    xp_earned = score * 10

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    # Update XP
    user.xp += xp_earned

    # Level System
    if user.xp >= 700:
        user.level = "Nero Champion"
    elif user.xp >= 400:
        user.level = "Quiz Master"
    elif user.xp >= 200:
        user.level = "Knowledge Seeker"
    elif user.xp >= 100:
        user.level = "Explorer"
    else:
        user.level = "Beginner"

    # Save Attempt
    attempt = QuizAttempt(
        user_id=user_id,
        score=score,
        total_questions=1,
        difficulty="Medium"
    )

    db.session.add(attempt)

    # --------------------------------------------------
    # Achievements System
    # --------------------------------------------------

    quiz_count = QuizAttempt.query.filter_by(user_id=user_id).count()

    if quiz_count == 1:

        achievement = Achievement(
            user_id=user_id,
            title="First Quiz",
            description="Completed your first quiz"
        )

        db.session.add(achievement)

    if quiz_count == 5:

        achievement = Achievement(
            user_id=user_id,
            title="Quiz Explorer",
            description="Completed 5 quizzes"
        )

        db.session.add(achievement)

    db.session.commit()

    return jsonify({"score": score})


# --------------------------------------------------
# Quiz History
# --------------------------------------------------
@quiz_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():

    user_id = int(get_jwt_identity())

    history = QuizAttempt.query.filter_by(user_id=user_id).all()

    results = []

    for item in history:

        results.append({
            "score": item.score,
            "difficulty": item.difficulty
        })

    return jsonify(results)


# --------------------------------------------------
# Leaderboard
# --------------------------------------------------
@quiz_bp.route("/leaderboard", methods=["GET"])
def leaderboard():

    top_users = (
        db.session.query(
            QuizAttempt.user_id,
            db.func.sum(QuizAttempt.score).label("total_score")
        )
        .group_by(QuizAttempt.user_id)
        .order_by(db.func.sum(QuizAttempt.score).desc())
        .limit(10)
        .all()
    )

    leaderboard = []

    for user in top_users:

        leaderboard.append({
            "user_id": user.user_id,
            "score": user.total_score
        })

    return jsonify(leaderboard)


# --------------------------------------------------
# User Statistics
# --------------------------------------------------
@quiz_bp.route("/stats", methods=["GET"])
@jwt_required()
def user_stats():

    user_id = int(get_jwt_identity())

    quizzes = QuizAttempt.query.filter_by(user_id=user_id).all()

    total = len(quizzes)

    if total == 0:

        return jsonify({
            "total_quizzes": 0,
            "best_score": 0,
            "average_score": 0,
            "accuracy": 0
        })

    scores = [q.score for q in quizzes]

    best = max(scores)

    average = sum(scores) / total

    accuracy = round((average / 1) * 100, 2)

    return jsonify({
        "total_quizzes": total,
        "best_score": best,
        "average_score": round(average, 2),
        "accuracy": accuracy
    })


# --------------------------------------------------
# Adaptive Difficulty
# --------------------------------------------------
@quiz_bp.route("/adaptive-difficulty", methods=["GET"])
@jwt_required()
def adaptive_difficulty():

    user_id = int(get_jwt_identity())

    quizzes = QuizAttempt.query.filter_by(user_id=user_id).all()

    if len(quizzes) == 0:
        return jsonify({"difficulty": "easy"})

    scores = [q.score for q in quizzes]

    average = sum(scores) / len(scores)

    percentage = (average / 1) * 100

    if percentage >= 80:
        difficulty = "hard"

    elif percentage >= 50:
        difficulty = "medium"

    else:
        difficulty = "easy"

    return jsonify({"difficulty": difficulty})


# --------------------------------------------------
# User Profile
# --------------------------------------------------
@quiz_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    return jsonify({
        "xp": user.xp,
        "level": user.level
    })


# --------------------------------------------------
# Achievements
# --------------------------------------------------
@quiz_bp.route("/achievements", methods=["GET"])
@jwt_required()
def get_achievements():

    user_id = int(get_jwt_identity())

    achievements = Achievement.query.filter_by(user_id=user_id).all()

    result = []

    for a in achievements:

        result.append({
            "title": a.title,
            "description": a.description
        })

    return jsonify(result)


# --------------------------------------------------
# Platform Stats
# --------------------------------------------------
@quiz_bp.route("/platform-stats", methods=["GET"])
def platform_stats():

    total_users = User.query.count()
    total_quizzes = QuizAttempt.query.count()

    avg_accuracy = 75

    return jsonify({
        "users": total_users,
        "quizzes": total_quizzes,
        "accuracy": avg_accuracy
    })