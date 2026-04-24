from collections.abc import Mapping
from typing import Any

from app.domain.magento_columns import SOURCE_ALIASES

NULL_LIKE_VALUES = {"", ",", "nan", "none", "null", "NaN", "NULL", "None"}


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and str(value) == "nan":
        return True
    if isinstance(value, str) and value.strip() in NULL_LIKE_VALUES:
        return True
    return False


def clean_scalar(value: Any) -> Any:
    if is_empty(value):
        return None
    if isinstance(value, str):
        return value.strip()
    return value


def normalize_row(row: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in row.items():
        if key is None:
            continue
        clean_key = SOURCE_ALIASES.get(str(key).strip(), str(key).strip())
        normalized[clean_key] = clean_scalar(value)

    if not normalized.get("image"):
        normalized["image"] = normalized.get("source_image_path")

    if not normalized.get("small_image") and normalized.get("image"):
        normalized["small_image"] = normalized["image"]

    if not normalized.get("thumbnail") and normalized.get("image"):
        normalized["thumbnail"] = normalized["image"]

    if not normalized.get("certificate_number1") and normalized.get("certificate_number"):
        normalized["certificate_number1"] = normalized["certificate_number"]

    return normalized
