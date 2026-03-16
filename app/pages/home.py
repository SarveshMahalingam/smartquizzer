import streamlit as st
import re
import datetime
from backend import nlp_processor
import pandas as pd
import plotly.express as px
from database import db_operations

# --- Mock Data (Replace with your database logic) ---
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "name": "John Doe",
        "dob": "1990-01-01",
        "email": "john@example.com",
        "phone": "+1 555 123 4567"
    }

if 'editing' not in st.session_state:
    st.session_state.editing = False

header_col1, header_col2 = st.columns([8, 2])
with header_col1:
    st.title(f"Welcome, {st.session_state.user_data['name']}!")
with header_col2:
    # Use container width makes the button look nicer next to the title
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_data = {}
        # Redirect back to the login page (main.py)
        st.switch_page("main.py") 

 # Adds a nice horizontal line to separate the header from the content
# --- UI Layout ---
st.divider()
st.header("📈 Your Learning Analytics")

# 1. Fetch the data from MongoDB
user_email = st.session_state.user_data.get("email")
history = db_operations.get_user_quiz_history(user_email)

if history:
    # --- 1. VISIBLE BY DEFAULT: METRICS & TIMELINE ---
    df = pd.DataFrame(history)
    df['Date'] = pd.to_datetime(df['timestamp']).dt.strftime('%b %d, %H:%M')
    
    total_quizzes = len(df)
    avg_accuracy = df['accuracy'].mean()
    
    # High-level metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Quizzes Taken", total_quizzes)
    col2.metric("Average Lifetime Accuracy", f"{avg_accuracy:.1f}%")

    # The Timeline Chart (Always visible)
    st.subheader("Accuracy Timeline")
    fig_line = px.line(
        df, x='Date', y='accuracy', markers=True, 
        color_discrete_sequence=['#FF4B4B']
    )
    fig_line.update_yaxes(range=[0, 105]) 
    st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    # --- 2. DROPDOWN BUTTONS: INDIVIDUAL QUIZ STATS & PIE CHARTS ---
    st.subheader("🗓️ Individual Quiz Breakdown")
    
    # Reverse history so newest is at the top
    reversed_history = history[::-1]
    
    for i, quiz in enumerate(reversed_history):
        # Format the date nicely for the button
        dt = pd.to_datetime(quiz.get("timestamp"))
        date_str = dt.strftime('%b %d, %Y - %I:%M %p')
        
        q_score = quiz.get('score', 0)
        q_total = quiz.get('total_questions', 0)
        q_acc = quiz.get('accuracy', 0)
        q_areas = quiz.get('improvement_areas', [])
        
        # The button label
        button_label = f"📝 Quiz: {date_str} | Score: {q_score}/{q_total}"
        
        # The Dropdown!
        with st.expander(button_label):
            st.metric("Quiz Accuracy", f"{q_acc:.1f}%")
            
            # Generate a specific pie chart just for THIS quiz
            if q_areas:
                st.write("**Areas for Improvement:**")
                
                # Count the mistakes per topic for this specific quiz
                df_mistakes = pd.DataFrame(q_areas, columns=['Topic'])
                mistake_counts = df_mistakes['Topic'].value_counts().reset_index()
                mistake_counts.columns = ['Topic', 'Mistakes']
                
                # The Mini Pie Chart
                fig_pie = px.pie(
                    mistake_counts, 
                    values='Mistakes', 
                    names='Topic', 
                    hole=0.4, 
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(
                    showlegend=False, 
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=250, # Shorter height so it fits beautifully in the dropdown!
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.success("✨ Flawless victory! You got every question right on this quiz.")

else:
    st.info("No analytics yet! Generate and complete your first quiz to track your progress here.")
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.header("Profile Section")
    
    if not st.session_state.editing:
        # --- VIEW MODE ---
        st.write(f"**Name:** {st.session_state.user_data['name']}")
        st.write(f"**DOB:** {st.session_state.user_data['dob']}")
        st.write(f"**Email:** {st.session_state.user_data['email']}")
        st.write(f"**Phone:** {st.session_state.user_data['phone']}")
        
        if st.button("Edit Profile"):
            st.session_state.editing = True
            st.rerun()
            
    else:
        # --- EDIT MODE ---
        with st.form(key="edit_form"):
            st.subheader("Edit User Details")
            # Populate inputs with current data
            new_name = st.text_input("User Name:", value=st.session_state.user_data['name'])
            start_date = datetime.date(1900, 1, 1)
            end_date = datetime.date(2100, 12, 31)

            # Pass them into the date_input widget
            new_dob = st.date_input(
                "Select a date:",
                value=st.session_state.user_data['dob'],           # The default highlighted date
                min_value=start_date,    # The furthest back they can scroll
                max_value=end_date,       # The furthest forward they can scroll
                
            )
            # new_dob = st.date_input("Select Date of Birth:") # Add value parsing if needed
            new_email = st.text_input("Enter Email Address", value=st.session_state.user_data['email'])
            new_phone = st.text_input("Enter Phone Number:", value=st.session_state.user_data['phone'])
            
            submit_button = st.form_submit_button(label='Save Changes')
            cancel_button = st.form_submit_button(label='Cancel')

            if submit_button:
                # Add your validation logic here (regex, phonenumbers, etc.)
                # If valid:
                st.session_state.user_data.update({
                    "name": new_name,
                    "dob":new_dob,
                    "email": new_email,
                    "phone": new_phone
                })
                st.session_state.editing = False
                st.success("Profile Updated!")
                st.rerun()
            
            if cancel_button:
                st.session_state.editing = False
                st.rerun()

with col2:
    st.header("Generate Quiz")
    st.write("Provide learning material to generate your adaptive quiz.")

    # 1. Content Input Toggle (File vs URL)
    input_method = st.radio("Choose Input Method:", ["File Upload", "URL Input"], horizontal=True)
    
    # This flag helps us know when to enable the Start Quiz button
    content_ready = False 
    file_or_url_data = None

    if input_method == "File Upload":
        uploaded_file = st.file_uploader("Upload study materials (PDF/Text)", type=["pdf", "txt"])
        if uploaded_file:
            st.success("File received! Ready for processing.")
            content_ready = True
            file_or_url_data = uploaded_file
            
    else:
        url_input = st.text_input("Enter Article/Content URL:", placeholder="https://en.wikipedia.org/wiki/...")
        if url_input:
            # Basic check to ensure it's not empty
            st.success("URL received! Ready for processing.")
            content_ready = True
            file_or_url_data = url_input

            
    st.divider()

    # 2. Difficulty Selection
    # As per your documentation, the adaptive engine starts at Medium
    difficulty = st.selectbox(
        "Select Initial Difficulty:", 
        ["Easy", "Medium", "Hard"], 
        index=1 # Sets "Medium" as the default selection
    )
    # 3. Question Type Selection
    question_types = st.multiselect(
        "Select Question Types:",
        options=["MCQ", "Fill-in-the-blank", "True/False"],
        default=["MCQ", "True/False"]
    )

    if not question_types:
        st.warning("Please select at least one question type to proceed.")
        content_ready = False

    # 4. Start Quiz Button
    # The 'disabled' parameter prevents the user from clicking it if no file/URL is provided
    # 4. Start Quiz Button
    if st.button("Start Quiz", type="primary", use_container_width=True, disabled=not content_ready):
        
        # 1. Show a loading spinner while the AI thinks
        with st.spinner("Extracting text and generating AI questions... This may take a minute!"):
            from backend import nlp_processor
            from backend import llm_generator
            
            # 2. Extract text chunks from the file/URL
            chunks, status = nlp_processor.process_content(input_method, file_or_url_data)
            
            if chunks:
                # 3. Ask Hugging Face / local T5 to generate the quiz
                generated_quiz = llm_generator.generate_questions(
                    text_chunks=chunks,
                    difficulty=difficulty,
                    question_types=question_types,
                    num_questions=10 # Generating 3 questions to start
                )
                
                # 4. If successful, save the quiz data and jump to the next page!
                if generated_quiz and "error" not in generated_quiz[0]:
                    
                    # Save everything to session state so the quiz page can read it
                    st.session_state.quiz_data = generated_quiz
                    st.session_state.current_question_index = 0
                    st.session_state.score = 0

                    st.session_state.quiz_submitted = False 
                    
                    # 🛑 FIX 2: Wipe the persistent answers dictionary
                    st.session_state.user_answers = {}
                    
                    # --- THE CLEANUP LOOP ---
                    # Look through Streamlit's memory and delete old widgets and options
                    for key in list(st.session_state.keys()):
                        if key.startswith("options_") or key.startswith("widget_"):
                            del st.session_state[key]
                            
                    # 🛑 FIX 3: DELETE THE DATABASE LOCK!
                    if "results_saved" in st.session_state:
                        del st.session_state["results_saved"]

                    st.switch_page("pages/quiz.py")
                    
                    # --- THE FIX: WIPE OLD OPTIONS FROM MEMORY ---
                    # Look through Streamlit's memory and delete old shuffled options and answered states
                    for key in list(st.session_state.keys()):
                        if key.startswith("options_") or key.startswith("answered_"):
                            del st.session_state[key]
                    # ---------------------------------------------
                    # Instantly redirect the user to the Quiz UI
                    st.switch_page("pages/quiz.py") # <--- MAKE SURE YOUR FILE IS NAMED quiz.py
                    
                else:
                    st.error("AI Generation failed. Check your terminal for Hugging Face errors.")
            else:
                st.error(f"Failed to process content: {status}")