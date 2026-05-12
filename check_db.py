import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('warehouse/telecom_warehouse.db')

# Print the columns in the fact_usage table
df = pd.read_sql_query("SELECT * FROM fact_usage LIMIT 1", conn)
print("ACTUAL COLUMNS IN DATABASE:")
print(df.columns.tolist())

conn.close()