"""
User Model
==========

Represents a user account in the system.

Attributes:
    id (int): Unique user identifier
    username (str): Login username
    role (str): User role ('user' or 'admin')

"""


class User:
    """
    Simple User entity for representing authenticated users.
    
    This model mirrors the users database table 
    (excludes password_hash field for security reasons.)
    """
    
    def __init__(self, user_id: int, username: str, role: str = "user"):
        """
        Initialize a User instance.
        
        Args:
            user_id: Unique identifier from database
            username: Login username
            role: User role - 'user' or 'admin' (default: 'user')
        """
        self.id = user_id
        self.username = username
        self.role = role
    
    def to_dict(self) -> dict:
        """
        Convert User to dictionary representation.
        
        Returns:
            dict: User data as {id, username, role}
        """
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"
