import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime ,timezone

# --- Database Connection ---
# For local testing, you can use a local MongoDB URI. 
# For production, use Streamlit secrets: st.secrets["MONGO_URI"]
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sarveshmahalingam2004_db_user:ixOHvjgz8psOWPTp@smartquizzer-db.c2yk85r.mongodb.net/?appName=smartquizzer-db")
client = MongoClient(MONGO_URI)
db = client["SmartQuizzerDB"]

# Collections based on your schema diagram
users_collection = db["Users"]
content_collection = db["Content"]
questions_collection = db["Questions"]
quizzes_collection = db["Quizzes"]

# --- User Operations ---

def create_user(email, password, name, phone, dob):
    """Creates a new user with securely hashed passwords and default preferences."""
    
    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return False, "User with this email already exists."

    # Hash the password as required by your schema
    hashed_password = generate_password_hash(password)

    user_document = {
        "email": email,
        "password": hashed_password,
        "name": name,
        "phone": phone,
        "dob": dob,
        "preferences": {
            "difficulty": "Medium",
            "subjects": [],
            "question_types": ["MCQ", "Short Answer"]
        },
        "created_at": datetime.utcnow()
    }
    
    users_collection.insert_one(user_document)
    return True, "User registered successfully."

def authenticate_user(email, password):
    """Verifies user credentials for login."""
    user = users_collection.find_one({"email": email})
    
    if user and check_password_hash(user["password"], password):
        # Don't return the password hash to the frontend
        user.pop("password") 
        return True, user
    
    return False, "Invalid email or password."

def update_user_profile(email, updated_data):
    """Updates user details in the database."""
    result = users_collection.update_one(
        {"email": email},
        {"$set": updated_data}
    )
    return result.modified_count > 0

def save_quiz_result(email, score, total_questions, improvement_areas):
    """Saves the final quiz result to the database."""
    try:
        quiz_document = {
            "user_email": email,
            "score": score,
            "total_questions": total_questions,
            "accuracy": (score / total_questions) * 100 if total_questions > 0 else 0,
            "improvement_areas": improvement_areas,
            "timestamp": datetime.now(timezone.utc) # Records exactly when they took it
        }
        quizzes_collection.insert_one(quiz_document)
        return True, "Success"
    except Exception as e:
        print(f"Error saving quiz: {e}")
        return False, str(e)

def get_user_quiz_history(email):
    """Fetches a user's past quizzes, sorted oldest to newest for the chart."""
    # sort("timestamp", 1) ensures chronological order (oldest left, newest right)
    cursor = quizzes_collection.find({"user_email": email}).sort("timestamp", 1)
    return list(cursor)