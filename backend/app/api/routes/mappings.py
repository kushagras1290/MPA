from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.db.models import AttributeMapping
from app.schemas.mapping import AttributeMappingCreate, AttributeMappingRead

router = APIRouter()


@router.get("", response_model=list[AttributeMappingRead])
def list_mappings(db: Session = Depends(db_session)) -> list[AttributeMapping]:
    return (
        db.query(AttributeMapping)
        .order_by(AttributeMapping.attribute_code, AttributeMapping.human_value)
        .all()
    )


@router.post("", response_model=AttributeMappingRead)
def create_mapping(
    payload: AttributeMappingCreate, db: Session = Depends(db_session)
) -> AttributeMapping:
    mapping = AttributeMapping(**payload.model_dump())
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    return mapping
