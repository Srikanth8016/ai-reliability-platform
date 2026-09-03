from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.incident_event import IncidentEvent
from app.repositories.incident_repository import (
    add_incident_event,
    create_incident,
    get_incident,
    get_incidents,
    update_incident,
)
from app.schemas.incident import IncidentCreate, IncidentUpdate


def create_new_incident(
    db: Session,
    data: IncidentCreate,
    current_user_id: int,
):

    incident = Incident(
        title=data.title,
        description=data.description,
        severity=data.severity.value,
        status="OPEN",
        service_id=data.service_id,
        created_by=current_user_id,
        started_at=datetime.utcnow(),
    )

    incident = create_incident(db, incident)

    event = IncidentEvent(
        incident_id=incident.id,
        event_type="CREATED",
        message="Incident created",
        created_by=current_user_id,
    )

    add_incident_event(db, event)

    return incident


def list_all_incidents(db: Session):

    return get_incidents(db)


def get_single_incident(
    db: Session,
    incident_id: int,
):

    incident = get_incident(db, incident_id)

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident


def update_existing_incident(
    db: Session,
    incident_id: int,
    data: IncidentUpdate,
    current_user_id: int,
):

    incident = get_incident(db, incident_id)

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    old_status = incident.status

    if data.title is not None:
        incident.title = data.title

    if data.description is not None:
        incident.description = data.description

    if data.severity is not None:
        incident.severity = data.severity.value

    if data.status is not None:

        new_status = data.status.value

        allowed_transitions = {
            "OPEN": ["INVESTIGATING"],
            "INVESTIGATING": ["MITIGATED"],
            "MITIGATED": ["RESOLVED"],
            "RESOLVED": ["CLOSED"],
            "CLOSED": [],
        }

        allowed = allowed_transitions.get(
            old_status,
            [],
        )

        if new_status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid status transition "
                    f"from {old_status} to {new_status}"
                ),
            )

        incident.status = new_status

        if new_status == "RESOLVED":
            incident.resolved_at = datetime.utcnow()

        event = IncidentEvent(
            incident_id=incident.id,
            event_type="STATUS_CHANGED",
            message=(
                f"Status changed from "
                f"{old_status} to {new_status}"
            ),
            created_by=current_user_id,
        )

        add_incident_event(db, event)

    return update_incident(db, incident)
