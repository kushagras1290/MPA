PREMIUM_GEMSTONES: set[str] = {
    "Blue Sapphire",
    "Yellow Sapphire",
    "Ruby",
    "Emerald",
    "Pearl",
    "Red Coral",
    "Cats Eye",
    "Cat's Eye",
    "Hessonite",
}

MID_PRECIOUS_GEMSTONES: set[str] = {
    "White Sapphire",
    "Opal",
    "Aquamarine",
    "Tourmaline",
}

SEMI_PRECIOUS_GEMSTONES: set[str] = {
    "Amethyst",
    "Citrine",
    "Garnet",
    "Peridot",
    "Moonstone",
    "Topaz",
}


def classify_gemstone(gemstone: str | None) -> str:
    if not gemstone:
        return ""
    normalized = gemstone.strip()
    if normalized in PREMIUM_GEMSTONES:
        return "1 - Precious"
    if normalized in MID_PRECIOUS_GEMSTONES:
        return "2 - Mid-Precious"
    if normalized in SEMI_PRECIOUS_GEMSTONES:
        return "3 - Semi-Precious"
    return ""


HSN_BY_GEMSTONE: dict[str, str] = {
    "Red Coral": "96019040",
    "Emerald": "71039130",
    "Ruby": "71039120",
    "Blue Sapphire": "71039990",
    "Yellow Sapphire": "71039990",
    "White Sapphire": "71039990",
    "Amethyst": "71039949",
    "Citrine": "71039949",
}
