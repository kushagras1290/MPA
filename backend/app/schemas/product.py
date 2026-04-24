from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductInput(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    sku: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=255)
    gemstone: str | None = None
    origin: str | None = None
    treatment: str | None = None
    carat_weight: float | None = None
    weight_ratti: float | None = None
    shape: str | None = None
    colour: str | None = None
    cut: str | None = None
    dimensions: str | None = None
    certification: str | None = None
    certificate_number1: str | None = None
    price: float | None = None
    special_price: float | None = None
    qty: int | None = 1
    vendor: str | None = None
    vendor_id: str | None = None
    hsn_code: str | None = None
    dispatch_days: str | None = None
    shipping_days: int | None = None
    return_policy: str | None = None
    main_image: str | None = None
    source_image_path: str | None = None
    verified_certificateimage: str | None = None
    automatic_video_link: str | None = None
    short_description: str | None = None
    description: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    url_key: str | None = None

    @field_validator("sku", "name")
    @classmethod
    def strip_required(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value

    @field_validator("price", "special_price", "carat_weight", "weight_ratti")
    @classmethod
    def numeric_must_be_positive(cls, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise ValueError("Numeric value cannot be negative")
        return value


class ProductGenerated(BaseModel):
    raw: dict[str, Any]
    normalized: dict[str, Any]
    magento_export_row: dict[str, Any]
    magento_api_payload: dict[str, Any]


class ProductStagingRead(BaseModel):
    id: int
    sku: str
    name: str
    gemstone: str | None
    origin: str | None
    carat_weight: float | None
    weight_ratti: float | None
    price: float | None
    qty: int
    is_in_stock: bool
    stage_status: str
    validation_status: str

    model_config = ConfigDict(from_attributes=True)
