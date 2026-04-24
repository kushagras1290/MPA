from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.db.enums import ProductStageStatus
from app.db.models import AttributeMapping, ProductStaging
from app.schemas.magento import MagentoPushResponse
from app.services.magento_client import MagentoApiError, MagentoClient
from app.services.magento_mapper import MagentoApiPayloadMapper

router = APIRouter()


@router.post("/products/{product_id}/push-draft", response_model=MagentoPushResponse)
async def push_product_draft(product_id: int, db: Session = Depends(db_session)) -> MagentoPushResponse:
    product = db.get(ProductStaging, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    mappings = db.query(AttributeMapping).filter(AttributeMapping.is_active.is_(True)).all()
    option_map = {
        (mapping.attribute_code, mapping.human_value): mapping.magento_option_id
        for mapping in mappings
    }

    payload = MagentoApiPayloadMapper(option_mappings=option_map).to_payload(product.generated_payload)
    payload["product"]["status"] = 2  # Always draft/disabled from automation.

    try:
        response = await MagentoClient().create_or_update_product(payload)
    except MagentoApiError as exc:
        product.stage_status = ProductStageStatus.UPLOAD_FAILED
        db.commit()
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    product.magento_product_id = str(response.get("id") or "")
    product.magento_sku = product.sku
    product.stage_status = ProductStageStatus.MAGENTO_DRAFT_CREATED
    db.commit()

    return MagentoPushResponse(
        product_id=product.magento_product_id,
        sku=product.sku,
        status="magento_draft_created",
        message="Product pushed to Magento as disabled/draft.",
    )
