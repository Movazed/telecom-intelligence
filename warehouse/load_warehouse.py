import pandas as pd
import sqlite3
import os

def load_data(conn):
    print("Reading Parquet files from data/processed/telecom_usage/...")
    # Read the parquet directory that PySpark generated
    df = pd.read_parquet('data/processed/telecom_usage/')
    
    print("Building Dimension and Fact tables...")
    # 1. Load Region Dimension
    dim_region = df[['grid_id', 'region_name', 'city']].drop_duplicates()
    dim_region = dim_region.rename(columns={'grid_id': 'region_id'})
    dim_region.to_sql('dim_region', conn, if_exists='replace', index=False)

    # 2. Load Time Dimension
    dim_time = df[['timestamp', 'date', 'hour']].drop_duplicates().copy()
    dim_time['day'] = pd.to_datetime(dim_time['date']).dt.day
    dim_time['month'] = pd.to_datetime(dim_time['date']).dt.month
    dim_time['weekday'] = pd.to_datetime(dim_time['date']).dt.day_name()
    dim_time['time_id'] = range(1, len(dim_time) + 1)
    
    dim_time_db = dim_time[['time_id', 'date', 'hour', 'day', 'month', 'weekday']]
    dim_time_db.to_sql('dim_time', conn, if_exists='replace', index=False)

    # 3. Load Fact Table
    fact_usage = df.merge(dim_time[['timestamp', 'time_id']], on='timestamp', how='left')
    fact_usage = fact_usage.rename(columns={'grid_id': 'region_id', 'internet_usage': 'internet_mb'})
    fact_usage = fact_usage[['time_id', 'region_id', 'call_count', 'sms_count', 'internet_mb']]
    fact_usage.to_sql('fact_usage', conn, if_exists='replace', index=True, index_label='usage_id')
    
    print("Warehouse load complete!")

def run_assessment_query(conn):
    """Runs the exact query required by the capstone rubric """
    print("\n--- Running Assessment Query ---")
    query = """
    SELECT r.region_name, t.hour, SUM(f.call_count) AS total_calls
    FROM fact_usage f
    JOIN dim_time t ON f.time_id = t.time_id
    JOIN dim_region r ON f.region_id = r.region_id
    GROUP BY r.region_name, t.hour
    ORDER BY total_calls DESC
    LIMIT 10;
    """
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    print("--------------------------------\n")

if __name__ == "__main__":
    # Create a local SQLite database file to act as our warehouse
    db_path = 'warehouse/telecom_warehouse.db'
    
    # Connect to the DB (it creates the file automatically if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    try:
        load_data(conn)
        run_assessment_query(conn)
        print("✅ Phase 3 Data Engineering Completed Successfully!")
    except Exception as e:
        print(f"Error loading warehouse: {e}")
    finally:
        conn.close()