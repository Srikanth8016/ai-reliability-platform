from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)
from app.services.incident_service import (
    create_new_incident,
    get_single_incident,
    list_all_incidents,
    update_existing_incident,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return create_new_incident(
        db,
        data,
        current_user.id,
    )


@router.get(
    "",
    response_model=list[IncidentResponse],
)
def get_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return list_all_incidents(db)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return get_single_incident(
        db,
        incident_id,
    )


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def update_incident(
    incident_id: int,
    data: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return update_existing_incident(
        db,
        incident_id,
        data,
        current_user.id,
    )
