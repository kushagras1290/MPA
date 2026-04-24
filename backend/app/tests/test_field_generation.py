from app.services.field_generation import generate_fields, slugify


def test_slugify_generates_clean_slug() -> None:
    assert slugify("Natural Blue Sapphire 3.25 Carat!") == "natural-blue-sapphire-3-25-carat"


def test_generate_fields_calculates_ratti_and_price_per_carat() -> None:
    product = {
        "sku": "GP159106",
        "name": "Amethyst - 5.11 Carats",
        "gemstone": "Amethyst",
        "origin": "Brazil",
        "treatment": "Unheated and Untreated",
        "carat_weight": 5.11,
        "shape": "Oval",
        "colour": "Violet",
        "cut": "Faceted",
        "dimensions": "13.87x9.68x6.68 mm",
        "certification": "AGR Certified",
        "price": 5500,
        "qty": 1,
        "main_image": "/g/p/gp159106-1-220426.jpg",
    }
    enriched = generate_fields(product)

    assert enriched["weight_ratti"] == "5.62"
    assert enriched["price_per_carat"] == "1076.0000"
    assert enriched["is_in_stock"] == "1"
    assert enriched["url_key"] == "amethyst-5-11-carats-gp159106"
    assert enriched["image"] == "/g/p/gp159106-1-220426.jpg"
