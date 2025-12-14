"""
Authentication Manager Service
==============================

This module provides secure user authentication and registration functionality.

Features:
- User registration with bcrypt password hashing
- Secure login with password verification
- Automatic users table creation
- Role-based user management (admin/user)

Security Notes:
- Passwords are never stored in plain text
- bcrypt with automatic salt generation is used for hashing
- Password hashes are stored as binary blobs in SQLite
- Login returns minimal user data (no password hash)

Database Table: users
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - username: TEXT UNIQUE
    - password_hash: BLOB (bcrypt output)
    - role: TEXT DEFAULT 'user'

Usage:
    auth = AuthManager()
    auth.register("username", "password", role="user")
    user = auth.login("username", "password")
"""

import bcrypt
from services.database_manager import DatabaseManager


class AuthManager:
    """
    Handles user authentication including registration and login.
    Uses bcrypt for secure password hashing.
    """
    
    def __init__(self):
        """
        Initialize the authentication manager.
        Creates the users table if it doesn't exist.
        """
        self.db = DatabaseManager()
        self._create_table()
    
    def _create_table(self):
        """
        Create the users table if it doesn't exist.
        
        Table Schema:
            - id: Auto-incrementing primary key
            - username: Unique identifier for the user
            - password_hash: bcrypt-hashed password (binary blob)
            - role: User role for authorization (default: 'user')
        """
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash BLOB,
                role TEXT DEFAULT 'user'
            )
        """)
    
    def register(self, username: str, password: str, role: str = "user") -> bool:
        """
        Register a new user with hashed password.
        
        Args:
            username: Unique username for the new user
            password: Plain text password (will be hashed)
            role: User role - 'user' or 'admin' (default: 'user')
        
        Returns:
            True if registration successful, False otherwise
        
        Notes:
            - Returns False if username/password is empty
            - Returns False if username already exists
            - Password is hashed with bcrypt before storage
        """
        # Validate inputs
        if not username or not password:
            return False
        
        # Hash password with bcrypt (includes automatic salt generation)
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            # Insert new user into database
            self.db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                (username, hashed, role)
            )
            return True
        except Exception:
            # Username conflict or database error
            return False
    
    def login(self, username: str, password: str):
        """
        Authenticate a user with username and password.
        
        Args:
            username: The username to authenticate
            password: Plain text password to verify
        
        Returns:
            dict: User data (id, username, role) on success
            None: On authentication failure
        
        Notes:
            - Handles various password_hash formats (bytes, memoryview, str)
            - Never returns the password hash in the result
            - Returns None for any error (security best practice)
        """
        # Validate inputs
        if not username or not password:
            return None
        
        # Fetch user from database
        row = self.db.fetchone("SELECT * FROM users WHERE username = ?", (username,))
        if not row:
            return None
        
        try:
            # Handle different password_hash formats from SQLite
            pwd_hash = row["password_hash"]
            
            # Convert memoryview to bytes if needed
            if isinstance(pwd_hash, memoryview):
                pwd_hash = pwd_hash.tobytes()
            
            # Convert string to bytes if needed
            if isinstance(pwd_hash, str):
                pwd_hash = pwd_hash.encode('utf-8')
            
            # Verify password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), pwd_hash):
                # Return user data without password hash
                return {
                    "id": row["id"],
                    "username": row["username"],
                    "role": row["role"]
                }
        except Exception:
            # Any verification error = authentication failure
            pass
        
        return None
