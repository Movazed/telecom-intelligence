import pandas as pd
import numpy as np

class UsageProcessor:
    def __init__(self):
        self.df = None

    def load_data(self, path):
        """Loads CSV into a DataFrame."""
        print(f"Loading data from {path}...")
        # FIX: Swapped 'timestamp' and 'grid_id' to match your actual dataset structure
        columns = ['timestamp', 'grid_id', 'country_code', 'sms_in', 'sms_out', 'call_in', 'call_out', 'internet']
        
        # Read the csv, forcing low_memory=False
        self.df = pd.read_csv(path, names=columns, low_memory=False)
        return self.df

    def clean_data(self):
        """Cleans timestamps, extracts time features, drops invalid rows, and ensures numeric fields."""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        # 1. Ensure numeric usage fields
        cols_to_convert = ['sms_in', 'sms_out', 'call_in', 'call_out', 'internet']
        for col in cols_to_convert:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Consolidate usage columns 
        self.df['call_count'] = self.df['call_in'] + self.df['call_out']
        self.df['sms_count'] = self.df['sms_in'] + self.df['sms_out']
        self.df['internet_usage'] = self.df['internet']

        # 2. Convert timestamp to datetime
        # Since your data has string dates (e.g., '2013-11-01 00:00:00'), pd.to_datetime parses it automatically
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')

        # 3. Extract hour, day
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['day'] = self.df['timestamp'].dt.day

        # 4. Drop invalid rows
        # Drop rows where timestamp is NaT or grid_id is not a number
        self.df['grid_id'] = pd.to_numeric(self.df['grid_id'], errors='coerce')
        self.df = self.df.dropna(subset=['timestamp', 'grid_id'])

        # Keep only necessary columns
        self.df = self.df[['grid_id', 'timestamp', 'hour', 'day', 'call_count', 'sms_count', 'internet_usage']]
        
        return self.df

    def compute_daily_usage(self):
        """Calculates total usage per day."""
        if self.df is None or 'day' not in self.df.columns:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        daily_usage = self.df.groupby('day')[['call_count', 'sms_count', 'internet_usage']].sum().reset_index()
        return daily_usage

    def compute_kpis(self):
        """Computes key performance indicators."""
        if self.df is None:
            raise ValueError("Data not cleaned. Call clean_data() first.")

        kpis = {}
        
        # Total usage per region 
        region_usage = self.df.groupby('grid_id')['internet_usage'].sum().sort_values(ascending=False)
        kpis['top_regions_internet'] = region_usage.head(5).to_dict()

        # Average usage per hour 
        avg_hourly = self.df.groupby('hour')[['call_count', 'sms_count', 'internet_usage']].mean()
        kpis['avg_hourly_usage'] = avg_hourly.to_dict('index')

        # Peak usage hour (based on internet usage for simplicity) 
        hourly_total = self.df.groupby('hour')['internet_usage'].sum()
        peak_hour = int(hourly_total.idxmax())
        kpis['peak_usage_hour'] = peak_hour

        return kpis


# Task 1.3 Plan API Enrichment (Stub) 
def call_plan_api(customer_id):
    """Simulates calling GET /plans/customer/{id}"""
    mock_response = {
        "customer_id": customer_id,
        "plan_type": "Premium Unlimited",
        "data_limit_gb": 100,
        "status": "Active"
    }
    return mock_response

# --- Quick Test Block ---
if __name__ == "__main__":
    processor = UsageProcessor()
    # Loading the correct relative path
    processor.load_data('data/raw/sms-call-internet-mi-2013-11-01.csv')
    processor.clean_data()
    
    print("\n--- Daily Usage ---")
    print(processor.compute_daily_usage())
    
    print("\n--- KPIs ---")
    kpis = processor.compute_kpis()
    print(f"Peak Hour: {kpis['peak_usage_hour']}")
    print(f"Top 5 Regions (Internet): {list(kpis['top_regions_internet'].keys())}")
    
    print("\n--- API Stub Test ---")
    print(call_plan_api(12345))