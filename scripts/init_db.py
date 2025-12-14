"""
Database Initialization Script
==============================

This script sets up the initial database state for the application.
Run this once before first use to create tables and seed sample data.

Actions Performed:
1. Creates database tables (via service constructors)
2. Creates default admin user (admin/adminpass)
3. Loads sample cybersecurity incidents from CSV
4. Loads sample dataset metadata from CSV
5. Loads sample IT tickets from CSV

Usage:
    python -m scripts.init_db

Default Credentials:
    Username: admin
    Password: adminpass

CSV Files Required:
    - data/cyber_incidents.csv
    - data/datasets_metadata.csv
    - data/it_tickets.csv
"""

from services.auth_manager import AuthManager
from services.security_service import SecurityService
from services.dataset_service import DatasetService
from services.it_service import ITService


def init():
    """
    Initialize the database with schema and sample data.
    
    This function:
    1. Creates all required database tables
    2. Seeds an admin user for initial access
    3. Loads sample data from CSV files
    
    Tables Created:
        - users (via AuthManager)
        - cyber_incidents (via SecurityService)
        - datasets_metadata (via DatasetService)
        - it_tickets (via ITService)
    """
    print("Initializing database...")
    
    # -------------------------------------------------------------------------
    # Create Admin User
    # -------------------------------------------------------------------------
    print("  Creating admin user...")
    auth = AuthManager()
    try:
        auth.register("admin", "adminpass", role="admin")
        print("    ✓ Admin user created")
    except Exception:
        print("    - Admin user already exists (skipped)")
    
    # -------------------------------------------------------------------------
    # Load Cybersecurity Sample Data
    # -------------------------------------------------------------------------
    print("  Loading cybersecurity incidents...")
    security_service = SecurityService()
    try:
        security_service.load_csv("data/cyber_incidents.csv")
        print("    ✓ Incidents loaded from data/cyber_incidents.csv")
    except Exception as e:
        print(f"    ! Error loading incidents: {e}")
    
    # -------------------------------------------------------------------------
    # Load Dataset Metadata Sample Data
    # -------------------------------------------------------------------------
    print("  Loading dataset metadata...")
    dataset_service = DatasetService()
    try:
        dataset_service.load_csv("data/datasets_metadata.csv")
        print("    ✓ Datasets loaded from data/datasets_metadata.csv")
    except Exception as e:
        print(f"    ! Error loading datasets: {e}")
    
    # -------------------------------------------------------------------------
    # Load IT Tickets Sample Data
    # -------------------------------------------------------------------------
    print("  Loading IT tickets...")
    it_service = ITService()
    try:
        it_service.load_csv("data/it_tickets.csv")
        print("    ✓ Tickets loaded from data/it_tickets.csv")
    except Exception as e:
        print(f"    ! Error loading tickets: {e}")
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 50)
    print("Database initialization complete!")
    print("=" * 50)
    print("\nData loaded:")
    print(f"  - Cyber incidents: {security_service.total_count()}")
    print(f"  - Datasets: {dataset_service.total_count()}")
    print(f"  - IT tickets: {it_service.total_count()}")
    print("\nDefault login credentials:")
    print("  Username: admin")
    print("  Password: adminpass")
    print("\nRun the app with: streamlit run Home.py")


if __name__ == "__main__":
    init()
