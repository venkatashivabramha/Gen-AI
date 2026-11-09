"""
Admin Dashboard
User management and system monitoring
"""
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Admin Dashboard", page_icon="⚙️", layout="wide")

# Check admin access
if not st.session_state.get('is_admin', False):
    st.warning("🔒 Admin access required")
    st.info("Please login with an admin account to access this page")
    st.stop()

st.title("⚙️ Admin Dashboard")
st.markdown(f"Welcome, **{st.session_state.get('user_email', 'Admin')}**")

# MongoDB connection
@st.cache_resource
def get_db_connection():
    mongodb_uri = os.getenv('MONGODB_URI', st.secrets.get('MONGODB_URI', ''))
    if mongodb_uri:
        client = MongoClient(mongodb_uri)
        return client['business_plan_generator']
    return None

db = get_db_connection()

if not db:
    st.error("Database not configured. Admin features unavailable.")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["👥 Users", "📊 Statistics", "⚙️ Settings"])

with tab1:
    st.header("User Management")
    
    # Get all users
    users = list(db['users'].find({}, {'password': 0}))  # Exclude passwords
    
    if users:
        # Convert to DataFrame
        df = pd.DataFrame(users)
        df['_id'] = df['_id'].astype(str)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(users))
        with col2:
            approved = sum(1 for u in users if u.get('approved', False))
            st.metric("Approved", approved)
        with col3:
            pending = sum(1 for u in users if not u.get('approved', False))
            st.metric("Pending", pending)
        with col4:
            admins = sum(1 for u in users if u.get('is_admin', False))
            st.metric("Admins", admins)
        
        st.markdown("---")
        
        # User list
        st.subheader("All Users")
        
        for user in users:
            with st.expander(f"👤 {user.get('full_name', 'Unknown')} - {user['email']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Email:** {user['email']}")
                    st.write(f"**Name:** {user.get('full_name', 'N/A')}")
                    st.write(f"**Created:** {user.get('created_at', 'N/A')}")
                    st.write(f"**Last Login:** {user.get('last_login', 'Never')}")
                
                with col2:
                    st.write(f"**Status:** {'✅ Approved' if user.get('approved') else '⏳ Pending'}")
                    st.write(f"**Role:** {'👑 Admin' if user.get('is_admin') else '👤 User'}")
                
                # Actions
                st.markdown("**Actions:**")
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if not user.get('approved', False):
                        if st.button(f"✅ Approve", key=f"approve_{user['_id']}"):
                            db['users'].update_one(
                                {'_id': user['_id']},
                                {'$set': {'approved': True}}
                            )
                            st.success("User approved!")
                            st.rerun()
                    else:
                        if st.button(f"❌ Revoke", key=f"revoke_{user['_id']}"):
                            db['users'].update_one(
                                {'_id': user['_id']},
                                {'$set': {'approved': False}}
                            )
                            st.success("Approval revoked!")
                            st.rerun()
                
                with action_col2:
                    if not user.get('is_admin', False):
                        if st.button(f"👑 Make Admin", key=f"admin_{user['_id']}"):
                            db['users'].update_one(
                                {'_id': user['_id']},
                                {'$set': {'is_admin': True}}
                            )
                            st.success("User promoted to admin!")
                            st.rerun()
                
                with action_col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{user['_id']}"):
                        db['users'].delete_one({'_id': user['_id']})
                        st.success("User deleted!")
                        st.rerun()
    else:
        st.info("No users found")

with tab2:
    st.header("System Statistics")
    
    # User stats
    users = list(db['users'].find())
    
    if users:
        df = pd.DataFrame(users)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Registrations over time
        st.subheader("User Registrations Over Time")
        daily_signups = df.groupby(df['created_at'].dt.date).size()
        st.line_chart(daily_signups)
        
        # User status pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("User Status")
            status_counts = {
                'Approved': sum(1 for u in users if u.get('approved', False)),
                'Pending': sum(1 for u in users if not u.get('approved', False))
            }
            st.bar_chart(status_counts)
        
        with col2:
            st.subheader("User Roles")
            role_counts = {
                'Admins': sum(1 for u in users if u.get('is_admin', False)),
                'Users': sum(1 for u in users if not u.get('is_admin', False))
            }
            st.bar_chart(role_counts)
    else:
        st.info("No data available yet")

with tab3:
    st.header("System Settings")
    
    st.subheader("🔧 Configuration")
    
    with st.form("settings_form"):
        require_approval = st.checkbox(
            "Require admin approval for new users",
            value=True,
            help="When enabled, new users must be approved by an admin before accessing the system"
        )
        
        allow_registration = st.checkbox(
            "Allow new user registration",
            value=True,
            help="When disabled, the signup form will be hidden"
        )
        
        max_generations_per_day = st.number_input(
            "Max generations per user per day",
            min_value=1,
            max_value=100,
            value=10,
            help="Limit to prevent abuse"
        )
        
        submit = st.form_submit_button("Save Settings")
        
        if submit:
            # Save settings to database
            db['settings'].update_one(
                {'_id': 'global'},
                {'$set': {
                    'require_approval': require_approval,
                    'allow_registration': allow_registration,
                    'max_generations_per_day': max_generations_per_day,
                    'updated_at': datetime.now()
                }},
                upsert=True
            )
            st.success("✅ Settings saved!")
    
    st.markdown("---")
    
    st.subheader("📊 System Information")
    st.info(f"""
    **Database:** MongoDB Atlas (Connected ✅)
    
    **Collections:**
    - users: {db['users'].count_documents({})}
    - settings: {db['settings'].count_documents({})}
    
    **System Status:** Operational ✅
    """)
