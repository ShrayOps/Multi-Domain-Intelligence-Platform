"""
Login Page - User Authentication Interface
==========================================

This module provides the login and registration functionality for the platform.
It handles:
- User login with username/password authentication
- New user registration
- Session management via Streamlit's session_state

The page uses AuthManager service for secure bcrypt-based password verification.

Session State:
- st.session_state.current_user: Stores the logged-in user's data (dict) or None

Default admin credentials: admin / adminpass
"""

import streamlit as st
from services.auth_manager import AuthManager

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------------------------------------------------------------------
# Session Initialization
# ---------------------------------------------------------------------------
from components.auth import init_session
init_session()

# ---------------------------------------------------------------------------
# Initialize authentication service
# ---------------------------------------------------------------------------
auth = AuthManager()

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("🔐 Login / Register")

# ---------------------------------------------------------------------------
# Check if user is already logged in
# ---------------------------------------------------------------------------
if st.session_state.current_user:
    st.success(f"✅ You are logged in as **{st.session_state.current_user['username']}**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("##### ✅ Session Active")
            st.caption("You have full access to all dashboards.")
            
            if st.button("🚪 Logout", width='stretch', type="primary", key="main_logout"):
                st.session_state.current_user = None
                st.rerun()

else:
    # ---------------------------------------------------------------------------
    # Login/Register tabs for non-authenticated users
    # ---------------------------------------------------------------------------
    st.caption("You must login to access the dashboards.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])
        
        # -------------------------------------------------------------------
        # Login Tab
        # -------------------------------------------------------------------
        with login_tab:
            with st.container(border=True):
                st.markdown("##### Welcome Back")
                
                login_username = st.text_input(
                    "Username", 
                    key="login_username", 
                    max_chars=20,
                    placeholder="Enter your username"
                )
                login_password = st.text_input(
                    "Password", 
                    type="password", 
                    key="login_password", 
                    max_chars=20,
                    placeholder="Enter your password"
                )
                
                if st.button("🔑 Login", width='stretch', type="primary"):
                    user = auth.login(login_username, login_password)
                    if user:
                        st.session_state.current_user = user
                        st.switch_page("Home.py")
                    else:
                        st.error("Invalid credentials or missing username/password.")
        
        # -------------------------------------------------------------------
        # Register Tab
        # -------------------------------------------------------------------
        with register_tab:
            with st.container(border=True):
                st.markdown("##### Create Account")
                
                reg_username = st.text_input(
                    "Username", 
                    key="reg_username", 
                    max_chars=20,
                    placeholder="Choose a username"
                )
                reg_password = st.text_input(
                    "Password", 
                    type="password", 
                    key="reg_password", 
                    max_chars=20,
                    placeholder="Choose a password"
                )
                
                if st.button("📝 Create Account", width='stretch', type="primary"):
                    success = auth.register(reg_username, reg_password)
                    if success:
                        st.success("✅ Account created! Switch to the Login tab to sign in.")
                    else:
                        st.error("Could not create user. Username may already exist or fields are empty.")
        
        st.divider()
