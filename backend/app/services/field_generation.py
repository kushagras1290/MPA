import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

from app.domain.defaults import DEFAULT_MAGENTO_VALUES
from app.domain.gempundit_taxonomy import HSN_BY_GEMSTONE, classify_gemstone

RATTI_TO_CARAT = Decimal("0.91")
PRICE_BUCKET = Decimal("500")
PRICE_PER_CARAT_BUCKET = Decimal("500")


def _is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def to_decimal(value: Any) -> Decimal | None:
    if _is_blank(value):
        return None
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None


def quantize(value: Decimal, places: str = "0.01") -> Decimal:
    return value.quantize(Decimal(places), rounding=ROUND_HALF_UP)


def decimal_to_csv_number(value: Decimal, places: str = "0.0000") -> str:
    return f"{quantize(value, places):f}"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def generate_url_key(product: dict[str, Any]) -> str:
    explicit = product.get("url_key")
    if explicit:
        return slugify(str(explicit))
    gemstone = product.get("gemstone") or product.get("classification") or "gemstone"
    carat = product.get("carat_weight") or product.get("weight_carat")
    sku = product.get("sku")
    return slugify(" ".join(str(piece) for piece in [gemstone, sku] if piece)) if not carat else slugify(
        " ".join(str(piece) for piece in [gemstone, carat, "carats", sku] if piece)
    )


def generate_meta_title(product: dict[str, Any]) -> str:
    if product.get("meta_title"):
        return str(product["meta_title"])
    gemstone = product.get("gemstone") or "Gemstone"
    carat = product.get("carat_weight") or product.get("weight_carat")
    sku = product.get("sku")
    origin = product.get("origin")
    origin_part = f" from {origin}" if origin else ""
    if carat:
        return f"Premium Certified {gemstone} for Astrological Use - {carat} Carats ({sku}){origin_part}"
    return f"Premium Certified {gemstone} ({sku}){origin_part}"


def generate_name2(product: dict[str, Any]) -> str:
    if product.get("name2"):
        return str(product["name2"])
    gemstone = product.get("gemstone") or "Gemstone"
    carat = product.get("carat_weight") or product.get("weight_carat") or ""
    return f"{carat} ct {gemstone} Natural Original Top Quality Lab Certified Gemstone".strip()


def generate_short_description(product: dict[str, Any]) -> str:
    if product.get("short_description"):
        return str(product["short_description"])
    gemstone = product.get("gemstone") or "Gemstone"
    carat = product.get("carat_weight") or product.get("weight_carat")
    origin = product.get("origin")
    origin_part = f" from {origin}" if origin else ""
    return f"Natural {gemstone} weighing {carat} carat{origin_part}"


def generate_description(product: dict[str, Any]) -> str:
    if product.get("description"):
        return str(product["description"])
    gemstone = product.get("gemstone") or "Gemstone"
    carat = product.get("carat_weight") or product.get("weight_carat")
    shape = product.get("shape") or "selected"
    return f"Natural {gemstone} weighing {carat} carats in {shape} shape"


def generate_description2(product: dict[str, Any]) -> str:
    if product.get("description2"):
        return str(product["description2"])
    gemstone2 = product.get("gemstone2") or product.get("gemstone") or "gemstone"
    carat = product.get("carat_weight") or product.get("weight_carat")
    ratti = product.get("weight_ratti")
    price = product.get("price")
    return (
        f"Buy Natural {gemstone2} {carat} for sale online, weighing {carat} carats "
        f"(roughly {ratti} ratti). The price of this gemstone is {price}."
    )


def derive_status(qty: Decimal | None, explicit_status: Any = None) -> str:
    if explicit_status not in (None, ""):
        return str(explicit_status)
    return "Enabled" if qty is not None and qty > 0 else "Disabled"


