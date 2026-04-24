from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services.excel_template import ExcelTemplateGenerator

router = APIRouter()


@router.get("/product-upload")
def download_product_upload_template() -> FileResponse:
    dropdowns = {
        "gemstone": [
            "Amethyst",
            "Red Coral",
            "Emerald",
            "White Sapphire",
            "Citrine",
            "Blue Sapphire",
            "Ruby",
        ],
        "origin": ["Brazil", "Italy", "Zambia", "Sri Lanka (Ceylon)", "Myanmar (Burma)"],
        "shape": ["Oval", "Cushion", "Triangular", "Cylinder", "Octagonal", "Round"],
        "cut": ["Faceted", "Cabochon"],
        "cutting_style": ["Faceted", "Cabochon"],
        "certification": [
            "AGR Certified",
            "ITLGR Certified",
            "IIGJ Certified",
            "Free Lab Certificate",
        ],
        "vendor": ["GP", "Vendor_IN"],
        "return_policy": ["10 Day Money-Back Returns*"],
    }
    temp = NamedTemporaryFile(delete=False, suffix=".xlsx")
    output_path = Path(temp.name)
    temp.close()
    ExcelTemplateGenerator().generate(output_path, dropdowns=dropdowns)
    return FileResponse(
        output_path,
        filename="magento_product_upload_template.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
