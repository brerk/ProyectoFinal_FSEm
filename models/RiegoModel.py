from pydantic import BaseModel
from datetime import datetime


class RiegoConfig(BaseModel):
    time: str  # HH:MM
    duration: int  # Time on
    min_temp: float
    max_temp: float

    timestamp: datetime
