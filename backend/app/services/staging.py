from typing import Any

from sqlalchemy.orm import Session

from app.db.enums import BatchStatus, ProductStageStatus
from app.db.models import ProductStaging, UploadBatch
from app.services.field_generation import generate_fields


class StagingService:
    def create_batch(self, db: Session, file_name: str | None, total_rows: int) -> UploadBatch:
        batch = UploadBatch(
            original_file_name=file_name,
            total_rows=total_rows,
            source_type="excel",
            status=BatchStatus.CREATED,
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    def stage_products(self, db: Session, batch: UploadBatch, products: list[dict[str, Any]]) -> list[ProductStaging]:
        staged: list[ProductStaging] = []
        for product in products:
            enriched = generate_fields(product)
            model = ProductStaging(
                batch_id=batch.id,
                sku=str(enriched["sku"]),
                name=str(enriched["name"]),
                gemstone=enriched.get("gemstone"),
                origin=enriched.get("origin"),
                treatment=enriched.get("treatment"),
                carat_weight=enriched.get("carat_weight"),
                weight_ratti=enriched.get("weight_ratti"),
                shape=enriched.get("shape"),
                colour=enriched.get("colour"),
                cut=enriched.get("cut"),
                dimensions=enriched.get("dimensions"),
                certification=enriched.get("certification"),
                certificate_number=enriched.get("certificate_number1"),
                price=enriched.get("price"),
                special_price=enriched.get("special_price"),
                price_per_carat=enriched.get("price_per_carat"),
                qty=int(enriched.get("qty") or 0),
                is_in_stock=bool(int(enriched.get("is_in_stock") or 0)),
                url_key=enriched.get("url_key"),
                meta_title=enriched.get("meta_title"),
                meta_description=enriched.get("meta_description"),
                description=enriched.get("description"),
                short_description=enriched.get("short_description"),
                stage_status=ProductStageStatus.PENDING_APPROVAL,
                validation_status="validated",
                source_payload=product,
                generated_payload=enriched,
            )
            db.add(model)
            staged.append(model)

        batch.success_count = len(staged)
        batch.failed_count = max(0, batch.total_rows - len(staged))
        batch.status = BatchStatus.VALIDATED
        db.commit()
        for item in staged:
            db.refresh(item)
        return staged
