from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert_rule import AlertRule


def create_alert_rule(
    db: Session,
    rule: AlertRule,
):
    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


def get_alert_rules(
    db: Session,
    service_id: int | None = None,
):
    query = select(AlertRule).where(
        AlertRule.enabled.is_(True)
    )

    if service_id is not None:
        query = query.where(
            AlertRule.service_id == service_id
        )

    result = db.execute(query)

    return result.scalars().all()
