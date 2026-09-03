from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.metric import Metric


def create_metric(
    db: Session,
    metric: Metric,
):
    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric


def get_metrics(
    db: Session,
    service_id: int | None = None,
):
    query = select(Metric).order_by(
        Metric.timestamp.desc()
    )

    if service_id is not None:
        query = query.where(
            Metric.service_id == service_id
        )

    result = db.execute(query)

    return result.scalars().all()
