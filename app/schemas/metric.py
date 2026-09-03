from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MetricCreate(BaseModel):
    service_id: int
    name: str
    value: float


class MetricResponse(BaseModel):
    id: int
    service_id: int
    name: str
    value: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