def derive_tax_class(gemstone: str | None, explicit_tax_class: Any = None) -> str:
    if explicit_tax_class not in (None, ""):
        return str(explicit_tax_class)
    if gemstone in {"Ruby"}:
        return "Jewellery"
    if gemstone in {"Red Coral"}:
        return "Jewellery Corals"
    if gemstone in {"Blue Sapphire", "Yellow Sapphire", "White Sapphire"}:
        return "Jewellery Sapphire"
    return "Jewellery Semiprecious"


def generate_fields(product: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(DEFAULT_MAGENTO_VALUES)
    enriched.update({k: v for k, v in product.items() if v is not None})

    sku = str(enriched.get("sku") or "").strip()
    if sku and not enriched.get("sku_for_vendor_product"):
        enriched["sku_for_vendor_product"] = sku

    carat = to_decimal(enriched.get("carat_weight")) or to_decimal(enriched.get("weight_carat"))
    if carat is not None:
        enriched["carat_weight"] = f"{carat.normalize():f}"
        enriched["weight_carat"] = decimal_to_csv_number(carat)
        ratti = to_decimal(enriched.get("weight_ratti")) or quantize(carat / RATTI_TO_CARAT)
        enriched["weight_ratti"] = f"{ratti.normalize():f}"
        enriched["weight_sort1"] = decimal_to_csv_number(carat * Decimal("100"))

    price = to_decimal(enriched.get("price"))
    if price is not None:
        enriched["price"] = decimal_to_csv_number(price)

    special_price = to_decimal(enriched.get("special_price"))
    if special_price is not None:
        enriched["special_price"] = decimal_to_csv_number(special_price)

    if price is not None and carat is not None and carat > 0:
        ppc = quantize(price / carat, "1")
        enriched["price_per_carat"] = decimal_to_csv_number(ppc)
        ppc_range = (ppc // PRICE_PER_CARAT_BUCKET) * PRICE_PER_CARAT_BUCKET
        enriched["price_per_carat_range"] = f"{int(ppc_range)}"

    if price is not None:
        price_range = (price // PRICE_BUCKET) * PRICE_BUCKET
        enriched["price_range"] = f"{int(price_range)}"

    qty = to_decimal(enriched.get("qty"))
    if qty is not None:
        enriched["qty"] = decimal_to_csv_number(qty)
        enriched["is_in_stock"] = "1" if qty > 0 else "0"
        enriched["status"] = derive_status(qty, product.get("status"))

    gemstone = str(enriched.get("gemstone") or "").strip()
    if gemstone:
        enriched.setdefault("classification", gemstone)
        enriched.setdefault("gemstone2", gemstone)
        cutting_style = enriched.get("cutting_style") or enriched.get("cut")
        dimension_type = enriched.get("dimension_type") or "Not Calibrated"
        if cutting_style and not enriched.get("gemstone3"):
            enriched["gemstone3"] = f"{gemstone}-{cutting_style}-{dimension_type}"
        classification = classify_gemstone(gemstone)
        if classification and not enriched.get("gemstone2_type"):
            enriched["gemstone2_type"] = classification
        if not enriched.get("product_category_type"):
            enriched["product_category_type"] = "P" if classification == "1 - Precious" else "MP"
        if not enriched.get("hsn_code"):
            enriched["hsn_code"] = HSN_BY_GEMSTONE.get(gemstone, "71039990")
        enriched["tax_class_id"] = derive_tax_class(gemstone, product.get("tax_class_id"))

    colour = enriched.get("colour") or enriched.get("j_colour")
    if colour and not enriched.get("j_colour"):
        enriched["j_colour"] = colour

    enriched["url_key"] = generate_url_key(enriched)
    enriched["meta_title"] = generate_meta_title(enriched)
    enriched["name2"] = generate_name2(enriched)
    enriched["short_description"] = generate_short_description(enriched)
    enriched["description"] = generate_description(enriched)
    enriched["description2"] = generate_description2(enriched)

    main_image = enriched.get("image") or enriched.get("main_image") or enriched.get("source_image_path")
    if main_image:
        enriched["image"] = main_image
        enriched.setdefault("small_image", main_image)
        enriched.setdefault("thumbnail", main_image)

    return enriched
