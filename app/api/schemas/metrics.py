from datetime import date

from pydantic import BaseModel


class MetricsResponse(BaseModel):
    date: date
    avg_length_of_stay: float
    admission_count: int
