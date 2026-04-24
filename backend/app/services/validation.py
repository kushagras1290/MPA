from collections import Counter
from enum import StrEnum
from typing import Any

from app.db.enums import ErrorSeverity
from app.domain.field_policy import (
    CREATE_REQUIRED_FIELDS,
    DROPDOWN_FIELDS,
    LOOSE_GEMSTONE_REQUIRED_FIELDS,
    NEGATIVE_ALLOWED_FIELDS,
    NUMERIC_FIELDS,
)
from app.schemas.errors import ValidationIssue, ValidationResult


class ValidationMode(StrEnum):
    CREATE = "create"
    LEGACY_AUDIT = "legacy_audit"
    UPDATE = "update"


def _is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _is_loose_gemstone(product: dict[str, Any]) -> bool:
    attribute_set = str(product.get("attribute_set_id") or "").lower()
    product_type = str(product.get("product_type") or "").lower()
    offer_type = str(product.get("offer_type") or "").lower()
    return (
        "gemstone" in attribute_set
        and product_type in {"", "single stone", "rough", "pair", "gemstone set", "gemstone lot"}
        or offer_type == "loose gemstone"
    )


class ProductValidator:
    def __init__(
        self,
        allowed_values: dict[str, set[str]] | None = None,
        existing_skus: set[str] | None = None,
        existing_url_keys: set[str] | None = None,
        mode: ValidationMode = ValidationMode.CREATE,
    ) -> None:
        self.allowed_values = allowed_values or {}
        self.existing_skus = existing_skus or set()
        self.existing_url_keys = existing_url_keys or set()
        self.mode = mode

    def validate_batch(self, products: list[dict[str, Any]]) -> ValidationResult:
        issues: list[ValidationIssue] = []
        sku_counts = Counter(str(p.get("sku")) for p in products if p.get("sku"))
        url_counts = Counter(str(p.get("url_key")) for p in products if p.get("url_key"))

        for index, product in enumerate(products, start=2):
            issues.extend(self.validate_product(product, row_number=index).issues)

            sku = str(product.get("sku") or "")
            if sku and sku_counts[sku] > 1:
                issues.append(
                    ValidationIssue(
                        row_number=index,
                        sku=sku,
                        field_name="sku",
                        error_type="duplicate",
                        error_message=f"Duplicate SKU `{sku}` found in uploaded file.",
                        suggested_fix="Keep one row per SKU.",
                        severity=ErrorSeverity.BLOCKER,
                    )
                )
            if sku and sku in self.existing_skus and self.mode == ValidationMode.CREATE:
                issues.append(
                    ValidationIssue(
                        row_number=index,
                        sku=sku,
                        field_name="sku",
                        error_type="duplicate",
                        error_message=f"SKU `{sku}` already exists.",
                        suggested_fix="Use update mode or change SKU.",
                        severity=ErrorSeverity.BLOCKER,
                    )
                )

            url_key = str(product.get("url_key") or "")
            if url_key and url_counts[url_key] > 1:
                issues.append(
                    ValidationIssue(
                        row_number=index,
                        sku=sku,
                        field_name="url_key",
                        error_type="duplicate",
                        error_message=f"Duplicate URL key `{url_key}` found in uploaded file.",
                        suggested_fix="Append SKU to URL key.",
                        severity=ErrorSeverity.ERROR,
                    )
                )
            if url_key and url_key in self.existing_url_keys and self.mode == ValidationMode.CREATE:
                issues.append(
                    ValidationIssue(
                        row_number=index,
                        sku=sku,
                        field_name="url_key",
                        error_type="duplicate",
                        error_message=f"URL key `{url_key}` already exists.",
                        suggested_fix="Regenerate URL key.",
                        severity=ErrorSeverity.ERROR,
                    )
                )

        return ValidationResult(valid=not any(i.severity == ErrorSeverity.BLOCKER for i in issues), issues=issues)

    def validate_product(self, product: dict[str, Any], row_number: int | None = None) -> ValidationResult:
        issues: list[ValidationIssue] = []
        sku = product.get("sku")

        required_fields = CREATE_REQUIRED_FIELDS
        if _is_loose_gemstone(product):
            required_fields = tuple(dict.fromkeys((*required_fields, *LOOSE_GEMSTONE_REQUIRED_FIELDS)))

        for field in required_fields:
            if _is_blank(product.get(field)):
                severity = ErrorSeverity.BLOCKER if self.mode == ValidationMode.CREATE else ErrorSeverity.WARNING
                issues.append(
                    ValidationIssue(
                        row_number=row_number,
                        sku=sku,
                        field_name=field,
                        error_type="missing",
                        error_message=f"`{field}` is required by the {self.mode} validation policy.",
                        suggested_fix=f"Provide `{field}` or change product type/category policy.",
                        severity=severity,
                    )
                )

        for field in NUMERIC_FIELDS:
            value = product.get(field)
            if _is_blank(value):
                continue
            try:
                numeric = float(str(value).replace(",", ""))
            except (TypeError, ValueError):
                issues.append(
                    ValidationIssue(
                        row_number=row_number,
                        sku=sku,
                        field_name=field,
                        error_type="invalid_numeric",
                        error_message=f"`{field}` must be numeric.",
                        suggested_fix="Remove currency symbols, commas, and text.",
                        severity=ErrorSeverity.BLOCKER,
                    )
                )
                continue

            if numeric < 0 and field not in NEGATIVE_ALLOWED_FIELDS:
                issues.append(
                    ValidationIssue(
                        row_number=row_number,
                        sku=sku,
                        field_name=field,
                        error_type="invalid_numeric",
                        error_message=f"`{field}` cannot be negative.",
                        suggested_fix="Use a positive value.",
                        severity=ErrorSeverity.BLOCKER,
                    )
                )

        price = product.get("price")
        special_price = product.get("special_price")
        if not _is_blank(price) and not _is_blank(special_price):
            try:
                if float(str(special_price).replace(",", "")) >= float(str(price).replace(",", "")):
                    issues.append(
                        ValidationIssue(
                            row_number=row_number,
                            sku=sku,
                            field_name="special_price",
                            error_type="invalid_price",
                            error_message="Special price must be lower than regular price.",
                            suggested_fix="Lower special price or leave it blank.",
                            severity=ErrorSeverity.ERROR,
                        )
                    )
            except (TypeError, ValueError):
                pass

        qty = product.get("qty")
        is_in_stock = product.get("is_in_stock")
        if not _is_blank(qty):
            try:
                qty_num = float(str(qty).replace(",", ""))
                if qty_num <= 0 and str(is_in_stock).lower() in {"1", "true", "yes"}:
                    issues.append(
                        ValidationIssue(
                            row_number=row_number,
                            sku=sku,
                            field_name="is_in_stock",
                            error_type="stock_mismatch",
                            error_message="qty is 0 or negative but is_in_stock is true.",
                            suggested_fix="Set is_in_stock to 0 or correct quantity.",
                            severity=ErrorSeverity.ERROR,
                        )
                    )
            except (TypeError, ValueError):
                pass

        for field in DROPDOWN_FIELDS:
            allowed = self.allowed_values.get(field)
            value = product.get(field)
            if allowed and not _is_blank(value) and str(value) not in allowed:
                issues.append(
                    ValidationIssue(
                        row_number=row_number,
                        sku=sku,
                        field_name=field,
                        error_type="invalid_dropdown",
                        error_message=f"`{value}` is not an allowed value for `{field}`.",
                        suggested_fix=f"Use one of: {', '.join(sorted(list(allowed))[:20])}",
                        severity=ErrorSeverity.ERROR,
                    )
                )

        main_image = product.get("image") or product.get("main_image") or product.get("source_image_path")
        if _is_blank(main_image):
            severity = ErrorSeverity.BLOCKER if self.mode == ValidationMode.CREATE else ErrorSeverity.WARNING
            issues.append(
                ValidationIssue(
                    row_number=row_number,
                    sku=sku,
                    field_name="image",
                    error_type="missing_media",
                    error_message="Main image is missing.",
                    suggested_fix="Provide image/main_image/source image path.",
                    severity=severity,
                )
            )

        return ValidationResult(valid=not any(i.severity == ErrorSeverity.BLOCKER for i in issues), issues=issues)
