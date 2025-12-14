"""
Home Page - Multi-Domain Intelligence Platform
==============================================

This is the main entry point for the Streamlit application.
Streamlit automatically discovers this file and uses the pages/ directory
for multi-page navigation.

The home page provides:
- Application title and branding
- Overview of available features
- Navigation guidance

Usage:
    streamlit run Home.py
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

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
# Main Content
# ---------------------------------------------------------------------------
st.title("🏠 Multi-Domain Intelligence Platform")

# Show different content based on login status
if st.session_state.current_user:
    st.success(f"👋 Welcome back, **{st.session_state.current_user['username']}**!")
    
    st.markdown("### 🚀 Quick Access")
    
    # Dashboard cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🛡️ Cybersecurity")
            st.caption("Track security incidents, view metrics, and get AI-powered threat analysis.")
            st.page_link("pages/2_Cybersecurity.py", label="Open Dashboard →", icon="🛡️")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 📊 Data Science")
            st.caption("Manage dataset metadata, analyze storage usage, and optimize governance.")
            st.page_link("pages/3_Data_Science.py", label="Open Dashboard →", icon="📊")
    
    with col3:
        with st.container(border=True):
            st.markdown("### 🖥️ IT Operations")
            st.caption("Monitor support tickets, track resolution times, and identify bottlenecks.")
            st.page_link("pages/4_IT_Operations.py", label="Open Dashboard →", icon="🖥️")
    
    st.divider()
    
    st.markdown("### ✨ Key Features")
    
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("""
        - 📊 **Real-time Metrics** — Monitor KPIs at a glance
        - ✏️ **Full CRUD Operations** — Create, read, update, delete records
        """)
    
    with feat_col2:
        st.markdown("""
        - 📈 **Interactive Visualizations** — Explore data through charts
        - 🤖 **AI Assistant** — Context-aware recommendations via Gemini
        """)

else:
    st.info("👋 Welcome! Please login to access the dashboards.")
    
    st.markdown("### 🔐 Get Started")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.markdown("##### Login Required")
            st.caption("You need to authenticate to access the protected dashboards.")
            st.page_link("pages/1_Login.py", label="Go to Login →", icon="🔐")
    
    with col2:
        with st.container(border=True):
            st.markdown("##### About This Platform")
            st.markdown("""
            A unified web application providing insights into:
            - **Cybersecurity** — Incident tracking & threat analysis
            - **Data Science** — Dataset governance & metadata management  
            - **IT Operations** — Ticket management & performance analytics
            
            Each dashboard includes an embedded AI Assistant for domain-specific recommendations.
            """)
