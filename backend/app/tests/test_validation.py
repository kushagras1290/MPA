from app.services.validation import ProductValidator


def test_validator_blocks_missing_required_fields() -> None:
    result = ProductValidator().validate_product({"sku": "X", "name": "Test", "attribute_set_id": "Gemstones", "product_type": "Single Stone"}, row_number=2)
    assert not result.valid
    assert any(issue.field_name == "gemstone" for issue in result.issues)
    assert any(issue.severity == "blocker" for issue in result.issues)


def test_validator_detects_duplicate_sku_in_batch() -> None:
    product = {
        "sku": "GP1",
        "name": "A",
        "gemstone": "Amethyst",
        "origin": "Brazil",
        "treatment": "Unheated",
        "carat_weight": 1,
        "shape": "Oval",
        "colour": "Violet",
        "cut": "Faceted",
        "dimensions": "1x1x1 mm",
        "certification": "AGR Certified",
        "price": 1000,
        "qty": 1,
        "hsn_code": "71039949",
        "dispatch_days": "0 Business Days",
        "shipping_days": 0,
        "return_policy": "10 Day Money-Back Returns*",
        "main_image": "GP1-main.jpg",
        "description": "x",
        "short_description": "x",
    }
    result = ProductValidator().validate_batch([product, product])
    assert not result.valid
    assert any(issue.error_type == "duplicate" for issue in result.issues)
