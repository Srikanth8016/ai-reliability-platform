from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogCreate(BaseModel):
    service_id: int
    level: str
    message: str


class LogResponse(BaseModel):
    id: int
    service_id: int
    level: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
