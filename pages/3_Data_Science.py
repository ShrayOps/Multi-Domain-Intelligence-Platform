"""
Data Science Dashboard - Dataset Governance
============================================

This module provides a comprehensive data science dashboard featuring:
- Real-time metrics: total datasets, total rows, dataset count
- CRUD operations: create, view, edit, and delete dataset metadata
- Data visualization: datasets by uploader, row distribution
- AI Assistant: context-aware data governance recommendations powered by Gemini

Protected page: Requires user authentication via session_state.

Database Table: datasets_metadata
    - id: INTEGER PRIMARY KEY
    - dataset_id: INTEGER (external ID)
    - name: TEXT (dataset name)
    - rows: INTEGER (number of records)
    - columns: INTEGER (number of columns/features)
    - uploaded_by: TEXT (uploader username)
    - upload_date: TEXT (upload date)
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
from services.dataset_service import DatasetService
from services.ai_assistant import AIAssistant

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.title("📊 Data Science Dashboard")
st.caption("Dataset Governance & Management")
ds = DatasetService()

# ===========================================================================
# SECTION 1: KEY METRICS
# ===========================================================================
st.subheader("📊 Key Metrics")
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    total_datasets = ds.total_count()
    st.metric("Total Datasets", total_datasets)

with metric_col2:
    total_rows = ds.total_rows()
    st.metric("Total Rows", f"{total_rows:,}")

with metric_col3:
    avg_rows = total_rows / total_datasets if total_datasets > 0 else 0
    st.metric("Avg Rows/Dataset", f"{avg_rows:,.0f}")

st.divider()

# ===========================================================================
# SECTION 2: DATA MANAGEMENT (Add, Edit/Delete, Load Sample)
# ===========================================================================
st.subheader("🔧 Manage Datasets")

rows = ds.all()

action_tabs = st.tabs(["➕ Add New", "✏️ Edit / Delete", "📥 Load Sample Data"])

# -------------------------------------------------------------------------
# Tab 1: Add New Dataset
# -------------------------------------------------------------------------
with action_tabs[0]:
    with st.form("new_dataset_form", border=True):
        st.markdown("##### Register New Dataset")
        
        form_row1 = st.columns(3)
        with form_row1[0]:
            new_dataset_id = st.number_input("Dataset ID", min_value=1, value=1, step=1)
        with form_row1[1]:
            new_name = st.text_input("Dataset Name", placeholder="e.g., Customer_Churn")
        with form_row1[2]:
            new_uploaded_by = st.text_input("Uploaded By", placeholder="e.g., data_scientist")
        
        form_row2 = st.columns(3)
        with form_row2[0]:
            new_rows = st.number_input("Number of Rows", min_value=0, value=1000, step=100)
        with form_row2[1]:
            new_columns = st.number_input("Number of Columns", min_value=1, value=10, step=1)
        with form_row2[2]:
            new_upload_date = st.date_input("Upload Date")
        
        if st.form_submit_button("➕ Add Dataset", type="primary"):
            if new_name and new_uploaded_by:
                ds.create_dataset(new_dataset_id, new_name, new_rows, new_columns, new_uploaded_by, str(new_upload_date))
                st.success(f"✅ Added dataset: {new_name}")
                st.rerun()
            else:
                st.error("Dataset name and uploader are required")

# -------------------------------------------------------------------------
# Tab 2: Edit / Delete Dataset
# -------------------------------------------------------------------------
with action_tabs[1]:
    if rows:
        dataset_options = {
            f"#{row['dataset_id']} — {row['name']} | {row['rows']:,} rows | {row['columns']} cols": row['id'] 
            for row in rows
        }
        
        selected = st.selectbox(
            "Select a dataset to modify:",
            list(dataset_options.keys()),
            key="dataset_selector"
        )
        selected_id = dataset_options[selected]
        selected_dataset = next(r for r in rows if r['id'] == selected_id)
        
        edit_col, delete_col = st.columns([2, 1])
        
        with edit_col:
            with st.form("edit_dataset_form", border=True):
                st.markdown("##### Edit Dataset")
                
                edit_row1 = st.columns(2)
                with edit_row1[0]:
                    edit_dataset_id = st.number_input(
                        "Dataset ID", 
                        min_value=1, 
                        value=int(selected_dataset['dataset_id'])
                    )
                with edit_row1[1]:
                    edit_name = st.text_input("Name", value=selected_dataset['name'])
                
                edit_row2 = st.columns(2)
                with edit_row2[0]:
                    edit_uploaded_by = st.text_input("Uploaded By", value=selected_dataset['uploaded_by'])
                with edit_row2[1]:
                    edit_upload_date = st.date_input(
                        "Upload Date", 
                        value=pd.to_datetime(selected_dataset['upload_date'])
                    )
                
                edit_row3 = st.columns(2)
                with edit_row3[0]:
                    edit_rows = st.number_input(
                        "Rows", 
                        min_value=0, 
                        value=int(selected_dataset['rows']), 
                        step=100
                    )
                with edit_row3[1]:
                    edit_columns = st.number_input(
                        "Columns", 
                        min_value=1, 
                        value=int(selected_dataset['columns']), 
                        step=1
                    )
                
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    if edit_name and edit_uploaded_by:
                        ds.update_dataset(
                            selected_id, edit_dataset_id, edit_name, 
                            edit_rows, edit_columns, edit_uploaded_by, str(edit_upload_date)
                        )
                        st.success("✅ Dataset updated!")
                        st.rerun()
                    else:
                        st.error("Name and uploader are required")
        
        with delete_col:
            with st.container(border=True):
                st.markdown("##### Delete Dataset")
                st.error(
                    f"**⚠️ Delete this dataset?**\n\n"
                    f"**ID:** {selected_dataset['dataset_id']}\n\n"
                    f"**Name:** {selected_dataset['name']}\n\n"
                    f"**Rows:** {selected_dataset['rows']:,}"
                )
                if st.button("🗑️ Confirm Delete", type="primary", key="delete_dataset"):
                    ds.delete_dataset(selected_id)
                    st.success("✅ Dataset deleted!")
                    st.rerun()
    else:
        st.info("📭 No datasets to edit. Add a dataset or load sample data first.")

# -------------------------------------------------------------------------
# Tab 3: Load Sample Data
# -------------------------------------------------------------------------
with action_tabs[2]:
    st.markdown("Load sample dataset metadata from CSV file to get started quickly.")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("📥 Load Sample Datasets", type="secondary"):
            ds.load_csv("data/datasets_metadata.csv")
            st.success("✅ Sample datasets loaded!")
            st.rerun()
    with col2:
        st.caption("Source: `data/datasets_metadata.csv`")

st.divider()

# ===========================================================================
# SECTION 3: DATASETS TABLE
# ===========================================================================
if rows:
    df = pd.DataFrame([dict(r) for r in rows])
    
    st.subheader("🗂️ Datasets Table")
    st.dataframe(df, height=350, width='stretch')
    
    st.divider()
    
    # ===========================================================================
    # SECTION 4: DATA VISUALIZATIONS
    # ===========================================================================
    st.subheader("📈 Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        fig_cols = px.bar(
            df, x="name", y="columns", 
            title="Column Count by Dataset", 
            color="columns",
            color_continuous_scale="Blues"
        )
        fig_cols.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_cols, width='stretch')
    
    with viz_col2:
        fig_rows = px.bar(
            df, x="name", y="rows", 
            title="Row Count by Dataset", 
            color="rows",
            color_continuous_scale="Greens"
        )
        fig_rows.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_rows, width='stretch')
    
    uploader_counts = df['uploaded_by'].value_counts().reset_index()
    uploader_counts.columns = ['uploaded_by', 'count']
    fig_uploaders = px.pie(uploader_counts, values="count", names="uploaded_by", title="Datasets by Uploader")
    fig_uploaders.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_uploaders, width='stretch')

else:
    st.info("📭 No datasets found. Add a new dataset or load sample data to get started.")

st.divider()

# ===========================================================================
# SECTION 5: AI ASSISTANT
# ===========================================================================
st.subheader("🤖 AI Assistant")

with st.container(border=True):
    st.markdown("Get AI-powered recommendations for dataset governance and optimization.")
    
    ai_prompt = st.text_area(
        "Your Question", 
        height=100, 
        placeholder="E.g., 'Which datasets need better documentation?' or 'How can we optimize data storage?'",
        key="data_ai_prompt"
    )
    
    if st.button("🚀 Ask AI", key="data_ask_ai", type="primary"):
        if ai_prompt:
            ai = AIAssistant()
            with st.spinner("🔍 Analyzing..."):
                if rows:
                    df = pd.DataFrame([dict(r) for r in rows])
                    context = f"Current datasets context: {len(rows)} total datasets, {ds.total_rows():,} total rows. "
                    context += f"Uploaders: {df['uploaded_by'].value_counts().to_dict()}"
                    full_prompt = f"{context}\n\nUser question: {ai_prompt}"
                else:
                    full_prompt = ai_prompt
                
                answer = ai.ask(full_prompt)
            
            st.markdown("**AI Response:**")
            st.write(answer)
        else:
            st.warning("Please enter a question")
