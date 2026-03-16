import streamlit as st
import random
import pandas as pd
import plotly.express as px
from database import db_operations

st.set_page_config(page_title="SmartQuizzer - Live Quiz", layout="wide")

# ==========================================
# --- SECURITY & STATE INITIALIZATION ---
# ==========================================
if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

if "quiz_data" not in st.session_state or not st.session_state.quiz_data:
    st.switch_page("pages/home.py")
    st.stop()

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "score" not in st.session_state:
    st.session_state.score = 0

# 🛑 THE FIX: Create a persistent dictionary for answers that Streamlit won't delete!
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

quiz_data = st.session_state.quiz_data
total_questions = len(quiz_data)
current_idx = st.session_state.current_question_index

# ==========================================
# --- HELPER FUNCTIONS ---
# ==========================================
def jump_to_question(idx):
    """Changes the active question index."""
    st.session_state.current_question_index = idx

def submit_quiz():
    """Grades the entire quiz at once."""
    score = 0
    for i in range(total_questions):
        # 🛑 Check our persistent dictionary instead of widget keys
        user_answer = st.session_state.user_answers.get(i)
        correct_answer = quiz_data[i].get("answer")
        if user_answer == correct_answer:
            score += 1
    
    st.session_state.score = score
    st.session_state.quiz_submitted = True

def reset_quiz_state():
    """Cleans up memory to return to the dashboard."""
    for key in list(st.session_state.keys()):
        if key.startswith("options_") or key.startswith("widget_"):
            del st.session_state[key]
    st.session_state.user_answers = {} # Clear persistent answers
    st.session_state.quiz_data = None
    st.session_state.quiz_submitted = False
    st.switch_page("pages/home.py")

# ==========================================
# --- SIDEBAR NAVIGATION ---
# ==========================================
with st.sidebar:
    st.header("📋 Quiz Navigator")
    
    # Create a nice grid for the question buttons
    cols = st.columns(4)
    for i in range(total_questions):
        col_idx = i % 4
        
        # 🛑 Update check to look at our persistent dictionary
        is_answered = i in st.session_state.user_answers
        
        # Build button label (Add a checkmark if answered!)
        btn_label = f"✅ {i + 1}" if is_answered else f"{i + 1}"
            
        # Highlight the current question with the primary color
        btn_type = "primary" if i == current_idx else "secondary"
        
        with cols[col_idx]:
            st.button(
                btn_label, 
                key=f"nav_btn_{i}", 
                on_click=jump_to_question, 
                args=(i,), 
                type=btn_type, 
                use_container_width=True, 
                disabled=st.session_state.quiz_submitted
            )
    
    st.divider()
    if not st.session_state.quiz_submitted:
        st.button("✅ Submit Quiz", type="primary", use_container_width=True, on_click=submit_quiz)

# ==========================================
# --- MAIN UI LOGIC ---
# ==========================================
st.title("🧠 Your Smart Quiz")

