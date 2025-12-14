"""
Components Package
==================

This package contains reusable UI components and helper functions
shared across multiple pages in the application.

Available Components:
    - init_session: Initialize authentication session state
    - is_authenticated: Check if user is logged in
    - require_auth: Protect pages that require authentication

Usage:
    from components.auth import init_session, require_auth
    init_session()
    require_auth()
"""
