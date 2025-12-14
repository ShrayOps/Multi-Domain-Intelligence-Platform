"""
Database Manager Service
========================

This module provides a centralized database access layer for the application.
It wraps SQLite operations and ensures consistent connection handling.

Features:
- Single connection management per instance
- Parameterized query support (SQL injection prevention)
- Automatic commit on write operations
- Row factory for dict-like row access

Security Notes:
- All queries should use parameterized inputs
- Never concatenate user input directly into SQL strings
- Use the params tuple for all dynamic values

Usage:
    db = DatabaseManager()
    db.execute("INSERT INTO table (col) VALUES (?)", ("value",))
    rows = db.fetchall("SELECT * FROM table WHERE col = ?", ("value",))
    row = db.fetchone("SELECT * FROM table WHERE id = ?", (1,))
"""

from database.db import get_connection


class DatabaseManager:
    """
    Centralized database access manager.
    Provides methods for executing queries and fetching results.
    """
    
    def __init__(self):
        """
        Initialize database manager with a single connection.
        
        Creates a persistent connection and cursor for the lifetime
        of this instance. The connection uses sqlite3.Row factory
        for dict-like row access.
        """
        self.conn = get_connection()
        self.cur = self.conn.cursor()
    
    def execute(self, query: str, params: tuple = ()):
        """
        Execute a write operation (INSERT, UPDATE, DELETE, DDL).
        
        Args:
            query: SQL statement with ? placeholders for parameters
            params: Tuple of values to substitute into placeholders
        
        Returns:
            sqlite3.Cursor: The cursor after execution
        
        Notes:
            - Automatically commits after execution
            - Use for INSERT, UPDATE, DELETE, CREATE TABLE, etc.
            - Always use parameterized queries for security
        
        Example:
            db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
            db.execute("UPDATE users SET name = ? WHERE id = ?", ("Bob", 1))
        """
        self.cur.execute(query, params)
        self.conn.commit()
        return self.cur
    
    def fetchall(self, query: str, params: tuple = ()):
        """
        Execute a SELECT query and return all matching rows.
        
        Args:
            query: SQL SELECT statement with ? placeholders
            params: Tuple of values to substitute into placeholders
        
        Returns:
            list: List of sqlite3.Row objects (dict-like access)
        
        Example:
            rows = db.fetchall("SELECT * FROM users WHERE role = ?", ("admin",))
            for row in rows:
                print(row["username"])
        """
        cur = self.cur.execute(query, params)
        return cur.fetchall()
    
    def fetchone(self, query: str, params: tuple = ()):
        """
        Execute a SELECT query and return the first matching row.
        
        Args:
            query: SQL SELECT statement with ? placeholders
            params: Tuple of values to substitute into placeholders
        
        Returns:
            sqlite3.Row: Single row object or None if no match
        
        Example:
            user = db.fetchone("SELECT * FROM users WHERE id = ?", (1,))
            if user:
                print(user["username"])
        """
        cur = self.cur.execute(query, params)
        return cur.fetchone()
