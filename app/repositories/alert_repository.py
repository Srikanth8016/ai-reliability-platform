from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert


def create_alert(
    db: Session,
    alert: Alert,
):
    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_alerts(
    db: Session,
    service_id: int | None = None,
):
    query = select(Alert).order_by(
        Alert.created_at.desc()
    )

    if service_id is not None:
        query = query.where(
            Alert.service_id == service_id
        )

    result = db.execute(query)

    return result.scalars().all()


def get_active_alert(
    db: Session,
    service_id: int,
    name: str,
):
    result = db.execute(
        select(Alert)
        .where(Alert.service_id == service_id)
        .where(Alert.name == name)
        .where(Alert.status == "ACTIVE")
    )

    return result.scalar_one_or_none()
