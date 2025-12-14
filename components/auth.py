"""
Authentication Helpers
======================

This module provides authentication helper functions shared across all pages.
These functions manage Streamlit session state for user authentication.

Functions:
    - init_session: Initialize session state for authentication
    - is_authenticated: Check if user is currently logged in
    - require_auth: Protect pages that require authentication

Usage:
    from components.auth import init_session, require_auth
    
    # At the top of each page:
    init_session()
    
    # For protected pages:
    require_auth()  # Stops execution if not logged in
"""

import streamlit as st


def init_session():
    """
    Initialize session state for authentication.
    
    Call this at the top of each page to ensure session state
    is properly initialized before any authentication checks.
    
    Sets st.session_state.current_user to None if not already set.
    """
    if "current_user" not in st.session_state:
        st.session_state.current_user = None


def is_authenticated() -> bool:
    """
    Check if a user is currently authenticated.
    
    Returns:
        bool: True if user is logged in, False otherwise
    """
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    return st.session_state.current_user is not None


def require_auth() -> bool:
    """
    Require authentication to access the current page.
    
    If the user is not logged in, displays a warning message
    and stops page execution using st.stop().
    
    Returns:
        bool: True if authenticated (never returns False, stops instead)
    
    Usage:
        require_auth()  # Place at top of protected pages
        # Code below only runs if user is authenticated
    """
    if not is_authenticated():
        st.warning("🔒 You must be logged in to view this page.")
        st.stop()
    return True
