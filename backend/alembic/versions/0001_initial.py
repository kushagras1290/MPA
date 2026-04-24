"""Initial schema.

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-24
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    user_role = sa.Enum("DATA_ENTRY", "CATALOG_MANAGER", "ADMIN", "SEO", "IMAGE_TEAM", name="userrole")
    batch_status = sa.Enum(
        "CREATED", "PROCESSING", "VALIDATED", "FAILED", "PARTIAL", "APPROVED",
        "EXPORTED", "PUSHED_TO_MAGENTO", "ROLLED_BACK", name="batchstatus"
    )
    product_stage_status = sa.Enum(
        "DRAFT", "VALIDATION_FAILED", "VALIDATED", "PENDING_APPROVAL", "REJECTED",
        "APPROVED", "MAGENTO_DRAFT_CREATED", "PUBLISHED", "UPLOAD_FAILED", "DISABLED",
        "ARCHIVED", name="productstagestatus"
    )
    error_severity = sa.Enum("WARNING", "ERROR", "BLOCKER", name="errorseverity")
    media_asset_type = sa.Enum("MAIN", "GALLERY", "CERTIFICATE", "VIDEO", name="mediaassettype")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "upload_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uploaded_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("original_file_name", sa.String(length=255), nullable=True),
        sa.Column("total_rows", sa.Integer(), nullable=False),
        sa.Column("success_count", sa.Integer(), nullable=False),
        sa.Column("failed_count", sa.Integer(), nullable=False),
        sa.Column("status", batch_status, nullable=False),
        sa.Column("raw_metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "products_staging",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_id", sa.Integer(), sa.ForeignKey("upload_batches.id"), nullable=True),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("gemstone", sa.String(length=120), nullable=True),
        sa.Column("origin", sa.String(length=160), nullable=True),
        sa.Column("treatment", sa.String(length=255), nullable=True),
        sa.Column("carat_weight", sa.Numeric(10, 3), nullable=True),
        sa.Column("weight_ratti", sa.Numeric(10, 3), nullable=True),
        sa.Column("shape", sa.String(length=120), nullable=True),
        sa.Column("colour", sa.String(length=120), nullable=True),
        sa.Column("cut", sa.String(length=120), nullable=True),
        sa.Column("dimensions", sa.String(length=160), nullable=True),
        sa.Column("certification", sa.String(length=160), nullable=True),
        sa.Column("certificate_number", sa.String(length=160), nullable=True),
        sa.Column("price", sa.Numeric(12, 2), nullable=True),
        sa.Column("special_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("price_per_carat", sa.Numeric(12, 2), nullable=True),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("is_in_stock", sa.Boolean(), nullable=False),
        sa.Column("url_key", sa.String(length=255), nullable=True),
        sa.Column("meta_title", sa.String(length=255), nullable=True),
        sa.Column("meta_description", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("stage_status", product_stage_status, nullable=False),
        sa.Column("validation_status", sa.String(length=32), nullable=False),
        sa.Column("magento_product_id", sa.String(length=120), nullable=True),
        sa.Column("magento_sku", sa.String(length=80), nullable=True),
        sa.Column("source_payload", sa.JSON(), nullable=False),
        sa.Column("generated_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_products_staging_batch_id", "products_staging", ["batch_id"])
    op.create_index("ix_products_staging_sku", "products_staging", ["sku"])
    op.create_index("ix_products_staging_url_key", "products_staging", ["url_key"])

    op.create_table(
        "product_custom_attributes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_staging_id", sa.Integer(), sa.ForeignKey("products_staging.id"), nullable=False),
        sa.Column("attribute_code", sa.String(length=120), nullable=False),
        sa.Column("raw_value", sa.Text(), nullable=True),
        sa.Column("mapped_value", sa.Text(), nullable=True),
        sa.Column("magento_option_id", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_product_custom_attributes_product_staging_id", "product_custom_attributes", ["product_staging_id"])
    op.create_index("ix_product_custom_attributes_attribute_code", "product_custom_attributes", ["attribute_code"])

    op.create_table(
        "attribute_mappings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attribute_code", sa.String(length=120), nullable=False),
        sa.Column("human_value", sa.String(length=255), nullable=False),
        sa.Column("magento_label", sa.String(length=255), nullable=False),
        sa.Column("magento_option_id", sa.String(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_attribute_mappings_attribute_code", "attribute_mappings", ["attribute_code"])
    op.create_index("ix_attribute_mappings_human_value", "attribute_mappings", ["human_value"])

    op.create_table(
        "media_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_staging_id", sa.Integer(), sa.ForeignKey("products_staging.id"), nullable=True),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("asset_type", media_asset_type, nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("final_filename", sa.String(length=255), nullable=True),
        sa.Column("final_url", sa.Text(), nullable=True),
        sa.Column("magento_media_id", sa.String(length=120), nullable=True),
        sa.Column("upload_status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_media_assets_sku", "media_assets", ["sku"])

    op.create_table(
        "upload_errors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_id", sa.Integer(), sa.ForeignKey("upload_batches.id"), nullable=True),
        sa.Column("product_staging_id", sa.Integer(), sa.ForeignKey("products_staging.id"), nullable=True),
        sa.Column("row_number", sa.Integer(), nullable=True),
        sa.Column("sku", sa.String(length=80), nullable=True),
        sa.Column("field_name", sa.String(length=120), nullable=True),
        sa.Column("error_type", sa.String(length=80), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.Column("suggested_fix", sa.Text(), nullable=True),
        sa.Column("severity", error_severity, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_upload_errors_batch_id", "upload_errors", ["batch_id"])
    op.create_index("ix_upload_errors_product_staging_id", "upload_errors", ["product_staging_id"])
    op.create_index("ix_upload_errors_sku", "upload_errors", ["sku"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity_type", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.String(length=120), nullable=True),
        sa.Column("old_value", sa.JSON(), nullable=True),
        sa.Column("new_value", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("upload_errors")
    op.drop_table("media_assets")
    op.drop_table("attribute_mappings")
    op.drop_table("product_custom_attributes")
    op.drop_table("products_staging")
    op.drop_table("upload_batches")
    op.drop_table("users")
