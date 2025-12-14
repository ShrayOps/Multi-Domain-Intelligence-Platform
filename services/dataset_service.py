"""
Dataset Service - Data Governance Management
============================================

This module provides data access and business logic for managing
dataset metadata in the platform's data science dashboard.

Features:
- CRUD operations for dataset metadata
- Bulk import from CSV files
- Analytics and metrics
- Resource summaries for governance decisions

Database Table: datasets_metadata
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - dataset_id: INTEGER (external dataset ID)
    - name: TEXT (dataset name)
    - rows: INTEGER (number of records)
    - columns: INTEGER (number of columns/features)
    - uploaded_by: TEXT (user who uploaded)
    - upload_date: TEXT (upload date in YYYY-MM-DD format)

Usage:
    service = DatasetService()
    service.create_dataset(1, "Sales_2025", 50000, 15, "data_scientist", "2025-01-15")
    datasets = service.all()
"""

import pandas as pd
from services.database_manager import DatabaseManager


class DatasetService:
    """
    Service class for managing dataset metadata.
    Supports data governance and storage optimization workflows.
    """
    
    def __init__(self):
        """
        Initialize the dataset service.
        Creates the datasets_metadata table if it doesn't exist.
        """
        self.db = DatabaseManager()
        self._create_table()
    
    def _create_table(self):
        """
        Create the datasets_metadata table if it doesn't exist.
        
        Table Schema:
            - id: Auto-incrementing primary key
            - dataset_id: External dataset identifier
            - name: Human-readable dataset name
            - rows: Number of records in the dataset
            - columns: Number of columns/features
            - uploaded_by: User who uploaded the dataset
            - upload_date: Date dataset was uploaded
        """
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER,
                name TEXT,
                rows INTEGER,
                columns INTEGER,
                uploaded_by TEXT,
                upload_date TEXT
            )
        """)
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def load_csv(self, path: str):
        """
        Bulk import dataset metadata from a CSV file.
        
        Args:
            path: Path to CSV file with columns:
                  dataset_id, name, rows, columns, uploaded_by, upload_date
        """
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            self.db.execute(
                "INSERT INTO datasets_metadata (dataset_id, name, rows, columns, uploaded_by, upload_date) VALUES (?,?,?,?,?,?)",
                (int(row["dataset_id"]), row["name"], int(row["rows"]), int(row["columns"]), row["uploaded_by"], row["upload_date"])
            )
    
    def create_dataset(self, dataset_id: int, name: str, rows: int, columns: int, uploaded_by: str, upload_date: str):
        """
        Create a new dataset metadata entry.
        
        Args:
            dataset_id: External dataset identifier
            name: Dataset name
            rows: Number of records
            columns: Number of columns/features
            uploaded_by: User who uploaded
            upload_date: Upload date (YYYY-MM-DD format)
        """
        self.db.execute(
            "INSERT INTO datasets_metadata (dataset_id, name, rows, columns, uploaded_by, upload_date) VALUES (?,?,?,?,?,?)",
            (int(dataset_id), name, int(rows), int(columns), uploaded_by, upload_date)
        )
    
    def update_dataset(self, id: int, dataset_id: int, name: str, rows: int, columns: int, uploaded_by: str, upload_date: str):
        """
        Update an existing dataset metadata entry.
        
        Args:
            id: Database ID of the dataset to update
            dataset_id: External dataset identifier
            name: Dataset name
            rows: Number of records
            columns: Number of columns/features
            uploaded_by: User who uploaded
            upload_date: Upload date
        """
        self.db.execute(
            "UPDATE datasets_metadata SET dataset_id=?, name=?, rows=?, columns=?, uploaded_by=?, upload_date=? WHERE id=?",
            (int(dataset_id), name, int(rows), int(columns), uploaded_by, upload_date, id)
        )
    
    def delete_dataset(self, id: int):
        """
        Delete a dataset metadata entry by database ID.
        
        Args:
            id: Database ID of the dataset to delete
        """
        self.db.execute("DELETE FROM datasets_metadata WHERE id=?", (id,))
    
    def all(self):
        """
        Retrieve all datasets ordered by upload date (newest first).
        
        Returns:
            list: All dataset records as sqlite3.Row objects
        """
        return self.db.fetchall("SELECT * FROM datasets_metadata ORDER BY upload_date DESC")
    
    # =========================================================================
    # Metrics and Analytics
    # =========================================================================
    
    def total_count(self):
        """
        Get total number of datasets.
        
        Returns:
            int: Total dataset count
        """
        result = self.db.fetchone("SELECT COUNT(*) as total FROM datasets_metadata")
        return result["total"] if result else 0
    
    def total_rows(self):
        """
        Get total number of rows across all datasets.
        
        Returns:
            int: Sum of all dataset row counts
        """
        result = self.db.fetchone("SELECT SUM(rows) as total_rows FROM datasets_metadata")
        return result["total_rows"] if result and result["total_rows"] else 0
    
    def uploader_summary(self):
        """
        Get aggregated metrics grouped by uploader.
        
        Returns:
            list: Rows with (uploaded_by, dataset_count, total_rows) columns
        """
        return self.db.fetchall(
            "SELECT uploaded_by, COUNT(*) as dataset_count, SUM(rows) as total_rows "
            "FROM datasets_metadata GROUP BY uploaded_by"
        )
