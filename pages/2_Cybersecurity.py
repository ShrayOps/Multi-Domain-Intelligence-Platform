"""
Cybersecurity Dashboard - Security Incident Management
======================================================

This module provides a comprehensive cybersecurity dashboard featuring:
- Real-time metrics: total incidents, open incidents, severity breakdown
- CRUD operations: create, view, edit, and delete security incidents
- Data visualization: incident distribution by category, severity, and status
- AI Assistant: context-aware security recommendations powered by Gemini

Protected page: Requires user authentication via session_state.

Database Table: cyber_incidents
    - id: INTEGER PRIMARY KEY
    - incident_id: INTEGER (external ID)
    - timestamp: TEXT (incident datetime)
    - severity: TEXT (Low, Medium, High, Critical)
    - category: TEXT (Phishing, Malware, DDoS, Unauthorized Access, Misconfiguration)
    - status: TEXT (Open, In Progress, Resolved, Closed)
    - description: TEXT
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------------------------------------------------------------------
# Session Initialization
# ---------------------------------------------------------------------------
from components.auth import init_session, require_auth
init_session()

# ---------------------------------------------------------------------------
# Authentication check - redirect if not logged in
# ---------------------------------------------------------------------------
require_auth()

# ---------------------------------------------------------------------------
# Imports (placed after auth check to avoid unnecessary loading)
# ---------------------------------------------------------------------------
import pandas as pd
import plotly.express as px
from datetime import datetime
from services.security_service import SecurityService
from services.ai_assistant import AIAssistant

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.title("🛡️ Cybersecurity Dashboard")
st.caption("Security Incident Management & Threat Analysis")
serv = SecurityService()

# ===========================================================================
# SECTION 1: KEY METRICS
# ===========================================================================
st.subheader("📊 Key Metrics")
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    total_incidents = serv.total_count()
    st.metric("Total Incidents", total_incidents)

with metric_col2:
    open_incidents = serv.open_count()
    st.metric("Open/In Progress", open_incidents)

with metric_col3:
    severity_data = serv.severity_counts()
    critical_high = 0
    if severity_data:
        for row in severity_data:
            if row["severity"] in ["Critical", "High"]:
                critical_high += row["cnt"]
    st.metric("Critical/High Severity", critical_high)

st.divider()

# ===========================================================================
# SECTION 2: DATA MANAGEMENT (Add, Edit/Delete, Load Sample)
# ===========================================================================
st.subheader("🔧 Manage Incidents")

rows = serv.all()

action_tabs = st.tabs(["➕ Add New", "✏️ Edit / Delete", "📥 Load Sample Data"])

# -------------------------------------------------------------------------
# Tab 1: Add New Incident
# -------------------------------------------------------------------------
with action_tabs[0]:
    with st.form("new_incident_form", border=True):
        st.markdown("##### Create New Incident")
        
        form_row1 = st.columns(3)
        with form_row1[0]:
            new_incident_id = st.number_input("Incident ID", min_value=1, value=1000, step=1)
        with form_row1[1]:
            new_category = st.selectbox(
                "Category", 
                ["Phishing", "Malware", "DDoS", "Unauthorized Access", "Misconfiguration"]
            )
        with form_row1[2]:
            new_severity = st.selectbox(
                "Severity", 
                ["Low", "Medium", "High", "Critical"]
            )
        
        form_row2 = st.columns(3)
        with form_row2[0]:
            new_status = st.selectbox(
                "Status", 
                ["Open", "In Progress", "Resolved", "Closed"]
            )
        with form_row2[1]:
            new_date = st.date_input("Date")
        with form_row2[2]:
            new_time = st.time_input("Time")
        
        new_description = st.text_area("Description", placeholder="Describe the incident...", height=80)
        
        if st.form_submit_button("➕ Add Incident", type="primary"):
            timestamp = f"{new_date} {new_time}"
            serv.create_incident(new_incident_id, timestamp, new_severity, new_category, new_status, new_description)
            st.success(f"✅ Added incident #{new_incident_id}")
            st.rerun()

# -------------------------------------------------------------------------
# Tab 2: Edit / Delete Incident
# -------------------------------------------------------------------------
with action_tabs[1]:
    if rows:
        incident_options = {
            f"#{row['incident_id']} — {row['category']} | {row['severity']} | {row['status']}": row['id'] 
            for row in rows
        }
        
        selected = st.selectbox(
            "Select an incident to modify:",
            list(incident_options.keys()),
            key="incident_selector"
        )
        selected_id = incident_options[selected]
        selected_incident = next(r for r in rows if r['id'] == selected_id)
        
        edit_col, delete_col = st.columns([2, 1])
        
        with edit_col:
            with st.form("edit_incident_form", border=True):
                st.markdown("##### Edit Incident")
                
                edit_row1 = st.columns(2)
                with edit_row1[0]:
                    edit_incident_id = st.number_input(
                        "Incident ID", 
                        min_value=1, 
                        value=int(selected_incident['incident_id'])
                    )
                with edit_row1[1]:
                    edit_category = st.selectbox(
                        "Category", 
                        ["Phishing", "Malware", "DDoS", "Unauthorized Access", "Misconfiguration"],
                        index=["Phishing", "Malware", "DDoS", "Unauthorized Access", "Misconfiguration"].index(selected_incident['category']) 
                            if selected_incident['category'] in ["Phishing", "Malware", "DDoS", "Unauthorized Access", "Misconfiguration"] else 0
                    )
                
                edit_row2 = st.columns(2)
                with edit_row2[0]:
                    edit_severity = st.selectbox(
                        "Severity", 
                        ["Low", "Medium", "High", "Critical"],
                        index=["Low", "Medium", "High", "Critical"].index(selected_incident['severity']) 
                            if selected_incident['severity'] in ["Low", "Medium", "High", "Critical"] else 0
                    )
                with edit_row2[1]:
                    edit_status = st.selectbox(
                        "Status", 
                        ["Open", "In Progress", "Resolved", "Closed"],
                        index=["Open", "In Progress", "Resolved", "Closed"].index(selected_incident['status']) 
                            if selected_incident['status'] in ["Open", "In Progress", "Resolved", "Closed"] else 0
                    )
                
                edit_row3 = st.columns(2)
                with edit_row3[0]:
                    # Parse existing timestamp for date
                    try:
                        existing_dt = pd.to_datetime(selected_incident['timestamp'])
                        edit_date = st.date_input("Date", value=existing_dt.date())
                    except:
                        edit_date = st.date_input("Date")
                with edit_row3[1]:
                    # Parse existing timestamp for time
                    try:
                        existing_dt = pd.to_datetime(selected_incident['timestamp'])
                        edit_time = st.time_input("Time", value=existing_dt.time())
                    except:
                        edit_time = st.time_input("Time")
                edit_description = st.text_area("Description", value=selected_incident['description'] or "", height=80)
                
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    edit_timestamp = f"{edit_date} {edit_time}"
                    serv.update_incident(
                        selected_id, edit_incident_id, edit_timestamp, 
                        edit_severity, edit_category, edit_status, edit_description
                    )
                    st.success("✅ Incident updated!")
                    st.rerun()
        
        with delete_col:
            with st.container(border=True):
                st.markdown("##### Delete Incident")
                st.error(
                    f"**⚠️ Delete this incident?**\n\n"
                    f"**ID:** {selected_incident['incident_id']}\n\n"
                    f"**Category:** {selected_incident['category']}\n\n"
                    f"**Severity:** {selected_incident['severity']}"
                )
                if st.button("🗑️ Confirm Delete", type="primary", key="delete_incident"):
                    serv.delete_incident(selected_id)
                    st.success("✅ Incident deleted!")
                    st.rerun()
    else:
        st.info("📭 No incidents to edit. Add an incident or load sample data first.")

# -------------------------------------------------------------------------
# Tab 3: Load Sample Data
# -------------------------------------------------------------------------
with action_tabs[2]:
    st.markdown("Load sample incidents from CSV file to get started quickly.")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("📥 Load Sample Incidents", type="secondary"):
            serv.load_csv("data/cyber_incidents.csv")
            st.success("✅ Sample incidents loaded!")
            st.rerun()
    with col2:
        st.caption("Source: `data/cyber_incidents.csv`")

st.divider()

# ===========================================================================
# SECTION 3: INCIDENTS TABLE
# ===========================================================================
if rows:
    df = pd.DataFrame([dict(r) for r in rows])
    
    st.subheader("🗂️ Incidents Table")
    st.dataframe(df, height=350, width='stretch')
    
    st.divider()
    
    # ===========================================================================
    # SECTION 4: DATA VISUALIZATIONS
    # ===========================================================================
    st.subheader("📈 Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        category_data = serv.category_counts()
        if category_data:
            cat_df = pd.DataFrame([dict(r) for r in category_data])
            fig_cat = px.pie(cat_df, values="cnt", names="category", title="Incidents by Category")
            fig_cat.update_layout(margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig_cat, width='stretch')
    
    with viz_col2:
        severity_data = serv.severity_counts()
        if severity_data:
            sev_df = pd.DataFrame([dict(r) for r in severity_data])
            fig_sev = px.bar(sev_df, x="severity", y="cnt", title="Incidents by Severity", color="severity")
            fig_sev.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig_sev, width='stretch')
    
    status_data = serv.status_counts()
    if status_data:
        status_df = pd.DataFrame([dict(r) for r in status_data])
        fig_status = px.bar(status_df, x="status", y="cnt", title="Incidents by Status", color="status")
        fig_status.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_status, width='stretch')

else:
    st.info("📭 No incidents found. Add a new incident or load sample data to get started.")

st.divider()

# ===========================================================================
# SECTION 5: AI ASSISTANT
# ===========================================================================
st.subheader("🤖 AI Assistant")

with st.container(border=True):
    st.markdown("Get AI-powered insights and recommendations based on your cybersecurity data.")
    
    ai_prompt = st.text_area(
        "Your Question", 
        height=100, 
        placeholder="E.g., 'What are the top security threats we should address?' or 'How can we reduce phishing incidents?'",
        key="cyber_ai_prompt"
    )
    
    if st.button("🚀 Ask AI", key="cyber_ask_ai", type="primary"):
        if ai_prompt:
            ai = AIAssistant()
            with st.spinner("🔍 Analyzing..."):
                if rows:
                    df = pd.DataFrame([dict(r) for r in rows])
                    context = f"Current incidents context: {len(rows)} total incidents, {serv.open_count()} open/in progress. "
                    context += f"Categories: {df['category'].value_counts().to_dict()}. "
                    context += f"Severities: {df['severity'].value_counts().to_dict()}"
                    full_prompt = f"{context}\n\nUser question: {ai_prompt}"
                else:
                    full_prompt = ai_prompt
                
                answer = ai.ask(full_prompt)
            
            st.markdown("**AI Response:**")
            st.write(answer)
        else:
            st.warning("Please enter a question")
