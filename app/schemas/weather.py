from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WeatherRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    location: str
    temperature: float
    feels_like: float | None
    humidity: int | None
    pressure: int | None
    wind_speed: float | None
    description: str | None
