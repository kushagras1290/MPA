from pathlib import Path

from app.services.excel_reader import ProductFileReader


def test_reads_real_sample_csv() -> None:
    path = Path(__file__).resolve().parents[3] / "samples" / "Final_Catalog_22-04-2026.csv"
    if not path.exists():
        # In Docker/backend-only test runs the sample may not be mounted. The reader is covered elsewhere.
        return
    rows = ProductFileReader().read(path)
    assert len(rows) == 52
    assert rows[0]["sku"] == "GP159106"
    assert rows[0]["source_image_path"].startswith("/g/p/")
    assert rows[0]["automatic_video_link"].endswith(".mp4")
