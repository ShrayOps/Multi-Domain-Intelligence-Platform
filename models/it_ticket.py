"""
IT Ticket Model
===============

Represents a support ticket in the IT operations system.

Attributes:
    id (int): Database primary key
    ticket_id (int): External ticket identifier
    priority (str): Urgency level (Low, Medium, High, Critical)
    description (str): Brief description of the issue
    status (str): Current state (Open, In Progress, Waiting for User, Resolved)
    assigned_to (str): Staff member responsible
    created_at (str): Ticket creation datetime
    resolution_time_hours (int): Hours to resolve
"""


class ITTicket:
    """
    Entity representing an IT support ticket.
    
    This model mirrors the it_tickets database table.
    Used for tracking and analyzing IT operations.
    """
    
    def __init__(self, id: int, ticket_id: int, priority: str, description: str,
                 status: str, assigned_to: str, created_at: str, resolution_time_hours: int):
        """
        Initialize an ITTicket instance.
        
        Args:
            id: Database primary key
            ticket_id: External ticket identifier
            priority: Urgency level (Low, Medium, High, Critical)
            description: Brief description of the issue
            status: Current state (Open, In Progress, Waiting for User, Resolved)
            assigned_to: Assigned staff member
            created_at: Ticket creation datetime
            resolution_time_hours: Hours taken to resolve (0 if still open)
        """
        self.id = id
        self.ticket_id = ticket_id
        self.priority = priority
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.resolution_time_hours = resolution_time_hours
    
    def to_dict(self) -> dict:
        """
        Convert ITTicket to dictionary representation.
        
        Returns:
            dict: Ticket data with all attributes
        """
        return self.__dict__
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ITTicket(id={self.id}, ticket_id={self.ticket_id}, priority='{self.priority}', status='{self.status}')"
