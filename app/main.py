import streamlit as st
import pandas as pd
import re 
import phonenumbers
from datetime import datetime
from database import db_operations
import datetime
# --- State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

st.set_page_config(page_title="SmartQuizzer Login", layout="wide")

# --- Helper Functions (Previously Missing) ---
email_regex = r"[^@]+@[^@]+\.[^@]+"

def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return parsed_number if phonenumbers.is_valid_number(parsed_number) else None
    except:
        return None

def show_admin_dashboard():
    """Displays the database contents for administrators."""
    st.header("Admin Dashboard - Database View")
    st.info("Here you can see the live data stored in your MongoDB collections.")
    
    # Fetch all users from the database, excluding the password hash and Mongo _id
    users_cursor = db_operations.users_collection.find({}, {"_id": 0, "password": 0})
    users_list = list(users_cursor)
    
    if users_list:
        df = pd.DataFrame(users_list)
        st.subheader("Registered Users Table")
        st.dataframe(df, use_container_width=True)
        
        # Displaying some quick analytics
        c1, c2, c3 = st.columns(3)
        c1.metric(label="Total Registered Users", value=len(users_list))
        c2.metric(label="Quizzes Generated", value="0") 
        c3.metric(label="System Status", value="Online")
    else:
        st.warning("No users found in the database yet.")

# --- ROUTING LOGIC ---
# If already logged in AND not admin, instantly redirect to the user dashboard
if st.session_state.logged_in and st.session_state.user_data.get('email') != "admin@smartquizzer.com":
    st.switch_page("pages/home.py") # Make sure your file in the pages folder is named home.py

# --- MAIN UI ---
if not st.session_state.logged_in:
    st.title("Welcome to SmartQuizzer")
    col1, col2 = st.columns(2)
    
    # --- LOGIN SECTION ---
    with col1:
        st.header("Login")
        with st.form("login_form"):
            login_email = st.text_input("Email address")
            login_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                success, result = db_operations.authenticate_user(login_email, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = result 
                    
                    # REDIRECT LOGIC
                    if login_email == "admin@smartquizzer.com":
                        st.rerun() # Stay on main.py for admin dashboard
                    else:
                        st.switch_page("pages/home.py") # Send regular users to home.py
                else:
                    st.error(result)

    # --- SIGNUP SECTION ---
    with col2:
        st.header("Sign up")
        with st.form(key="signup_form"):
            name = st.text_input("User Name:")
            # Set your vast date range
            start_date = datetime.date(1900, 1, 1)
            end_date = datetime.date(2100, 12, 31)

            # Pass them into the date_input widget
            dob_input = st.date_input(
                "Select a date:",
                value="today",           # The default highlighted date
                min_value=start_date,    # The furthest back they can scroll
                max_value=end_date       # The furthest forward they can scroll
            )
            # dob_input = st.date_input("Select Date of Birth:")
            email_input = st.text_input("Enter Email Address")
            phone_number = st.text_input("Enter Phone Number:", placeholder="+91 4123 345 678")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button(label='Register'):
                # 1. Validation Checks
                valid_phone = validate_phone_number(phone_number)
                valid_email = re.fullmatch(email_regex, email_input)
                
                if not valid_phone:
                    st.error("Invalid phone number. Check format or country code.")
                elif not valid_email:
                    st.error("Invalid email format.")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    # 2. Database Insertion
                    formatted_phone = phonenumbers.format_number(valid_phone, phonenumbers.PhoneNumberFormat.E164)
                    dob_datetime = datetime.combine(dob_input, datetime.min.time()) 
                    
                    success, msg = db_operations.create_user(
                        email=email_input, password=password, name=name, 
                        phone=formatted_phone, dob=dob_datetime
                    )
                    if success:
                        st.success(f"{msg} You can now log in.")
                    else:
                        st.error(msg)

else:
    # --- ADMIN DASHBOARD ---
    # Because of the redirect at the top, ONLY the admin will ever see this part of the script
    col1, col2 = st.columns([8, 2])
    with col1:
        st.success(f"Welcome back, {st.session_state.user_data.get('name', 'Admin')}!")
    with col2:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            st.rerun()
            
    st.divider()

    # Show the database view to the admin
    show_admin_dashboard()