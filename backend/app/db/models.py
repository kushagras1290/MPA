from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.enums import (
    BatchStatus,
    ErrorSeverity,
    MediaAssetType,
    ProductStageStatus,
    UserRole,
)
from app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.DATA_ENTRY)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class UploadBatch(Base, TimestampMixin):
    __tablename__ = "upload_batches"

    id: Mapped[int] = mapped_column(primary_key=True)
    uploaded_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    source_type: Mapped[str] = mapped_column(String(32), default="excel")
    original_file_name: Mapped[str | None] = mapped_column(String(255))
    total_rows: Mapped[int] = mapped_column(Integer, default=0)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[BatchStatus] = mapped_column(Enum(BatchStatus), default=BatchStatus.CREATED)
    raw_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    products: Mapped[list["ProductStaging"]] = relationship(back_populates="batch")


class ProductStaging(Base, TimestampMixin):
    __tablename__ = "products_staging"

    id: Mapped[int] = mapped_column(primary_key=True)
    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("upload_batches.id"), nullable=True, index=True
    )

    sku: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gemstone: Mapped[str | None] = mapped_column(String(120))
    origin: Mapped[str | None] = mapped_column(String(160))
    treatment: Mapped[str | None] = mapped_column(String(255))
    carat_weight: Mapped[float | None] = mapped_column(Numeric(10, 3))
    weight_ratti: Mapped[float | None] = mapped_column(Numeric(10, 3))
    shape: Mapped[str | None] = mapped_column(String(120))
    colour: Mapped[str | None] = mapped_column(String(120))
    cut: Mapped[str | None] = mapped_column(String(120))
    dimensions: Mapped[str | None] = mapped_column(String(160))
    certification: Mapped[str | None] = mapped_column(String(160))
    certificate_number: Mapped[str | None] = mapped_column(String(160))
    price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    special_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    price_per_carat: Mapped[float | None] = mapped_column(Numeric(12, 2))
    qty: Mapped[int] = mapped_column(Integer, default=1)
    is_in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    url_key: Mapped[str | None] = mapped_column(String(255), index=True)
    meta_title: Mapped[str | None] = mapped_column(String(255))
    meta_description: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    short_description: Mapped[str | None] = mapped_column(Text)

    stage_status: Mapped[ProductStageStatus] = mapped_column(
        Enum(ProductStageStatus), default=ProductStageStatus.DRAFT
    )
    validation_status: Mapped[str] = mapped_column(String(32), default="not_validated")
    magento_product_id: Mapped[str | None] = mapped_column(String(120))
    magento_sku: Mapped[str | None] = mapped_column(String(80))
    source_payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    generated_payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    batch: Mapped[UploadBatch] = relationship(back_populates="products")
    custom_attributes: Mapped[list["ProductCustomAttribute"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    media_assets: Mapped[list["MediaAsset"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class ProductCustomAttribute(Base, TimestampMixin):
    __tablename__ = "product_custom_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_staging_id: Mapped[int] = mapped_column(ForeignKey("products_staging.id"), index=True)
    attribute_code: Mapped[str] = mapped_column(String(120), index=True)
    raw_value: Mapped[str | None] = mapped_column(Text)
    mapped_value: Mapped[str | None] = mapped_column(Text)
    magento_option_id: Mapped[str | None] = mapped_column(String(120))

    product: Mapped[ProductStaging] = relationship(back_populates="custom_attributes")


class AttributeMapping(Base, TimestampMixin):
    __tablename__ = "attribute_mappings"

    id: Mapped[int] = mapped_column(primary_key=True)
    attribute_code: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    human_value: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    magento_label: Mapped[str] = mapped_column(String(255), nullable=False)
    magento_option_id: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class MediaAsset(Base, TimestampMixin):
    __tablename__ = "media_assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_staging_id: Mapped[int | None] = mapped_column(
        ForeignKey("products_staging.id"), nullable=True
    )
    sku: Mapped[str] = mapped_column(String(80), index=True)
    asset_type: Mapped[MediaAssetType] = mapped_column(Enum(MediaAssetType))
    original_filename: Mapped[str] = mapped_column(String(255))
    final_filename: Mapped[str | None] = mapped_column(String(255))
    final_url: Mapped[str | None] = mapped_column(Text)
    magento_media_id: Mapped[str | None] = mapped_column(String(120))
    upload_status: Mapped[str] = mapped_column(String(32), default="pending")

    product: Mapped[ProductStaging | None] = relationship(back_populates="media_assets")


class UploadError(Base, TimestampMixin):
    __tablename__ = "upload_errors"

    id: Mapped[int] = mapped_column(primary_key=True)
    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("upload_batches.id"), nullable=True, index=True
    )
    product_staging_id: Mapped[int | None] = mapped_column(
        ForeignKey("products_staging.id"), nullable=True, index=True
    )
    row_number: Mapped[int | None] = mapped_column(Integer)
    sku: Mapped[str | None] = mapped_column(String(80), index=True)
    field_name: Mapped[str | None] = mapped_column(String(120))
    error_type: Mapped[str] = mapped_column(String(80))
    error_message: Mapped[str] = mapped_column(Text)
    suggested_fix: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[ErrorSeverity] = mapped_column(
        Enum(ErrorSeverity), default=ErrorSeverity.ERROR
    )


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(120))
    old_value: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    new_value: Mapped[dict[str, Any] | None] = mapped_column(JSON)
