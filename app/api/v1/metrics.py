from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.metric import Metric
from app.models.user import User
from app.repositories.alert_rule_repository import get_alert_rules
from app.repositories.metric_repository import (
    create_metric,
    get_metrics,
)
from app.schemas.metric import (
    MetricCreate,
    MetricResponse,
)
from app.services.alert_engine import evaluate_alert_rule

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.post(
    "",
    response_model=MetricResponse,
    status_code=201,
)
def create_new_metric(
    data: MetricCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    metric = Metric(
        service_id=data.service_id,
        name=data.name,
        value=data.value,
    )

    metric = create_metric(db, metric)

    rules = get_alert_rules(
        db,
        service_id=data.service_id,
    )

    for rule in rules:

        if rule.metric_name != data.name:
            continue

        evaluate_alert_rule(
            db,
            rule,
            data.value,
        )

    return metric


@router.get(
    "",
    response_model=list[MetricResponse],
)
def list_metrics(
    service_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_metrics(db, service_id)
