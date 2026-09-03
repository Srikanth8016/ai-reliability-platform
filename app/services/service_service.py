from sqlalchemy.orm import Session

from app.repositories import service_repository
from app.schemas.service import ServiceCreate


def create_service(
    db: Session,
    service_data: ServiceCreate,
):
    return service_repository.create_service(
        db,
        service_data,
    )


def get_services(db: Session):
    return service_repository.get_services(db)


def get_service(
    db: Session,
    service_id: int,
):
    return service_repository.get_service(
        db,
        service_id,
    )
