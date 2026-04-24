from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.db.enums import BatchStatus
from app.db.models import UploadError
from app.schemas.errors import ValidationIssue
from app.schemas.upload import UploadResponse
from app.services.csv_exporter import MagentoCsvExporter
from app.services.error_report import ErrorReportWriter
from app.services.excel_reader import ProductFileReader
from app.services.staging import StagingService
from app.services.validation import ProductValidator

router = APIRouter()


@router.post("/product-file", response_model=UploadResponse)
async def upload_product_file(
    file: UploadFile = File(...),
    db: Session = Depends(db_session),
) -> UploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ProductFileReader.SUPPORTED_SUFFIXES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    with NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        path = Path(temp.name)

    try:
        products = ProductFileReader().read(path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    batch = StagingService().create_batch(db, file.filename, total_rows=len(products))
    result = ProductValidator().validate_batch(products)

    if result.issues:
        for issue in result.issues:
            db.add(
                UploadError(
                    batch_id=batch.id,
                    row_number=issue.row_number,
                    sku=issue.sku,
                    field_name=issue.field_name,
                    error_type=issue.error_type,
                    error_message=issue.error_message,
                    suggested_fix=issue.suggested_fix,
                    severity=issue.severity,
                )
            )
        db.commit()

    if not result.valid:
        batch.status = BatchStatus.FAILED
        batch.failed_count = len(products)
        db.commit()
        return UploadResponse(
            batch_id=batch.id,
            total_rows=len(products),
            status="failed",
            message=f"Validation failed with {len(result.issues)} issues.",
        )

    StagingService().stage_products(db, batch, products)
    return UploadResponse(
        batch_id=batch.id,
        total_rows=len(products),
        status="validated",
        message="Products validated and staged for approval.",
    )


@router.get("/{batch_id}/magento-csv")
def download_magento_csv(batch_id: int, db: Session = Depends(db_session)) -> FileResponse:
    from app.db.models import ProductStaging

    products = db.query(ProductStaging).filter(ProductStaging.batch_id == batch_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No staged products found for batch.")

    rows = [product.generated_payload for product in products]
    output_path = Path(f"/tmp/magento_export_batch_{batch_id}.csv")
    MagentoCsvExporter().export(rows, output_path)
    return FileResponse(output_path, filename=f"magento_export_batch_{batch_id}.csv", media_type="text/csv")


@router.get("/{batch_id}/error-report")
def download_error_report(batch_id: int, db: Session = Depends(db_session)) -> FileResponse:
    errors = db.query(UploadError).filter(UploadError.batch_id == batch_id).all()
    if not errors:
        raise HTTPException(status_code=404, detail="No errors found for batch.")

    issues = [
        ValidationIssue(
            row_number=error.row_number,
            sku=error.sku,
            field_name=error.field_name,
            error_type=error.error_type,
            error_message=error.error_message,
            suggested_fix=error.suggested_fix,
            severity=error.severity,
        )
        for error in errors
    ]
    output_path = Path(f"/tmp/error_report_batch_{batch_id}.xlsx")
    ErrorReportWriter().write_excel(issues, output_path)
    return FileResponse(
        output_path,
        filename=f"error_report_batch_{batch_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
