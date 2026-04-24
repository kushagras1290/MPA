from dataclasses import dataclass
from enum import StrEnum


class FieldAccess(StrEnum):
    STAFF = "staff"
    AUTO = "auto"
    ADMIN = "admin"
    SEO = "seo"
    IMAGE = "image"
    CONDITIONAL = "conditional"


@dataclass(frozen=True)
class FieldRule:
    code: str
    access: FieldAccess
    required_for_create: bool = False
    required_for_loose_gemstone: bool = False
    dropdown: bool = False
    numeric: bool = False
    negative_allowed: bool = False
    description: str = ""


FIELD_RULES: dict[str, FieldRule] = {
    "attribute_set_id": FieldRule("attribute_set_id", FieldAccess.ADMIN, dropdown=True),
    "sku": FieldRule("sku", FieldAccess.STAFF, True, True, description="Unique product SKU"),
    "name": FieldRule("name", FieldAccess.STAFF, True, True),
    "meta_title": FieldRule("meta_title", FieldAccess.SEO),
    "url_key": FieldRule("url_key", FieldAccess.SEO),
    "sku_for_vendor_product": FieldRule("sku_for_vendor_product", FieldAccess.STAFF),
    "treatment": FieldRule("treatment", FieldAccess.STAFF, False, True, dropdown=True),
    "carat_weight": FieldRule("carat_weight", FieldAccess.STAFF, False, True, numeric=True),
    "classification": FieldRule("classification", FieldAccess.STAFF, dropdown=True),
    "cutting_style": FieldRule("cutting_style", FieldAccess.STAFF, dropdown=True),
    "dimensions": FieldRule("dimensions", FieldAccess.STAFF, False, True),
    "j_colour": FieldRule("j_colour", FieldAccess.STAFF, dropdown=True),
    "name2": FieldRule("name2", FieldAccess.AUTO),
    "offers": FieldRule("offers", FieldAccess.ADMIN, dropdown=True),
    "vendor_id": FieldRule("vendor_id", FieldAccess.ADMIN),
    "weight_ratti": FieldRule("weight_ratti", FieldAccess.AUTO, numeric=True),
    "shipping_days": FieldRule("shipping_days", FieldAccess.STAFF, numeric=True),
    "hsn_code": FieldRule("hsn_code", FieldAccess.STAFF, dropdown=True),
    "price": FieldRule("price", FieldAccess.STAFF, True, True, numeric=True),
    "special_price": FieldRule("special_price", FieldAccess.STAFF, numeric=True),
    "weight_carat": FieldRule("weight_carat", FieldAccess.AUTO, numeric=True),
    "price_per_carat": FieldRule("price_per_carat", FieldAccess.AUTO, numeric=True),
    "weight_sort1": FieldRule("weight_sort1", FieldAccess.AUTO, numeric=True),
    "status": FieldRule("status", FieldAccess.ADMIN, dropdown=True),
    "tax_class_id": FieldRule("tax_class_id", FieldAccess.ADMIN, dropdown=True),
    "gemstone": FieldRule("gemstone", FieldAccess.STAFF, False, True, dropdown=True),
    "gem_composition": FieldRule("gem_composition", FieldAccess.STAFF, dropdown=True),
    "shape": FieldRule("shape", FieldAccess.STAFF, False, True, dropdown=True),
    "certification": FieldRule("certification", FieldAccess.STAFF, False, True, dropdown=True),
    "return_policy": FieldRule("return_policy", FieldAccess.STAFF, dropdown=True),
    "colour": FieldRule("colour", FieldAccess.STAFF, False, True, dropdown=True),
    "cut": FieldRule("cut", FieldAccess.STAFF, False, True, dropdown=True),
    "dimension_type": FieldRule("dimension_type", FieldAccess.STAFF, dropdown=True),
    "dispatch_days": FieldRule("dispatch_days", FieldAccess.STAFF),
    "gemstone2": FieldRule("gemstone2", FieldAccess.STAFF, dropdown=True),
    "vendor": FieldRule("vendor", FieldAccess.STAFF, dropdown=True),
    "offer_type": FieldRule("offer_type", FieldAccess.ADMIN, dropdown=True),
    "origin": FieldRule("origin", FieldAccess.STAFF, False, True, dropdown=True),
    "product_type": FieldRule("product_type", FieldAccess.STAFF, dropdown=True),
    "description": FieldRule("description", FieldAccess.SEO),
    "short_description": FieldRule("short_description", FieldAccess.SEO),
    "comment_explation": FieldRule("comment_explation", FieldAccess.ADMIN),
    "description2": FieldRule("description2", FieldAccess.SEO),
    "qty": FieldRule("qty", FieldAccess.STAFF, True, True, numeric=True, negative_allowed=True),
    "is_in_stock": FieldRule("is_in_stock", FieldAccess.AUTO, dropdown=True),
    "gemstone3": FieldRule("gemstone3", FieldAccess.AUTO),
    "image": FieldRule("image", FieldAccess.IMAGE, False, True),
    "small_image": FieldRule("small_image", FieldAccess.IMAGE),
    "thumbnail": FieldRule("thumbnail", FieldAccess.IMAGE),
    "invoice_id": FieldRule("invoice_id", FieldAccess.ADMIN),
    "news_from_date": FieldRule("news_from_date", FieldAccess.ADMIN),
    "news_to_date": FieldRule("news_to_date", FieldAccess.ADMIN),
    "stickers": FieldRule("stickers", FieldAccess.ADMIN, dropdown=True),
    "callfor": FieldRule("callfor", FieldAccess.ADMIN, dropdown=True),
    "quality_config_gem": FieldRule("quality_config_gem", FieldAccess.ADMIN),
    "redirect_select_for_quality": FieldRule("redirect_select_for_quality", FieldAccess.ADMIN),
    "select_for_quality": FieldRule("select_for_quality", FieldAccess.ADMIN),
    "mainproduct_forjewlrypage": FieldRule("mainproduct_forjewlrypage", FieldAccess.ADMIN),
    "gemstone2_type": FieldRule("gemstone2_type", FieldAccess.AUTO, dropdown=True),
    "price_per_carat_range": FieldRule("price_per_carat_range", FieldAccess.AUTO, numeric=True),
    "metal_config": FieldRule("metal_config", FieldAccess.ADMIN, dropdown=True),
    "ideal_design": FieldRule("ideal_design", FieldAccess.ADMIN),
    "price_for_jewelry": FieldRule("price_for_jewelry", FieldAccess.ADMIN, numeric=True),
    "promotion_baseprice_jewlery": FieldRule("promotion_baseprice_jewlery", FieldAccess.ADMIN, numeric=True),
    "product_discount_percentage": FieldRule("product_discount_percentage", FieldAccess.AUTO, numeric=True),
    "promotion_discount_price": FieldRule("promotion_discount_price", FieldAccess.ADMIN, numeric=True),
    "specific_gravity": FieldRule("specific_gravity", FieldAccess.STAFF, numeric=True),
    "refractive_index": FieldRule("refractive_index", FieldAccess.STAFF),
    "show_pricing_table": FieldRule("show_pricing_table", FieldAccess.ADMIN, dropdown=True),
    "callfor_price_wanto_show": FieldRule("callfor_price_wanto_show", FieldAccess.ADMIN, dropdown=True),
    "automatic_video_link": FieldRule("automatic_video_link", FieldAccess.IMAGE),
    "call_for_price_text": FieldRule("call_for_price_text", FieldAccess.ADMIN),
    "calibrated_size_range": FieldRule("calibrated_size_range", FieldAccess.CONDITIONAL),
    "beads_size": FieldRule("beads_size", FieldAccess.CONDITIONAL),
    "hole": FieldRule("hole", FieldAccess.CONDITIONAL),
    "beads_in_strand": FieldRule("beads_in_strand", FieldAccess.CONDITIONAL, numeric=True),
    "length_inches": FieldRule("length_inches", FieldAccess.CONDITIONAL, numeric=True),
    "quality_grade": FieldRule("quality_grade", FieldAccess.CONDITIONAL, dropdown=True),
    "strands": FieldRule("strands", FieldAccess.CONDITIONAL, numeric=True),
    "dimension_approx": FieldRule("dimension_approx", FieldAccess.CONDITIONAL),
    "arrangement_type": FieldRule("arrangement_type", FieldAccess.CONDITIONAL, dropdown=True),
    "length_cm": FieldRule("length_cm", FieldAccess.CONDITIONAL, numeric=True),
    "how_to_wear": FieldRule("how_to_wear", FieldAccess.SEO),
    "certificate_number1": FieldRule("certificate_number1", FieldAccess.STAFF),
    "verified_certificateimage": FieldRule("verified_certificateimage", FieldAccess.IMAGE),
    "verified_certificateimage1": FieldRule("verified_certificateimage1", FieldAccess.IMAGE),
    "additional_certification": FieldRule("additional_certification", FieldAccess.STAFF, dropdown=True),
    "price_range": FieldRule("price_range", FieldAccess.AUTO),
    "gemstone_benifits_new": FieldRule("gemstone_benifits_new", FieldAccess.SEO),
    "product_category_type": FieldRule("product_category_type", FieldAccess.AUTO, dropdown=True),
}

CREATE_REQUIRED_FIELDS: tuple[str, ...] = tuple(
    code for code, rule in FIELD_RULES.items() if rule.required_for_create
)

LOOSE_GEMSTONE_REQUIRED_FIELDS: tuple[str, ...] = tuple(
    code for code, rule in FIELD_RULES.items() if rule.required_for_loose_gemstone
)

DROPDOWN_FIELDS: tuple[str, ...] = tuple(code for code, rule in FIELD_RULES.items() if rule.dropdown)

NUMERIC_FIELDS: tuple[str, ...] = tuple(code for code, rule in FIELD_RULES.items() if rule.numeric)

NEGATIVE_ALLOWED_FIELDS: tuple[str, ...] = tuple(
    code for code, rule in FIELD_RULES.items() if rule.negative_allowed
)

NORMAL_STAFF_HIDDEN_FIELDS: tuple[str, ...] = tuple(
    code for code, rule in FIELD_RULES.items() if rule.access in {FieldAccess.ADMIN, FieldAccess.AUTO}
)
