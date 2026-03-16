import os
import json
import google.generativeai as genai

# ==========================================
# --- GEMINI CONFIGURATION ---
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")

# Configure the SDK
genai.configure(api_key=GEMINI_API_KEY)

# We use gemini-2.5-flash because it is incredibly fast and part of the free tier
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# --- CORE GENERATOR FUNCTION ---
# ==========================================
def generate_questions(text_chunks, difficulty, question_types, num_questions=3):
    """
    Generates questions using Google's Gemini API, natively forcing valid JSON output.
    """
    # Combine chunks for context (Gemini can handle a lot of text!)
    context = "\n".join(text_chunks[:5]) 
    
    # --- PROMPT ENGINEERING ---
    # --- PROMPT ENGINEERING ---
    # --- PROMPT ENGINEERING ---
    prompt = f"""
    You are an expert AI tutor. Based on the provided text, generate exactly {num_questions} quiz questions.
    The difficulty level must be: {difficulty}.
    The question types must be chosen from: {question_types}.
    
    Context Text:
    {context}
    
    You MUST output a valid JSON array of objects. Do not include markdown formatting like ```json.
    Each object in the array must use this exact structure:
    {{
        "question": "The actual question text",
        "type": "The specific type of this question",
        "answer": "The correct answer",
        "distractors": ["Wrong option 1", "Wrong option 2", "Wrong option 3"],
        "difficulty": "{difficulty}",
        "topic": "A brief 2-3 word topic summary"
    }}
    
    CRITICAL RULES FOR OPTIONS:
    1. If the question type is "MCQ", provide exactly 3 plausible but incorrect distractors.
    2. If the question type is "True/False", the "answer" MUST be exactly "True" or "False". The "distractors" array MUST contain exactly one item: the opposite value (e.g., ["False"]). Do not invent extra sentences.
    3. If the question type is "Fill in the Blank", the "question" text MUST contain a blank space represented by "_____". The "answer" is the correct missing word/phrase, and the "distractors" MUST contain exactly 3 incorrect words/phrases that could logically fit in that blank.
    """
    try:
        # Call Gemini and FORCE it to reply strictly in JSON format
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.8
            )
        )
        
        # Because we forced JSON, we can just load it directly into a Python list/dictionary!
        quiz_data = json.loads(response.text)
        return quiz_data
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return [{"error": f"Failed to generate questions: {str(e)}"}]