from enum import StrEnum


class UserRole(StrEnum):
    DATA_ENTRY = "data_entry"
    CATALOG_MANAGER = "catalog_manager"
    ADMIN = "admin"
    SEO = "seo"
    IMAGE_TEAM = "image_team"


class BatchStatus(StrEnum):
    CREATED = "created"
    PROCESSING = "processing"
    VALIDATED = "validated"
    FAILED = "failed"
    PARTIAL = "partial"
    APPROVED = "approved"
    EXPORTED = "exported"
    PUSHED_TO_MAGENTO = "pushed_to_magento"
    ROLLED_BACK = "rolled_back"


class ProductStageStatus(StrEnum):
    DRAFT = "draft"
    VALIDATION_FAILED = "validation_failed"
    VALIDATED = "validated"
    PENDING_APPROVAL = "pending_approval"
    REJECTED = "rejected"
    APPROVED = "approved"
    MAGENTO_DRAFT_CREATED = "magento_draft_created"
    PUBLISHED = "published"
    UPLOAD_FAILED = "upload_failed"
    DISABLED = "disabled"
    ARCHIVED = "archived"


class ErrorSeverity(StrEnum):
    WARNING = "warning"
    ERROR = "error"
    BLOCKER = "blocker"


class MediaAssetType(StrEnum):
    MAIN = "main"
    GALLERY = "gallery"
    CERTIFICATE = "certificate"
    VIDEO = "video"
