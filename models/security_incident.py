"""
Security Incident Model
=======================

Represents a cybersecurity incident in the system.

Attributes:
    id (int): Database primary key
    incident_id (int): External incident identifier
    timestamp (str): Incident datetime
    severity (str): Impact level (Low, Medium, High, Critical)
    category (str): Type of incident
    status (str): Current state (Open, In Progress, Resolved, Closed)
    description (str): Incident details
"""


class SecurityIncident:
    """
    Entity representing a cybersecurity incident.
    
    This model mirrors the cyber_incidents database table.
    """
    
    def __init__(self, id: int, incident_id: int, timestamp: str, severity: str, 
                 category: str, status: str, description: str):
        """
        Initialize a SecurityIncident instance.
        
        Args:
            id: Database primary key
            incident_id: External incident identifier
            timestamp: Incident datetime
            severity: Impact level (Low, Medium, High, Critical)
            category: Type of incident (Phishing, Malware, DDoS, etc.)
            status: Current state (Open, In Progress, Resolved, Closed)
            description: Details about the incident
        """
        self.id = id
        self.incident_id = incident_id
        self.timestamp = timestamp
        self.severity = severity
        self.category = category
        self.status = status
        self.description = description
    
    def to_dict(self) -> dict:
        """
        Convert SecurityIncident to dictionary representation.
        
        Returns:
            dict: Incident data with all attributes
        """
        return {
            "id": self.id,
            "incident_id": self.incident_id,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "category": self.category,
            "status": self.status,
            "description": self.description
        }
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"SecurityIncident(id={self.id}, incident_id={self.incident_id}, category='{self.category}', status='{self.status}')"
