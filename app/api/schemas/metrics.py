"""Pydantic schema for representing operational metrics response."""
from datetime import date
from pydantic import BaseModel


class MetricsResponse(BaseModel):
    """Response model containing aggregated operational metrics for a specific date."""

    date: date
    avg_length_of_stay: float
    admission_count: int
