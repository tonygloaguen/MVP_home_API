from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    weather_api_key: str = Field(..., env="WEATHER_API_KEY")
    latitude: float = Field(48.8566, env="LATITUDE")
    longitude: float = Field(2.3522, env="LONGITUDE")
    location_name: str = Field("Paris", env="LOCATION_NAME")

    weather_ttl_minutes: int = Field(30, env="WEATHER_TTL_MINUTES")
    ephemerides_ttl_hours: int = Field(6, env="EPHEMERIDES_TTL_HOURS")

    database_url: str = Field("sqlite:///./homedash.db", env="DATABASE_URL")

    # --- NEWS / RSS ---
    news_rss_url: str = Field(
        "https://www.francetvinfo.fr/titres.rss", env="NEWS_RSS_URL"
    )
    news_ttl_minutes: int = Field(30, env="NEWS_TTL_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
