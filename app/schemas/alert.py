from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    service_id: int
    name: str
    message: str
    severity: str


class AlertResponse(BaseModel):
    id: int
    service_id: int
    name: str
    message: str
    severity: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
