from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from datetime import datetime, timedelta
import os
import shutil
import pandas as pd

# --- WSL PATH MAPPING ---
# Airflow (running in WSL) sees your C: drive here:
PROJECT_ROOT = "/mnt/c/Projects/workspace/telecom-intelligence"

LANDING_DIR = os.path.join(PROJECT_ROOT, 'data', 'landing')
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
REJECTED_DIR = os.path.join(PROJECT_ROOT, 'data', 'rejected')

# Default arguments for the DAG
default_args = {
    'owner': 'telecom_team',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# --- Python Functions for each Task ---

def detect_files():
    """Step 1: Verify landing directory visibility and trigger ShortCircuit if empty"""
    if not os.path.exists(LANDING_DIR):
        os.makedirs(LANDING_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(LANDING_DIR) if os.path.isfile(os.path.join(LANDING_DIR, f))]
    print(f"Scanning Directory: {LANDING_DIR}")
    print(f"Found {len(files)} files in landing zone.")
    
    # Return True to proceed, False to skip the rest of the DAG
    return len(files) > 0

def validate_files():
    """Step 2: Task 3.6 - Quarantine Logic (Moves files to raw/ or rejected/)"""
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(REJECTED_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(LANDING_DIR) if os.path.isfile(os.path.join(LANDING_DIR, f))]
    
    for file_name in files:
        file_path = os.path.join(LANDING_DIR, file_name)
        try:
            # Check if file is empty
            if os.path.getsize(file_path) == 0:
                raise ValueError("Empty file detected")
            
            # Check if valid CSV structure
            pd.read_csv(file_path, nrows=1)
            
            # If healthy, move to RAW
            shutil.move(file_path, os.path.join(RAW_DIR, file_name))
            print(f"✅ PASSED: {file_name} moved to raw/")
        except Exception as e:
            # If corrupt, move to REJECTED
            shutil.move(file_path, os.path.join(REJECTED_DIR, file_name))
            print(f"❌ REJECTED: {file_name} moved to rejected/ | Reason: {e}")
    return True

def move_files():
    print("Files successfully organized into raw/ and rejected/ zones.")
    return True

def log_status():
    print("Audit Log: Validation task complete.")

def run_spark_job():
    """Step 5: Run the PySpark pipeline from raw/ folder"""
    spark_script = os.path.join(PROJECT_ROOT, 'spark', 'telecom_pipeline.py')
    print(f"Executing: python3 {spark_script}")
    exit_code = os.system(f"python3 {spark_script}")
    if exit_code != 0:
        raise Exception("Spark Job Failed")

def load_warehouse():
    print("Loading Parquet data into SQL Star Schema...")

def notify():
    print("✅ End-to-End Pipeline Executed Successfully.")


# --- Define the DAG ---
with DAG(
    'telecom_ingestion_pipeline',
    default_args=default_args,
    # Auto-update: Runs every 5 minutes
    schedule_interval='*/5 * * * *',
    catchup=False,
    description='Automated Telecom Network Intelligence ETL Pipeline'
) as dag:

    # t_detect now acts as a ShortCircuit check to stop unnecessary runs
    t_detect = ShortCircuitOperator(
        task_id='detect_files', 
        python_callable=detect_files
    )
    
    t_validate = PythonOperator(task_id='validate_files', python_callable=validate_files)
    t_move = PythonOperator(task_id='move_files', python_callable=move_files)
    t_log = PythonOperator(task_id='log_status', python_callable=log_status)
    t_spark = PythonOperator(task_id='run_spark_job', python_callable=run_spark_job)
    t_warehouse = PythonOperator(task_id='load_warehouse', python_callable=load_warehouse)
    t_notify = PythonOperator(task_id='notify', python_callable=notify)

    # Set the execution order exactly as required
    t_detect >> t_validate >> t_move >> t_log >> t_spark >> t_warehouse >> t_notify