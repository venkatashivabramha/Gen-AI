"""
Authentication Page
Login and signup functionality with MongoDB
"""
import streamlit as st
import bcrypt
import re
from pymongo import MongoClient
from datetime import datetime
import os

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Initialize session state BEFORE accessing it
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# MongoDB connection
@st.cache_resource
def get_db_connection():
    """Connect to MongoDB Atlas (free tier)"""
    mongodb_uri = os.getenv('MONGODB_URI', st.secrets.get('MONGODB_URI', ''))
    
    # Check if URI is valid (not placeholder or empty)
    if not mongodb_uri or 'username:password' in mongodb_uri or mongodb_uri == '':
        return None
    
    try:
        client = MongoClient(
            mongodb_uri,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
            socketTimeoutMS=3000,
            tlsAllowInvalidCertificates=False
        )
        # Test connection
        client.admin.command('ping')
        return client['business_plan_generator']
    except Exception:
        # Silently return None - app will run in demo mode
        return None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password):
    """Hash password with bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    """Check password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def create_user(db, email, password, full_name):
    """Create new user"""
    users = db['users']
    
    # Check if user exists
    if users.find_one({'email': email}):
        return False, "User already exists"
    
    # Create user
    user = {
        'email': email,
        'password': hash_password(password),
        'full_name': full_name,
        'created_at': datetime.now(),
        'approved': True,  # Auto-approve for demo (change to False for manual approval)
        'is_admin': False,
        'last_login': None
    }
    
    users.insert_one(user)
    return True, "Account created successfully!"

def login_user(db, email, password):
    """Authenticate user"""
    users = db['users']
    
    user = users.find_one({'email': email})
    
    if not user:
        return False, "User not found"
    
    if not user.get('approved', False):
        return False, "Account pending approval. Please contact admin."
    
    if check_password(password, user['password']):
        # Update last login
        users.update_one(
            {'email': email},
            {'$set': {'last_login': datetime.now()}}
        )
        return True, user
    
    return False, "Invalid password"

# Main UI
st.title("🔐 Authentication")

# Check if already logged in
if st.session_state.get('authenticated', False):
    st.success(f"✅ You're logged in as {st.session_state.get('user_email', 'Unknown')}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Generator 📝", use_container_width=True):
            st.switch_page("pages/2_📝_Generate.py")
    with col2:
        if st.button("Logout 🚪", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.is_admin = False
            st.rerun()
    
    st.stop()

# Login/Signup tabs
tab1, tab2 = st.tabs(["🔑 Login", "✍️ Sign Up"])

# Get database connection
db = get_db_connection()

# Show demo mode notice if no MongoDB
if not db:
    st.info("ℹ️ Running in Demo Mode (MongoDB not configured)")

with tab1:
    st.header("Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("Please fill in all fields")
            elif not db:
                # Demo mode - allow any login
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.is_admin = False
                st.success("✅ Logged in (Demo Mode)")
                st.rerun()
            else:
                success, result = login_user(db, email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.is_admin = result.get('is_admin', False)
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")

with tab2:
    st.header("Create New Account")
    
    with st.form("signup_form"):
        full_name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        
        agree = st.checkbox("I agree to the terms and conditions")
        
        submit = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit:
            if not all([full_name, email, password, password_confirm]):
                st.error("Please fill in all fields")
            elif not validate_email(email):
                st.error("Invalid email format")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif password != password_confirm:
                st.error("Passwords don't match")
            elif not agree:
                st.error("Please agree to the terms and conditions")
            elif not db:
                # Demo mode
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.is_admin = False
                st.success("✅ Account created (Demo Mode)")
                st.rerun()
            else:
                success, message = create_user(db, email, password, full_name)
                if success:
                    st.success(f"✅ {message} You can now login.")
                else:
                    st.error(f"❌ {message}")

# Demo mode notice
st.markdown("---")
with st.expander("🔧 Database Configuration"):
    st.markdown("""
    ### MongoDB Atlas Setup (FREE)
    
    1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
    2. Create a free account
    3. Create a free cluster (M0 - FREE forever)
    4. Create a database user
    5. Get connection string
    6. Add to Streamlit secrets:
    
    ```toml
    # .streamlit/secrets.toml
    MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
    ```
    
    **OR** set environment variable:
    ```bash
    export MONGODB_URI="mongodb+srv://..."
    ```
    
    **Without MongoDB:** App runs in demo mode (no data persistence)
    """)