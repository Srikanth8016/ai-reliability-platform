from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    team_id: int


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    team_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
