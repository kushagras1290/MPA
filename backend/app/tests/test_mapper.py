from app.services.magento_mapper import MagentoRowMapper


def test_mapper_preserves_export_columns() -> None:
    row = MagentoRowMapper().to_export_row(
        {
            "sku": "GP159106",
            "name": "Amethyst - 5.11 Carats",
            "gemstone": "Amethyst",
            "origin": "Brazil",
            "treatment": "Unheated",
            "carat_weight": 5.11,
            "shape": "Oval",
            "colour": "Violet",
            "cut": "Faceted",
            "dimensions": "13.87x9.68x6.68 mm",
            "certification": "AGR Certified",
            "price": 5500,
            "qty": 1,
            "main_image": "/g/p/gp159106-1-220426.jpg",
            "description": "x",
            "short_description": "x",
            "hsn_code": "71039949",
            "dispatch_days": "0 Business Days",
            "shipping_days": 0,
            "return_policy": "10 Day Money-Back Returns*",
        }
    )
    assert row["sku"] == "GP159106"
    assert row["attribute_set_id"] == "Gemstones"
    assert row["price_per_carat"] == "1076.0000"
    assert row["weight_ratti"] == "5.62"
