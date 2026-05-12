from fastapi import APIRouter, HTTPException
import pandas as pd
from api.database import get_db_connection
from api.schemas import UsageSummary, RegionUsage, PeakTraffic

router = APIRouter()

@router.get("/summary", response_model=UsageSummary)
def get_usage_summary():
    conn = get_db_connection()
    try:
        totals = conn.execute("SELECT SUM(call_count) as total_calls, SUM(sms_count) as total_sms, SUM(internet_mb) as total_internet FROM fact_usage").fetchone()
        peak_hour = conn.execute("SELECT time_id as hour FROM fact_usage GROUP BY time_id ORDER BY SUM(internet_mb) DESC LIMIT 1").fetchone()
        busiest = conn.execute("SELECT region_id as region_name FROM fact_usage GROUP BY region_id ORDER BY SUM(internet_mb) DESC LIMIT 1").fetchone()
        
        if not totals or totals['total_calls'] is None:
            return {
                "total_calls": 0, "total_sms": 0, "total_internet_mb": 0.0,
                "peak_hour": 0, "busiest_region": "N/A"
            }

        return {
            "total_calls": int(totals['total_calls'] or 0),
            "total_sms": int(totals['total_sms'] or 0),
            "total_internet_mb": float(totals['total_internet'] or 0.0),
            "peak_hour": int(peak_hour['hour']) if peak_hour else 0,
            # Wrap in str() to satisfy Pydantic string requirement
            "busiest_region": str(busiest['region_name']) if busiest else "N/A"
        }
    finally:
        conn.close()

@router.get("/region/{region}", response_model=RegionUsage)
def get_region_usage(region: str):
    conn = get_db_connection()
    try:
        query = """
            SELECT time_id as hour, SUM(call_count) as calls, SUM(sms_count) as sms, SUM(internet_mb) as internet_mb 
            FROM fact_usage 
            WHERE region_id = ? 
            GROUP BY time_id ORDER BY time_id
        """
        # We pass 'region' which comes in from the URL. 
        # If the URL is /region/5161, it works perfectly.
        df = pd.read_sql_query(query, conn, params=(region,))
        
        if df.empty or df['calls'].isnull().all():
            raise HTTPException(status_code=404, detail="Region not found")
            
        return {
            "region": str(region), 
            "hourly_distribution": df.to_dict(orient='records'), 
            "trend": df['internet_mb'].fillna(0).tolist()
        }
    finally:
        conn.close()

@router.get("/peak", response_model=PeakTraffic)
def get_peak_traffic():
    conn = get_db_connection()
    try:
        hours = pd.read_sql_query("SELECT time_id as hour, SUM(internet_mb) as total_usage FROM fact_usage GROUP BY time_id ORDER BY total_usage DESC LIMIT 5", conn)
        regions = pd.read_sql_query("SELECT region_id as region, SUM(internet_mb) as total_usage FROM fact_usage GROUP BY region_id ORDER BY total_usage DESC LIMIT 5", conn)
        
        # Convert the 'region' column to strings so Pydantic doesn't crash on the integers
        regions['region'] = regions['region'].astype(str)
        
        return {
            "top_hours": hours.to_dict(orient='records'), 
            "top_regions": regions.to_dict(orient='records')
        }
    finally:
        conn.close()