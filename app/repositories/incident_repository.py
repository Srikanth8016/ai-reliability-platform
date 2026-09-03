from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.incident_event import IncidentEvent


def create_incident(
    db: Session,
    incident: Incident,
) -> Incident:

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incidents(db: Session):

    result = db.execute(
        select(Incident).order_by(
            Incident.created_at.desc()
        )
    )

    return result.scalars().all()


def get_incident(
    db: Session,
    incident_id: int,
):

    result = db.execute(
        select(Incident).where(
            Incident.id == incident_id
        )
    )

    return result.scalar_one_or_none()


def get_active_incident_for_service(
    db: Session,
    service_id: int,
):
    result = db.execute(
        select(Incident)
        .where(Incident.service_id == service_id)
        .where(
            Incident.status.in_(
                [
                    "OPEN",
                    "INVESTIGATING",
                    "MITIGATED",
                ]
            )
        )
        .order_by(Incident.created_at.desc())
    )

    return result.scalars().first()


def update_incident(
    db: Session,
    incident: Incident,
):

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def add_incident_event(
    db: Session,
    event: IncidentEvent,
):

    db.add(event)
    db.commit()
    db.refresh(event)

    return event
