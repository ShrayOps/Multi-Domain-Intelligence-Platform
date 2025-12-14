"""
Security Service - Cybersecurity Incident Management
====================================================

This module provides data access and business logic for managing
cybersecurity incidents in the platform.

Features:
- CRUD operations for security incidents
- Bulk import from CSV files
- Analytics queries (counts, averages, groupings)
- Metrics for dashboard display

Database Table: cyber_incidents
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - incident_id: INTEGER (external incident ID)
    - timestamp: TEXT (incident datetime)
    - severity: TEXT (Low, Medium, High, Critical)
    - category: TEXT (Phishing, Malware, DDoS, Unauthorized Access, Misconfiguration)
    - status: TEXT (Open, In Progress, Resolved, Closed)
    - description: TEXT (incident description)

Usage:
    service = SecurityService()
    service.create_incident(1001, "2024-01-15 10:00:00", "High", "Phishing", "Open", "Description")
    incidents = service.all()
"""

import pandas as pd
from services.database_manager import DatabaseManager


class SecurityService:
    """
    Service class for managing cybersecurity incidents.
    Provides CRUD operations and analytical queries.
    """
    
    def __init__(self):
        """
        Initialize the security service.
        Creates the cyber_incidents table if it doesn't exist.
        """
        self.db = DatabaseManager()
        self._create_table()
    
    def _create_table(self):
        """
        Create the cyber_incidents table if it doesn't exist.
        
        Table Schema:
            - id: Auto-incrementing primary key
            - incident_id: External incident identifier
            - timestamp: When the incident occurred
            - severity: Impact level (Low, Medium, High, Critical)
            - category: Type of incident
            - status: Current state (Open, In Progress, Resolved, Closed)
            - description: Details about the incident
        """
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id INTEGER,
                timestamp TEXT,
                severity TEXT,
                category TEXT,
                status TEXT,
                description TEXT
            )
        """)
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def load_csv(self, path: str):
        """
        Bulk import incidents from a CSV file.
        
        Args:
            path: Path to CSV file with columns:
                  incident_id, timestamp, severity, category, status, description
        """
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            self.db.execute(
                "INSERT INTO cyber_incidents (incident_id, timestamp, severity, category, status, description) VALUES (?,?,?,?,?,?)",
                (int(row["incident_id"]), row["timestamp"], row["severity"], row["category"], row["status"], row["description"])
            )
    
    def create_incident(self, incident_id: int, timestamp: str, severity: str, category: str, status: str, description: str):
        """
        Create a new security incident.
        
        Args:
            incident_id: External incident identifier
            timestamp: Incident datetime
            severity: Impact level (Low, Medium, High, Critical)
            category: Incident type
            status: Current state
            description: Incident details
        """
        self.db.execute(
            "INSERT INTO cyber_incidents (incident_id, timestamp, severity, category, status, description) VALUES (?,?,?,?,?,?)",
            (int(incident_id), timestamp, severity, category, status, description)
        )
    
    def update_incident(self, id: int, incident_id: int, timestamp: str, severity: str, category: str, status: str, description: str):
        """
        Update an existing security incident.
        
        Args:
            id: Database ID of the incident to update
            incident_id: External incident identifier
            timestamp: Incident datetime
            severity: Impact level
            category: Incident type
            status: Current state
            description: Incident details
        """
        self.db.execute(
            "UPDATE cyber_incidents SET incident_id=?, timestamp=?, severity=?, category=?, status=?, description=? WHERE id=?",
            (int(incident_id), timestamp, severity, category, status, description, id)
        )
    
    def delete_incident(self, id: int):
        """
        Delete a security incident by database ID.
        
        Args:
            id: Database ID of the incident to delete
        """
        self.db.execute("DELETE FROM cyber_incidents WHERE id=?", (id,))
    
    def all(self):
        """
        Retrieve all incidents ordered by timestamp (newest first).
        
        Returns:
            list: All incident records as sqlite3.Row objects
        """
        return self.db.fetchall("SELECT * FROM cyber_incidents ORDER BY timestamp DESC")
    
    # =========================================================================
    # Metrics and Analytics
    # =========================================================================
    
    def total_count(self):
        """
        Get total number of incidents.
        
        Returns:
            int: Total incident count
        """
        result = self.db.fetchone("SELECT COUNT(*) as total FROM cyber_incidents")
        return result["total"] if result else 0
    
    def open_count(self):
        """
        Get count of open/unresolved incidents.
        
        Returns:
            int: Count of incidents with status 'Open' or 'In Progress'
        """
        result = self.db.fetchone(
            "SELECT COUNT(*) as open_count FROM cyber_incidents WHERE status IN ('Open', 'In Progress')"
        )
        return result["open_count"] if result else 0
    
    def category_counts(self):
        """
        Get incident counts grouped by category.
        
        Returns:
            list: Rows with (category, cnt) columns
        """
        return self.db.fetchall(
            "SELECT category, COUNT(*) as cnt FROM cyber_incidents GROUP BY category"
        )
    
    def severity_counts(self):
        """
        Get incident counts grouped by severity.
        
        Returns:
            list: Rows with (severity, cnt) columns
        """
        return self.db.fetchall(
            "SELECT severity, COUNT(*) as cnt FROM cyber_incidents GROUP BY severity"
        )
    
    def status_counts(self):
        """
        Get incident counts grouped by status.
        
        Returns:
            list: Rows with (status, cnt) columns
        """
        return self.db.fetchall(
            "SELECT status, COUNT(*) as cnt FROM cyber_incidents GROUP BY status"
        )
