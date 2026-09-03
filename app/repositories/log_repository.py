from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.log import Log


def create_log(
    db: Session,
    log: Log,
):
    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_logs(
    db: Session,
    service_id: int | None = None,
):
    query = select(Log).order_by(
        Log.timestamp.desc()
    )

    if service_id is not None:
        query = query.where(
            Log.service_id == service_id
        )

    result = db.execute(query)

    return result.scalars().all()
