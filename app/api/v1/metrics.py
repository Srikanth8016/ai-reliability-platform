from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.metric import Metric
from app.models.user import User
from app.queue.jobs import enqueue_job
from app.repositories.metric_repository import (
    create_metric,
    get_metrics,
)
from app.schemas.metric import (
    MetricCreate,
    MetricResponse,
)

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

    job = enqueue_job(
        "PROCESS_METRIC",
        {
            "metric_id": metric.id,
        },
    )

    print(
        f"Queued metric #{metric.id} "
        f"as job {job['id']}"
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
