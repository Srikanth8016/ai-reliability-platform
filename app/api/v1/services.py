from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service import ServiceCreate, ServiceResponse
from app.services import service_service

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
):
    return service_service.create_service(
        db,
        service_data,
    )


@router.get(
    "",
    response_model=list[ServiceResponse],
)
def get_services(
    db: Session = Depends(get_db),
):
    return service_service.get_services(db)


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    service = service_service.get_service(
        db,
        service_id,
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    return service
