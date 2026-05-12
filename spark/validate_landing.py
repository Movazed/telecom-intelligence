import os
import shutil
import pandas as pd

# Define paths based on project structure
LANDING_DIR = "data/landing/"
RAW_DIR = "data/raw/"
REJECTED_DIR = "data/rejected/"

def validate_files():
    """
    Scans the landing zone, validates CSV integrity, and moves files 
    to 'raw' for processing or 'rejected' for quarantine.
    """
    # 1. Ensure the destination directories exist
    for directory in [RAW_DIR, REJECTED_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    # 2. Get list of files in the landing zone
    files = [f for f in os.listdir(LANDING_DIR) if os.path.isfile(os.path.join(LANDING_DIR, f))]
    
    if not files:
        print("No new files found in the landing zone.")
        return

    print(f"Starting validation for {len(files)} files...")

    for file_name in files:
        landing_path = os.path.join(LANDING_DIR, file_name)
        
        # Skip hidden files
        if file_name.startswith('.'):
            continue

        try:
            # --- TASK 3.6: FAILURE HANDLING LOGIC ---
            
            # Check 1: File Extension
            if not file_name.lower().endswith('.csv'):
                raise ValueError("Unsupported file format (only .csv allowed)")

            # Check 2: Schema Integrity & Corruption
            # We read only the first 5 rows to be efficient while checking for structure
            pd.read_csv(landing_path, nrows=5)

            # Check 3: Check if file is empty
            if os.path.getsize(landing_path) == 0:
                raise ValueError("File is empty (0 bytes)")

            # If all checks pass, move to RAW
            dest_path = os.path.join(RAW_DIR, file_name)
            shutil.move(landing_path, dest_path)
            print(f"PASSED: {file_name} -> Moved to {RAW_DIR}")

        except Exception as e:
            # If any check fails, move to REJECTED (Quarantine)
            dest_path = os.path.join(REJECTED_DIR, file_name)
            shutil.move(landing_path, dest_path)
            print(f"REJECTED: {file_name} -> Moved to {REJECTED_DIR} | Reason: {e}")

if __name__ == "__main__":
    validate_files()