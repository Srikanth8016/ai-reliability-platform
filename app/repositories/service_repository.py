from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate


def create_service(
    db: Session,
    service_data: ServiceCreate,
) -> Service:
    service = Service(
        name=service_data.name,
        description=service_data.description,
        team_id=service_data.team_id,
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


def get_services(db: Session) -> list[Service]:
    statement = select(Service)

    result = db.execute(statement)

    return list(result.scalars().all())


def get_service(
    db: Session,
    service_id: int,
) -> Service | None:
    statement = select(Service).where(
        Service.id == service_id
    )

    result = db.execute(statement)

    return result.scalar_one_or_none()
