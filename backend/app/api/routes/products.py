from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.db.enums import ProductStageStatus
from app.db.models import ProductStaging
from app.schemas.product import ProductStagingRead

router = APIRouter()


@router.get("/staging", response_model=list[ProductStagingRead])
def list_staged_products(db: Session = Depends(db_session)) -> list[ProductStaging]:
    return db.query(ProductStaging).order_by(ProductStaging.id.desc()).limit(200).all()


@router.post("/staging/{product_id}/approve", response_model=ProductStagingRead)
def approve_product(product_id: int, db: Session = Depends(db_session)) -> ProductStaging:
    product = db.get(ProductStaging, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stage_status = ProductStageStatus.APPROVED
    db.commit()
    db.refresh(product)
    return product


@router.post("/staging/{product_id}/reject", response_model=ProductStagingRead)
def reject_product(product_id: int, db: Session = Depends(db_session)) -> ProductStaging:
    product = db.get(ProductStaging, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stage_status = ProductStageStatus.REJECTED
    db.commit()
    db.refresh(product)
    return product
