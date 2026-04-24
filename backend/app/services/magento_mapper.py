from typing import Any

from app.core.config import settings
from app.domain.magento_columns import MAGENTO_EXPORT_COLUMNS
from app.services.field_generation import generate_fields, to_decimal

STATUS_TO_MAGENTO_API = {"Enabled": 1, "Disabled": 2, "1": 1, "2": 2, 1: 1, 2: 2}
ATTRIBUTE_SET_NAME_TO_ID = {"Gemstones": settings.magento_default_attribute_set_id}


class MagentoRowMapper:
    def to_export_row(self, product: dict[str, Any]) -> dict[str, Any]:
        enriched = generate_fields(product)
        return {column: enriched.get(column, "") for column in MAGENTO_EXPORT_COLUMNS}

    def to_export_rows(self, products: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.to_export_row(product) for product in products]


class MagentoApiPayloadMapper:
    DROPDOWN_CUSTOM_ATTRIBUTES = {
        "gemstone",
        "origin",
        "treatment",
        "shape",
        "colour",
        "cut",
        "cutting_style",
        "certification",
        "return_policy",
        "classification",
        "gemstone2",
        "gemstone2_type",
        "product_category_type",
        "tax_class_id",
        "vendor",
        "offer_type",
        "product_type",
        "dimension_type",
        "gem_optical_properties",
        "gem_trade_name_config",
    }

    SIMPLE_CUSTOM_ATTRIBUTES = {
        "url_key",
        "meta_title",
        "description",
        "short_description",
        "description2",
        "carat_weight",
        "weight_carat",
        "weight_ratti",
        "weight_sort1",
        "price_per_carat",
        "price_per_carat_range",
        "price_range",
        "dimensions",
        "certificate_number1",
        "verified_certificateimage",
        "verified_certificateimage1",
        "additional_certification",
        "automatic_video_link",
        "gemstone_benifits_new",
        "specific_gravity",
        "refractive_index",
        "approx_weight_range",
        "catalog_uploaded_by",
        "hsn_code",
        "shipping_days",
        "dispatch_days",
        "sku_for_vendor_product",
        "invoice_id",
        "name2",
        "j_colour",
        "gemstone3",
        "comment_explation",
    }

    def __init__(self, option_mappings: dict[tuple[str, str], str] | None = None) -> None:
        self.option_mappings = option_mappings or {}

    def _mapped_value(self, attribute_code: str, raw_value: Any) -> Any:
        if raw_value is None or raw_value == "":
            return None
        key = (attribute_code, str(raw_value))
        return self.option_mappings.get(key, raw_value)

    def _attribute_set_id(self, raw_value: Any) -> int:
        if raw_value in (None, ""):
            return settings.magento_default_attribute_set_id
        if isinstance(raw_value, int):
            return raw_value
        value = str(raw_value)
        if value.isdigit():
            return int(value)
        return ATTRIBUTE_SET_NAME_TO_ID.get(value, settings.magento_default_attribute_set_id)

    def _status(self, raw_value: Any) -> int:
        return STATUS_TO_MAGENTO_API.get(
            raw_value, STATUS_TO_MAGENTO_API.get(str(raw_value), settings.default_product_status)
        )

    def to_payload(self, product: dict[str, Any]) -> dict[str, Any]:
        enriched = generate_fields(product)
        custom_attributes: list[dict[str, Any]] = []

        for code in sorted(self.DROPDOWN_CUSTOM_ATTRIBUTES | self.SIMPLE_CUSTOM_ATTRIBUTES):
            value = enriched.get(code)
            if value is None or value == "":
                continue
            custom_attributes.append(
                {"attribute_code": code, "value": self._mapped_value(code, value)}
            )

        price = to_decimal(enriched.get("price")) or 0
        qty = to_decimal(enriched.get("qty")) or 0
        carat = (
            to_decimal(enriched.get("weight_carat"))
            or to_decimal(enriched.get("carat_weight"))
            or 0
        )

        return {
            "product": {
                "sku": enriched["sku"],
                "name": enriched["name"],
                "attribute_set_id": self._attribute_set_id(enriched.get("attribute_set_id")),
                "price": float(price),
                "status": self._status(enriched.get("status")),
                "visibility": int(
                    enriched.get("visibility") or settings.default_product_visibility
                ),
                "type_id": "simple",
                "weight": float(carat) if carat else settings.default_product_weight,
                "extension_attributes": {
                    "stock_item": {
                        "qty": int(qty),
                        "is_in_stock": bool(int(enriched.get("is_in_stock") or 0)),
                    }
                },
                "custom_attributes": custom_attributes,
            }
        }
