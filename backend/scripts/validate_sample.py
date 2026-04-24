from pathlib import Path

from app.services.csv_exporter import MagentoCsvExporter
from app.services.excel_reader import ProductFileReader
from app.services.validation import ProductValidator


def main() -> None:
    sample = Path(__file__).resolve().parents[2] / "samples" / "Final_Catalog_22-04-2026.csv"
    rows = ProductFileReader().read(sample)
    result = ProductValidator().validate_batch(rows)
    print(f"Rows: {len(rows)}")
    print(f"Valid: {result.valid}")
    print(f"Issues: {len(result.issues)}")
    for issue in result.issues[:20]:
        print(issue.model_dump(mode="json"))

    out = Path("/tmp/magento_sample_export.csv")
    MagentoCsvExporter().export(rows, out)
    print(f"Exported: {out}")


if __name__ == "__main__":
    main()
