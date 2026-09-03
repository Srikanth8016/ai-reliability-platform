from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.alert_rule import AlertRule
from app.models.user import User
from app.repositories.alert_rule_repository import (
    create_alert_rule,
    get_alert_rules,
)
from app.schemas.alert_rule import (
    AlertRuleCreate,
    AlertRuleResponse,
)

router = APIRouter(
    prefix="/alert-rules",
    tags=["Alert Rules"],
)


@router.post(
    "",
    response_model=AlertRuleResponse,
    status_code=201,
)
def create_rule(
    data: AlertRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rule = AlertRule(
        service_id=data.service_id,
        metric_name=data.metric_name,
        operator=data.operator,
        threshold=data.threshold,
        severity=data.severity,
    )

    return create_alert_rule(db, rule)


@router.get(
    "",
    response_model=list[AlertRuleResponse],
)
def list_rules(
    service_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_alert_rules(db, service_id)
