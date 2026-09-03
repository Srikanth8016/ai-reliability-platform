from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.alert import Alert
from app.models.user import User
from app.repositories.alert_repository import (
    create_alert,
    get_alerts,
)
from app.schemas.alert import (
    AlertCreate,
    AlertResponse,
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=AlertResponse,
    status_code=201,
)
def create_new_alert(
    data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alert = Alert(
        service_id=data.service_id,
        name=data.name,
        message=data.message,
        severity=data.severity,
    )

    return create_alert(db, alert)


@router.get(
    "",
    response_model=list[AlertResponse],
)
def list_alerts(
    service_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_alerts(db, service_id)
