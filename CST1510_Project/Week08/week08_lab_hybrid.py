import sqlite3
from pathlib import Path
import pandas as pd
import bcrypt

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def connect_database(db_path=DB_PATH):
    return sqlite3.connect(str(db_path))

def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def create_it_tickets_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    if not filepath.exists():
        return 0
    cursor = conn.cursor()
    migrated = 0
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) > 2 else 'user'
                try:
                    cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                   (username, password_hash, role))
                    if cursor.rowcount > 0:
                        migrated += 1
                except Exception as e:
                    print("Error:", e)
    conn.commit()
    return migrated

def load_csv_to_table(conn, csv_path, table_name):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print("CSV not found:", csv_path)
        return 0
    df = pd.read_csv(csv_path)
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    return len(df)

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

def get_all_incidents(conn):
    return pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)

def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    return cursor.rowcount

def setup_database_complete():
    conn = connect_database()
    create_all_tables(conn)
    migrated = migrate_users_from_file(conn)
    # attempt to load CSVs if present
    load_csv_to_table(conn, DATA_DIR / "cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(conn, DATA_DIR / "datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table(conn, DATA_DIR / "it_tickets.csv", "it_tickets")
    conn.close()
    print("Setup complete. Migrated users:", migrated)

if __name__ == '__main__':
    setup_database_complete()
    print("You can now run CRUD or use the DB at:", DB_PATH)
