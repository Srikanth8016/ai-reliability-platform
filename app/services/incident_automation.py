from datetime import datetime

from sqlalchemy.orm import Session

from app.core.events import publish_event
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.incident_event import IncidentEvent
from app.repositories.incident_repository import (
    get_active_incident_for_service,
)
from app.repositories.outbox_repository import create_outbox_event


def create_incident_from_alert(
    db: Session,
    alert: Alert,
):
    existing_incident = (
        get_active_incident_for_service(
            db,
            alert.service_id,
        )
    )

    if existing_incident:

        event = IncidentEvent(
            incident_id=existing_incident.id,
            event_type="ALERT_CORRELATED",
            message=(
                f"Alert #{alert.id} correlated "
                f"with existing incident "
                f"#{existing_incident.id}"
            ),
            created_by=1,
        )

        db.add(event)
        db.commit()

        return existing_incident

    incident = Incident(
        title=alert.name,
        description=alert.message,
        severity=alert.severity,
        status="OPEN",
        service_id=alert.service_id,
        created_by=1,
        started_at=datetime.utcnow(),
    )

    db.add(incident)
    db.flush()  # get incident.id without committing

    event = IncidentEvent(
        incident_id=incident.id,
        event_type="ALERT_TRIGGERED",
        message=(
            f"Incident automatically created "
            f"from alert #{alert.id}"
        ),
        created_by=1,
    )

    db.add(event)

    # Write outbox event in the SAME transaction — atomic with the incident
    create_outbox_event(
        db=db,
        event_type="INCIDENT_CREATED",
        payload={
            "incident_id": incident.id,
            "service_id": incident.service_id,
            "severity": incident.severity,
            "status": incident.status,
        },
    )

    db.commit()
    db.refresh(incident)

    # Pub/Sub for immediate live notification (best-effort, not durable)
    publish_event(
        "INCIDENT_CREATED",
        {
            "incident_id": incident.id,
            "service_id": incident.service_id,
            "severity": incident.severity,
            "status": incident.status,
        },
    )

    return incident
