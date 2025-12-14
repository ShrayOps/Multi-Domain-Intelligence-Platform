"""
Dataset Metadata Model
======================

Represents dataset metadata for data governance.

Attributes:
    id (int): Database primary key
    dataset_id (int): External dataset identifier
    name (str): Dataset name
    rows (int): Number of records in dataset
    columns (int): Number of columns/features
    uploaded_by (str): User who uploaded the dataset
    upload_date (str): Upload date (YYYY-MM-DD)
"""


class DatasetMeta:
    """
    Entity representing dataset metadata.
    
    This model mirrors the datasets_metadata database table.
    Used for tracking and governing data assets.
    """
    
    def __init__(self, id: int, dataset_id: int, name: str, rows: int, 
                 columns: int, uploaded_by: str, upload_date: str):
        """
        Initialize a DatasetMeta instance.
        
        Args:
            id: Database primary key
            dataset_id: External dataset identifier
            name: Human-readable dataset name
            rows: Number of records in the dataset
            columns: Number of columns/features
            uploaded_by: User who uploaded the dataset
            upload_date: Date dataset was uploaded (YYYY-MM-DD)
        """
        self.id = id
        self.dataset_id = dataset_id
        self.name = name
        self.rows = rows
        self.columns = columns
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date
    
    def to_dict(self) -> dict:
        """
        Convert DatasetMeta to dictionary representation.
        
        Returns:
            dict: Dataset metadata with all attributes
        """
        return self.__dict__
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"DatasetMeta(id={self.id}, dataset_id={self.dataset_id}, name='{self.name}', rows={self.rows})"
