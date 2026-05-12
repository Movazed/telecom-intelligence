import sqlite3
import os

# --- ABSOLUTE PATH FIX ---
# Finds the 'api' directory, goes up one level to the project root, and points to warehouse
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'warehouse', 'telecom_warehouse.db')

def get_db_connection():
    """Establishes a connection to the SQLite Star Schema"""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at: {DB_PATH}. Please run the Spark pipeline first.")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn