from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class IncidentSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: IncidentSeverity
    service_id: int


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    service_id: int
    created_by: int
    started_at: datetime
    resolved_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
