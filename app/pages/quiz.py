import streamlit as st
import random

st.set_page_config(page_title="SmartQuizzer - Live Quiz", layout="wide")

# ==========================================
# --- SECURITY & STATE INITIALIZATION ---
# ==========================================
if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

if "quiz_data" not in st.session_state or not st.session_state.quiz_data:
    # st.warning("No quiz data found! Please generate a quiz first.")
    # if st.button("Go to Dashboard"):
    st.switch_page("pages/home.py")
    st.stop()

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "score" not in st.session_state:
    st.session_state.score = 0

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
        user_answer = st.session_state.get(f"answer_{i}")
        correct_answer = quiz_data[i].get("answer")
        if user_answer == correct_answer:
            score += 1
    
    st.session_state.score = score
    st.session_state.quiz_submitted = True

def reset_quiz_state():
    """Cleans up memory to return to the dashboard."""
    for key in list(st.session_state.keys()):
        if key.startswith("options_") or key.startswith("answer_"):
            del st.session_state[key]
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
        
        # Determine if answered
        is_answered = st.session_state.get(f"answer_{i}") is not None
        
        # Build button label
        btn_label = f"{i + 1}" if is_answered else f"{i + 1}"
            
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
    # FINAL SCORE & REVIEW SCREEN
    # ------------------------------------------
    st.balloons()
    st.header("Quiz Completed!")
    
    final_score = st.session_state.score
    accuracy = (final_score / total_questions) * 100
    
    col1, col2 = st.columns(2)
    col1.metric("Final Score", f"{final_score} / {total_questions}")
    col2.metric("Accuracy", f"{accuracy:.1f}%")
    
    st.divider()
    st.subheader("📝 Review Your Answers")
    
    for i, q in enumerate(quiz_data):
        user_ans = st.session_state.get(f"answer_{i}", "No Answer")
        correct_ans = q['answer']
        
        with st.expander(f"Question {i + 1}: {q['question']}"):
            if user_ans == correct_ans:
                st.success(f"**Your Answer:** {user_ans} (Correct!)")
            else:
                st.error(f"**Your Answer:** {user_ans}")
                st.info(f"**Correct Answer:** {correct_ans}")
    
    st.divider()
    # st.button("Return to Dashboard", type="primary", on_click=reset_quiz_state)
    if st.button("Go to Dashboard", type="primary", on_click=reset_quiz_state):
        st.switch_page("pages/home.py")
    st.stop()
else:
    # ------------------------------------------
    # ACTIVE QUESTION SCREEN
    # ------------------------------------------
    question_data = quiz_data[current_idx]
    
    # Display Question Tags
    st.caption(f"**Topic:** {question_data.get('topic', 'General')} | **Difficulty:** {question_data.get('difficulty', 'Unknown')} | **Type:** {question_data.get('type', 'Unknown')}")
    
    # The Question
    st.subheader(f"Q{current_idx + 1}. {question_data['question']}")
    
    # Shuffle options safely
    session_options_key = f"options_{current_idx}"
    if session_options_key not in st.session_state:
        options = question_data['distractors'] + [question_data['answer']]
        random.shuffle(options)
        st.session_state[session_options_key] = options
    
    options = st.session_state[session_options_key]
    
    # Show the radio button, tying it directly to session state
    st.radio(
        "Select your answer:", 
        options, 
        key=f"answer_{current_idx}", 
        index=None if st.session_state.get(f"answer_{current_idx}") is None else options.index(st.session_state.get(f"answer_{current_idx}"))
    )
    
    st.divider()
    
    # Previous / Next Navigation Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current_idx > 0:
            st.button("⬅️ Previous", on_click=jump_to_question, args=(current_idx - 1,), use_container_width=True)
    with col3:
        if current_idx < total_questions - 1:
            st.button("Next ➡️", on_click=jump_to_question, args=(current_idx + 1,), type="primary", use_container_width=True)
        else:
            st.button("✅ Submit Quiz", type="primary", on_click=submit_quiz, use_container_width=True)