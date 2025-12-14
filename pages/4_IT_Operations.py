"""
IT Operations Dashboard - Service Desk Analytics
=================================================

This module provides a comprehensive IT operations dashboard featuring:
- Real-time metrics: total tickets, open tickets, average resolution time
- CRUD operations: create, view, edit, and delete support tickets
- Data visualization: ticket status, priority distribution, assignee performance
- AI Assistant: context-aware operational recommendations powered by Gemini

Protected page: Requires user authentication via session_state.

Database Table: it_tickets
    - id: INTEGER PRIMARY KEY
    - ticket_id: INTEGER (external ID)
    - priority: TEXT (Low, Medium, High, Critical)
    - description: TEXT
    - status: TEXT (Open, In Progress, Waiting for User, Resolved)
    - assigned_to: TEXT
    - created_at: TEXT
    - resolution_time_hours: INTEGER
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
from services.it_service import ITService
from services.ai_assistant import AIAssistant

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.title("🖥️ IT Operations Dashboard")
st.caption("Service Desk Analytics & Ticket Management")
its = ITService()

# ===========================================================================
# SECTION 1: KEY METRICS
# ===========================================================================
st.subheader("📊 Key Metrics")
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    total_tickets = its.total_count()
    st.metric("Total Tickets", total_tickets)

with metric_col2:
    open_tickets = its.open_count()
    st.metric("Open/In Progress", open_tickets)

with metric_col3:
    avg_resolution = its.avg_resolution_time()
    st.metric("Avg Resolution", f"{avg_resolution} hrs")

st.divider()

# ===========================================================================
# SECTION 2: DATA MANAGEMENT (Create, Edit/Delete, Load Sample)
# ===========================================================================
st.subheader("🔧 Manage Tickets")

rows = its.all()

action_tabs = st.tabs(["➕ Add New", "✏️ Edit / Delete", "📥 Load Sample Data"])

# -------------------------------------------------------------------------
# Tab 1: Create New Ticket
# -------------------------------------------------------------------------
with action_tabs[0]:
    with st.form("new_ticket_form", border=True):
        st.markdown("##### Create New Ticket")
        
        form_row1 = st.columns(4)
        with form_row1[0]:
            new_ticket_id = st.number_input("Ticket ID", min_value=1, value=2000, step=1)
        with form_row1[1]:
            new_priority = st.selectbox(
                "Priority", 
                ["Low", "Medium", "High", "Critical"]
            )
        with form_row1[2]:
            new_status = st.selectbox(
                "Status", 
                ["Open", "In Progress", "Waiting for User", "Resolved"]
            )
        with form_row1[3]:
            new_assigned_to = st.text_input("Assigned To", placeholder="e.g., IT_Support_A")
        
        form_row2 = st.columns(3)
        with form_row2[0]:
            new_date = st.date_input("Date")
        with form_row2[1]:
            new_time = st.time_input("Time")
        with form_row2[2]:
            new_resolution_hours = st.number_input(
                "Resolution Time (hrs)", 
                min_value=0, 
                value=0, 
                step=1
            )
        
        new_description = st.text_area("Description", placeholder="Describe the issue...", height=80)
        
        if st.form_submit_button("➕ Create Ticket", type="primary"):
            if new_description and new_assigned_to:
                timestamp = f"{new_date} {new_time}"
                its.create_ticket(
                    new_ticket_id, new_priority, new_description, 
                    new_status, new_assigned_to, timestamp, new_resolution_hours
                )
                st.success(f"✅ Created ticket #{new_ticket_id}")
                st.rerun()
            else:
                st.error("Description and assignee are required")

# -------------------------------------------------------------------------
# Tab 2: Edit / Delete Ticket
# -------------------------------------------------------------------------
with action_tabs[1]:
    if rows:
        ticket_options = {
            f"#{row['ticket_id']} — {row['priority']} | {row['status']} | {row['assigned_to']}": row['id'] 
            for row in rows
        }
        
        selected = st.selectbox(
            "Select a ticket to modify:",
            list(ticket_options.keys()),
            key="ticket_selector"
        )
        selected_id = ticket_options[selected]
        selected_ticket = next(r for r in rows if r['id'] == selected_id)
        
        edit_col, delete_col = st.columns([2, 1])
        
        with edit_col:
            with st.form("edit_ticket_form", border=True):
                st.markdown("##### Edit Ticket")
                
                edit_row1 = st.columns(2)
                with edit_row1[0]:
                    edit_ticket_id = st.number_input(
                        "Ticket ID", 
                        min_value=1, 
                        value=int(selected_ticket['ticket_id'])
                    )
                with edit_row1[1]:
                    edit_priority = st.selectbox(
                        "Priority", 
                        ["Low", "Medium", "High", "Critical"],
                        index=["Low", "Medium", "High", "Critical"].index(selected_ticket['priority']) 
                            if selected_ticket['priority'] in ["Low", "Medium", "High", "Critical"] else 0
                    )
                
                edit_row2 = st.columns(2)
                with edit_row2[0]:
                    edit_status = st.selectbox(
                        "Status", 
                        ["Open", "In Progress", "Waiting for User", "Resolved"],
                        index=["Open", "In Progress", "Waiting for User", "Resolved"].index(selected_ticket['status']) 
                            if selected_ticket['status'] in ["Open", "In Progress", "Waiting for User", "Resolved"] else 0
                    )
                with edit_row2[1]:
                    edit_assigned_to = st.text_input("Assigned To", value=selected_ticket['assigned_to'])
                
                edit_row3 = st.columns(3)
                with edit_row3[0]:
                    # Parse existing timestamp for date
                    try:
                        existing_dt = pd.to_datetime(selected_ticket['created_at'])
                        edit_date = st.date_input("Date", value=existing_dt.date())
                    except:
                        edit_date = st.date_input("Date")
                with edit_row3[1]:
                    # Parse existing timestamp for time
                    try:
                        existing_dt = pd.to_datetime(selected_ticket['created_at'])
                        edit_time = st.time_input("Time", value=existing_dt.time())
                    except:
                        edit_time = st.time_input("Time")
                with edit_row3[2]:
                    edit_resolution = st.number_input(
                        "Resolution Hours", 
                        min_value=0, 
                        value=int(selected_ticket['resolution_time_hours']), 
                        step=1
                    )
                
                edit_description = st.text_area("Description", value=selected_ticket['description'] or "", height=80)
                
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    if edit_description and edit_assigned_to:
                        edit_created_at = f"{edit_date} {edit_time}"
                        its.update_ticket(
                            selected_id, edit_ticket_id, edit_priority, edit_description,
                            edit_status, edit_assigned_to, edit_created_at, edit_resolution
                        )
                        st.success("✅ Ticket updated!")
                        st.rerun()
                    else:
                        st.error("Description and assignee are required")
        
        with delete_col:
            with st.container(border=True):
                st.markdown("##### Delete Ticket")
                st.error(
                    f"**⚠️ Delete this ticket?**\n\n"
                    f"**ID:** {selected_ticket['ticket_id']}\n\n"
                    f"**Priority:** {selected_ticket['priority']}\n\n"
                    f"**Status:** {selected_ticket['status']}"
                )
                if st.button("🗑️ Confirm Delete", type="primary", key="delete_ticket"):
                    its.delete_ticket(selected_id)
                    st.success("✅ Ticket deleted!")
                    st.rerun()
    else:
        st.info("📭 No tickets to edit. Create a ticket or load sample data first.")

# -------------------------------------------------------------------------
# Tab 3: Load Sample Data
# -------------------------------------------------------------------------
with action_tabs[2]:
    st.markdown("Load sample tickets from CSV file to get started quickly.")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("📥 Load Sample Tickets", type="secondary"):
            its.load_csv("data/it_tickets.csv")
            st.success("✅ Sample tickets loaded!")
            st.rerun()
    with col2:
        st.caption("Source: `data/it_tickets.csv`")

st.divider()

# ===========================================================================
# SECTION 3: TICKETS TABLE
# ===========================================================================
if rows:
    df = pd.DataFrame([dict(r) for r in rows])
    
    st.subheader("🗂️ Tickets Table")
    st.dataframe(df, height=350, width='stretch')
    
    st.divider()
    
    # ===========================================================================
    # SECTION 4: DATA VISUALIZATIONS
    # ===========================================================================
    st.subheader("📈 Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        status_data = its.status_counts()
        if status_data:
            status_df = pd.DataFrame([dict(r) for r in status_data])
            fig_status = px.pie(status_df, values="cnt", names="status", title="Tickets by Status")
            fig_status.update_layout(margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig_status, width='stretch')
    
    with viz_col2:
        priority_data = its.priority_counts()
        if priority_data:
            priority_df = pd.DataFrame([dict(r) for r in priority_data])
            fig_priority = px.bar(priority_df, x="priority", y="cnt", title="Tickets by Priority", color="priority")
            fig_priority.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig_priority, width='stretch')
    
    assignee_data = its.assignee_summary()
    if assignee_data:
        assignee_df = pd.DataFrame([dict(r) for r in assignee_data])
        fig_assignee = px.bar(
            assignee_df, 
            x="assigned_to", 
            y="avg_resolution", 
            title="Avg Resolution Hours by Assignee",
            color="ticket_count",
            labels={"avg_resolution": "Avg Hours", "assigned_to": "Assignee", "ticket_count": "Ticket Count"}
        )
        fig_assignee.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_assignee, width='stretch')
    
    # -----------------------------------------------------------------------
    # Performance Analysis
    # -----------------------------------------------------------------------
    st.subheader("⚡ Performance Analysis")
    slowest = its.slowest_assignee()
    
    if slowest and assignee_data:
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.error(f"🐢 **Slowest Assignee:** {slowest[0]['assigned_to']} (~{round(slowest[0]['avg_res'], 1)} hrs avg)")
        
        with perf_col2:
            fastest = min(assignee_data, key=lambda x: x['avg_resolution'])
            st.success(f"🚀 **Fastest Assignee:** {fastest['assigned_to']} (~{round(fastest['avg_resolution'], 1)} hrs avg)")

else:
    st.info("📭 No tickets found. Create a new ticket or load sample data to get started.")

st.divider()

# ===========================================================================
# SECTION 5: AI ASSISTANT
# ===========================================================================
st.subheader("🤖 AI Assistant")

with st.container(border=True):
    st.markdown("Get AI-powered insights to improve IT operations and reduce resolution times.")
    
    ai_prompt = st.text_area(
        "Your Question", 
        height=100, 
        placeholder="E.g., 'How can we reduce ticket resolution time?' or 'Which priority level needs more attention?'",
        key="it_ai_prompt"
    )
    
    if st.button("🚀 Ask AI", key="it_ask_ai", type="primary"):
        if ai_prompt:
            ai = AIAssistant()
            with st.spinner("🔍 Analyzing..."):
                if rows:
                    df = pd.DataFrame([dict(r) for r in rows])
                    context = f"Current tickets context: {len(rows)} total tickets, {its.open_count()} open/in progress, avg resolution: {its.avg_resolution_time()} hours. "
                    context += f"Priorities: {df['priority'].value_counts().to_dict()}. "
                    context += f"Statuses: {df['status'].value_counts().to_dict()}"
                    full_prompt = f"{context}\n\nUser question: {ai_prompt}"
                else:
                    full_prompt = ai_prompt
                
                answer = ai.ask(full_prompt)
            
            st.markdown("**AI Response:**")
            st.write(answer)
        else:
            st.warning("Please enter a question")
