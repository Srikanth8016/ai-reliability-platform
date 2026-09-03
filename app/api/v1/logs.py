from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.log import Log
from app.models.user import User
from app.repositories.log_repository import (
    create_log,
    get_logs,
)
from app.schemas.log import LogCreate, LogResponse

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.post(
    "",
    response_model=LogResponse,
    status_code=201,
)
def create_new_log(
    data: LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = Log(
        service_id=data.service_id,
        level=data.level,
        message=data.message,
    )

    return create_log(db, log)


@router.get(
    "",
    response_model=list[LogResponse],
)
def list_logs(
    service_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_logs(db, service_id)
