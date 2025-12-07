from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class WeatherSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    location: str
    temperature: float
    feels_like: Optional[float] = None
    humidity: Optional[int] = None
    pressure: Optional[int] = None
    wind_speed: Optional[float] = None
    description: Optional[str] = None
