import os
import pandas as pd

def setup_test_environment():
    # 1. Create the required directory structure
    folders = [
        'data/landing',
        'data/raw',
        'data/rejected',
        'data/processed',
        'warehouse',
        'api/routes'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✔ Folder ready: {folder}")

    # 2. Create 'api/routes/__init__.py' if it doesn't exist
    init_path = 'api/routes/__init__.py'
    if not os.path.exists(init_path):
        with open(init_path, 'a'):
            pass
        print(f"✔ Created: {init_path}")

    # 3. Generate a 'Healthy' CSV File
    healthy_data = {
        'grid_id': [101, 102, 103],
        'timestamp': ['2025-05-01 10:00:00', '2025-05-01 11:00:00', '2025-05-01 12:00:00'],
        'call_count': [50, 60, 45],
        'sms_count': [120, 150, 110],
        'internet_mb': [500.5, 750.2, 420.8],
        'region_name': ['Milan', 'Rome', 'Turin']
    }
    df = pd.DataFrame(healthy_data)
    df.to_csv('data/landing/healthy_batch.csv', index=False)
    print("✔ Generated: data/landing/healthy_batch.csv")

    # 4. Generate a 'Corrupt' CSV File
    with open('data/landing/corrupt_data.csv', 'w') as f:
        f.write("ERROR: This is not a telecom file. Random system logs 12345.")
    print("✔ Generated: data/landing/corrupt_data.csv")

    # 5. Generate an 'Empty' CSV File
    with open('data/landing/empty_file.csv', 'w') as f:
        pass
    print("✔ Generated: data/landing/empty_file.csv")

    print("\n--- Setup Complete ---")
    print("Run: python spark/validate_landing.py")

if __name__ == "__main__":
    setup_test_environment()