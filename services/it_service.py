"""
IT Service - Support Ticket Management
======================================

This module provides data access and business logic for managing
IT support tickets in the platform's operations dashboard.

Features:
- CRUD operations for support tickets
- Bulk import from CSV files
- Ticket status and priority tracking
- Performance metrics (resolution times, assignee analysis)
- Bottleneck identification

Database Table: it_tickets
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - ticket_id: INTEGER (external ticket ID)
    - priority: TEXT (Low, Medium, High, Critical)
    - description: TEXT (ticket description)
    - status: TEXT (Open, In Progress, Waiting for User, Resolved)
    - assigned_to: TEXT (assigned staff member)
    - created_at: TEXT (creation datetime)
    - resolution_time_hours: INTEGER (hours to resolve)

Usage:
    service = ITService()
    service.create_ticket(2000, "High", "Email issue", "Open", "IT_Support_A", "2024-01-15 10:00:00", 0)
    tickets = service.all()
"""

import pandas as pd
from services.database_manager import DatabaseManager


class ITService:
    """
    Service class for managing IT support tickets.
    Provides operations tracking and performance analytics.
    """
    
    def __init__(self):
        """
        Initialize the IT service.
        Creates the it_tickets table if it doesn't exist.
        """
        self.db = DatabaseManager()
        self._create_table()
    
    def _create_table(self):
        """
        Create the it_tickets table if it doesn't exist.
        
        Table Schema:
            - id: Auto-incrementing primary key
            - ticket_id: External ticket identifier
            - priority: Urgency level (Low, Medium, High, Critical)
            - description: Brief description of the issue
            - status: Current ticket state
            - assigned_to: Staff member responsible
            - created_at: When ticket was opened
            - resolution_time_hours: Time to resolve in hours
        """
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER,
                priority TEXT,
                description TEXT,
                status TEXT,
                assigned_to TEXT,
                created_at TEXT,
                resolution_time_hours INTEGER
            )
        """)
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def load_csv(self, path: str):
        """
        Bulk import tickets from a CSV file.
        
        Args:
            path: Path to CSV file with columns:
                  ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
        """
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            self.db.execute(
                "INSERT INTO it_tickets (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours) VALUES (?,?,?,?,?,?,?)",
                (int(row["ticket_id"]), row["priority"], row["description"], row["status"], row["assigned_to"], row["created_at"], int(row["resolution_time_hours"]))
            )
    
    def create_ticket(self, ticket_id: int, priority: str, description: str, status: str, assigned_to: str, created_at: str, resolution_time_hours: int):
        """
        Create a new support ticket.
        
        Args:
            ticket_id: External ticket identifier
            priority: Urgency level (Low, Medium, High, Critical)
            description: Brief description of the issue
            status: Initial status
            assigned_to: Assigned staff member
            created_at: Creation datetime
            resolution_time_hours: Hours to resolve (0 for open tickets)
        """
        self.db.execute(
            "INSERT INTO it_tickets (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours) VALUES (?,?,?,?,?,?,?)",
            (int(ticket_id), priority, description, status, assigned_to, created_at, int(resolution_time_hours))
        )
    
    def update_ticket(self, id: int, ticket_id: int, priority: str, description: str, status: str, assigned_to: str, created_at: str, resolution_time_hours: int):
        """
        Update an existing support ticket.
        
        Args:
            id: Database ID of the ticket to update
            ticket_id: External ticket identifier
            priority: Urgency level
            description: Ticket description
            status: Current status
            assigned_to: Assigned staff member
            created_at: Creation datetime
            resolution_time_hours: Hours to resolve
        """
        self.db.execute(
            "UPDATE it_tickets SET ticket_id=?, priority=?, description=?, status=?, assigned_to=?, created_at=?, resolution_time_hours=? WHERE id=?",
            (int(ticket_id), priority, description, status, assigned_to, created_at, int(resolution_time_hours), id)
        )
    
    def delete_ticket(self, id: int):
        """
        Delete a support ticket by database ID.
        
        Args:
            id: Database ID of the ticket to delete
        """
        self.db.execute("DELETE FROM it_tickets WHERE id=?", (id,))
    
    def all(self):
        """
        Retrieve all tickets ordered by creation date (newest first).
        
        Returns:
            list: All ticket records as sqlite3.Row objects
        """
        return self.db.fetchall("SELECT * FROM it_tickets ORDER BY created_at DESC")
    
    # =========================================================================
    # Metrics and Analytics
    # =========================================================================
    
    def total_count(self):
        """
        Get total number of tickets.
        
        Returns:
            int: Total ticket count
        """
        result = self.db.fetchone("SELECT COUNT(*) as total FROM it_tickets")
        return result["total"] if result else 0
    
    def open_count(self):
        """
        Get count of open/in-progress tickets.
        
        Returns:
            int: Number of tickets with status 'Open' or 'In Progress'
        """
        result = self.db.fetchone(
            "SELECT COUNT(*) as open_count FROM it_tickets WHERE status IN ('Open', 'In Progress')"
        )
        return result["open_count"] if result else 0
    
    def avg_resolution_time(self):
        """
        Get average resolution time in hours.
        
        Returns:
            float: Average resolution hours (rounded to 1 decimal)
        """
        result = self.db.fetchone("SELECT AVG(resolution_time_hours) as avg_res FROM it_tickets")
        return round(result["avg_res"], 1) if result and result["avg_res"] else 0
    
    def priority_counts(self):
        """
        Get ticket counts grouped by priority.
        
        Returns:
            list: Rows with (priority, cnt) columns
        """
        return self.db.fetchall(
            "SELECT priority, COUNT(*) as cnt FROM it_tickets GROUP BY priority"
        )
    
    def status_counts(self):
        """
        Get ticket counts grouped by status.
        
        Returns:
            list: Rows with (status, cnt) columns
        """
        return self.db.fetchall(
            "SELECT status, COUNT(*) as cnt FROM it_tickets GROUP BY status"
        )
    
    def assignee_summary(self):
        """
        Get ticket counts and avg resolution time grouped by assignee.
        
        Returns:
            list: Rows with (assigned_to, ticket_count, avg_resolution) columns
        """
        return self.db.fetchall(
            "SELECT assigned_to, COUNT(*) as ticket_count, AVG(resolution_time_hours) as avg_resolution "
            "FROM it_tickets GROUP BY assigned_to ORDER BY ticket_count DESC"
        )
    
    def slowest_assignee(self):
        """
        Find the assignee with the highest average resolution time.
        
        Returns:
            list: Single row with (assigned_to, avg_res) or empty list
        """
        return self.db.fetchall(
            "SELECT assigned_to, AVG(resolution_time_hours) as avg_res "
            "FROM it_tickets GROUP BY assigned_to ORDER BY avg_res DESC LIMIT 1"
        )
