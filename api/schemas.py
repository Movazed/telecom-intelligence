from pydantic import BaseModel
from typing import List, Optional

class UsageSummary(BaseModel):
    total_calls: int
    total_sms: int
    total_internet_mb: float
    peak_hour: int
    busiest_region: str

class HourlyRecord(BaseModel):
    hour: int
    calls: int
    sms: int
    internet_mb: float

class RegionUsage(BaseModel):
    region: str
    hourly_distribution: List[HourlyRecord]
    trend: List[float]

class PeakUsageRecord(BaseModel):
    hour: Optional[int] = None
    region: Optional[str] = None
    total_usage: float

class PeakTraffic(BaseModel):
    top_hours: List[PeakUsageRecord]
    top_regions: List[PeakUsageRecord]

class PredictionRequest(BaseModel):
    region: str
    avg_usage: float
    growth_rate: float
    variability: float

class PredictionResponse(BaseModel):
    congestion_risk: str
    anomaly_flag: bool
    score: float