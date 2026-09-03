from datetime import datetime

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.incident import Incident
from app.models.incident_event import IncidentEvent
from app.repositories.incident_repository import (
    get_active_incident_for_service,
)


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
    db.flush()

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

    db.commit()
    db.refresh(incident)

    return incident
