
from pydantic import BaseModel
from datetime import date

class MetricsResponse(BaseModel):
    date: date
    avg_length_of_stay: float
    admission_count: int