if st.session_state.quiz_submitted:
    # ------------------------------------------
    # FINAL SCORE & ANALYTICS SCREEN
    # ------------------------------------------
    st.balloons()
    st.header("Quiz Completed! 🎯")
    
    final_score = st.session_state.score
    accuracy = (final_score / total_questions) * 100
    
    improvement_areas = []
    
    for i, q in enumerate(quiz_data):
        # 🛑 Pull user answers from the persistent dictionary
        user_ans = st.session_state.user_answers.get(i, "No Answer")
        if user_ans != q['answer']:
            category = q.get('topic', q.get('type', 'General Concepts'))
            improvement_areas.append(category)

    if "results_saved" not in st.session_state:
        user_email = st.session_state.user_data.get("email")
        
        # Show us the email to make sure you are actually logged in!
        st.info(f"Attempting to save results for: {user_email}")
        
        from database import db_operations
        success, error_msg = db_operations.save_quiz_result(
            email=user_email,
            score=final_score,
            total_questions=total_questions,
            improvement_areas=improvement_areas
        )
        
        if success:
            st.toast("✅ Quiz results successfully saved to MongoDB!")
            st.session_state.results_saved = True
        else:
            # 🚨 THIS WILL REVEAL THE BUG 🚨
            st.error(f"DATABASE ERROR: {error_msg}")
    col1, col2 = st.columns([1, 1.5]) 
    
    with col1:
        st.subheader("📊 Overview")
        st.metric("Final Score", f"{final_score} / {total_questions}")
        st.metric("Accuracy", f"{accuracy:.1f}%")
        
    with col2:
        st.subheader("🔍 Areas for Improvement")
        if improvement_areas:
            df_wrong = pd.DataFrame(improvement_areas, columns=['Topic'])
            mistake_counts = df_wrong['Topic'].value_counts().reset_index()
            mistake_counts.columns = ['Topic', 'Mistakes']
            
            fig = px.pie(
                mistake_counts, 
                values='Mistakes', 
                names='Topic', 
                hole=0.4, 
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10), 
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
        elif final_score == total_questions:
            st.success("Perfect Score! 🏆\n\nYou have mastered all topics in this module.")
    
    st.divider()
    
    # ------------------------------------------
    # DETAILED ANSWER REVIEW
    # ------------------------------------------
    st.subheader("📝 Review Your Answers")
    
    for i, q in enumerate(quiz_data):
        # 🛑 Pull from persistent dictionary again
        user_ans = st.session_state.user_answers.get(i, "No Answer")
        correct_ans = q['answer']
        
        with st.expander(f"Question {i + 1}: {q['question']}"):
            if user_ans == correct_ans:
                st.success(f"**Your Answer:** {user_ans} (Correct!)")
            else:
                st.error(f"**Your Answer:** {user_ans}")
                st.info(f"**Correct Answer:** {correct_ans}")
    
    st.divider()
    
    if st.button("Go to Dashboard", type="primary", on_click=reset_quiz_state):
        st.switch_page("pages/home.py")
    st.stop()
else:
    # ------------------------------------------
    # ACTIVE QUESTION SCREEN
    # ------------------------------------------
    question_data = quiz_data[current_idx]
    
    st.caption(f"**Topic:** {question_data.get('topic', 'General')} | **Difficulty:** {question_data.get('difficulty', 'Unknown')} | **Type:** {question_data.get('type', 'Unknown')}")
    st.subheader(f"Q{current_idx + 1}. {question_data['question']}")
    
    # Shuffle options safely
    session_options_key = f"options_{current_idx}"
    if session_options_key not in st.session_state:
        options = question_data['distractors'] + [question_data['answer']]
        random.shuffle(options)
        st.session_state[session_options_key] = options
    
    options = st.session_state[session_options_key]
    
    # 🛑 THE FIX: Safely find the index of the previously selected answer (if any)
    saved_answer = st.session_state.user_answers.get(current_idx)
    start_index = options.index(saved_answer) if saved_answer in options else None
    
    # Render the radio button
    selected_option = st.radio(
        "Select your answer:", 
        options, 
        index=start_index,
        key=f"widget_{current_idx}" # Streamlit can delete this later, we don't care anymore!
    )
    

    if selected_option:
        st.session_state.user_answers[current_idx] = selected_option
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current_idx > 0:
            st.button("⬅️ Previous", on_click=jump_to_question, args=(current_idx - 1,), use_container_width=True)
    with col3:
        if current_idx < total_questions - 1:
            st.button("Next ➡️", on_click=jump_to_question, args=(current_idx + 1,), type="primary", use_container_width=True)
        else:
            st.button("✅ Submit Quiz", type="primary", on_click=submit_quiz, use_container_width=True)

def reset_quiz_state():
    """Update your reset function to clear the save lock!"""
    for key in list(st.session_state.keys()):
        if key.startswith("options_") or key.startswith("widget_"):
            del st.session_state[key]
    st.session_state.user_answers = {} 
    st.session_state.quiz_data = None
    st.session_state.quiz_submitted = False
    
    # Unlock the save feature for the NEXT quiz
    if "results_saved" in st.session_state:
        del st.session_state["results_saved"]
        
    st.switch_page("pages/home.py")