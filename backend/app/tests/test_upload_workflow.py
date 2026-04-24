from collections.abc import Generator
from importlib import import_module
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import db_session
from app.db.session import Base
from app.main import app as fastapi_app

import_module("app.db.base")


def test_upload_stage_review_and_export_workflow() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_db_session() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[db_session] = override_db_session
    try:
        client = TestClient(fastapi_app)
        sample = (
            Path(__file__).resolve().parents[3]
            / "samples"
            / "generated_magento_export_preview.csv"
        )

        with sample.open("rb") as handle:
            upload_response = client.post(
                "/api/uploads/product-file",
                files={"file": (sample.name, handle, "text/csv")},
            )

        assert upload_response.status_code == 200
        upload_body = upload_response.json()
        assert upload_body["status"] == "validated"
        assert upload_body["total_rows"] == 5

        staged_response = client.get("/api/products/staging")
        assert staged_response.status_code == 200
        staged_products = staged_response.json()
        assert len(staged_products) == 5

        first_product_id = staged_products[0]["id"]
        approve_response = client.post(f"/api/products/staging/{first_product_id}/approve")
        assert approve_response.status_code == 200
        assert approve_response.json()["stage_status"] == "approved"

        csv_response = client.get(f"/api/uploads/{upload_body['batch_id']}/magento-csv")
        assert csv_response.status_code == 200
        assert "text/csv" in csv_response.headers["content-type"]
        assert b"sku" in csv_response.content.splitlines()[0]
    finally:
        fastapi_app.dependency_overrides.clear()
