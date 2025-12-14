"""
Database Connection Module
==========================

This module provides the core database connection functionality
for the application. It centralizes SQLite configuration and
connection management.

Database File:
    platform.db (located in the same directory as this module)

Configuration:
    - check_same_thread=False: Required for Streamlit's single-process model
    - row_factory=sqlite3.Row: Enables dict-like access to columns
"""

import sqlite3
import os

# ---------------------------------------------------------------------------
# Database File Path
# ---------------------------------------------------------------------------
# Database file is stored in the same directory as this module
DB_PATH = os.path.join(os.path.dirname(__file__), "platform.db")


def get_connection():
    """
    Create and return a SQLite database connection.
    
    Returns:
        sqlite3.Connection: Configured database connection
    
    Configuration:
        - check_same_thread=False: Allows connection sharing in Streamlit
        - row_factory=sqlite3.Row: Enables column access by name
    
    Example:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
        row = cursor.fetchone()
        print(row["username"])  # Dict-like access
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
