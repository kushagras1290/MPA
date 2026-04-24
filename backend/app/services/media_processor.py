import shutil
import zipfile
from pathlib import Path

from PIL import Image

from app.core.config import settings

ALLOWED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


class UnsafeArchiveError(ValueError):
    pass


class MediaProcessor:
    def safe_extract_zip(self, archive_path: Path, target_dir: Path) -> list[Path]:
        target_dir.mkdir(parents=True, exist_ok=True)
        extracted: list[Path] = []

        with zipfile.ZipFile(archive_path) as archive:
            for member in archive.infolist():
                member_path = Path(member.filename)
                if member_path.is_absolute() or ".." in member_path.parts:
                    raise UnsafeArchiveError(f"Unsafe ZIP path: {member.filename}")
                if member.is_dir():
                    continue
                destination = target_dir / member_path.name
                with archive.open(member) as src, destination.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                extracted.append(destination)

        return extracted

    def validate_image(self, path: Path) -> bool:
        if path.suffix.lower() not in ALLOWED_IMAGE_SUFFIXES:
            return False
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def match_by_sku(self, media_files: list[Path]) -> dict[str, list[Path]]:
        matches: dict[str, list[Path]] = {}
        for file_path in media_files:
            stem = file_path.stem.lower()
            # GP159106-main -> gp159106
            sku = stem.split("-")[0].upper()
            matches.setdefault(sku, []).append(file_path)
        return matches

    def public_url_for_catalog_path(self, catalog_path: str) -> str:
        if catalog_path.startswith("http://") or catalog_path.startswith("https://"):
            return catalog_path
        return f"{settings.media_public_base_url.rstrip('/')}/{catalog_path.lstrip('/')}"
