from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertRuleCreate(BaseModel):
    service_id: int
    metric_name: str
    operator: str
    threshold: float
    severity: str


class AlertRuleResponse(BaseModel):
    id: int
    service_id: int
    metric_name: str
    operator: str
    threshold: float
    severity: str
    enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
