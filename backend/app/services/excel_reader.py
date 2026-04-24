import csv
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pandas as pd

from app.services.normalizer import normalize_row


class ProductFileReader:
    SUPPORTED_SUFFIXES = {".csv", ".xlsx", ".xls"}

    def iter_rows(self, path: Path) -> Iterator[dict[str, Any]]:
        suffix = path.suffix.lower()
        if suffix not in self.SUPPORTED_SUFFIXES:
            raise ValueError(f"Unsupported file type: {suffix}")

        if suffix == ".csv":
            with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
                raw_reader = csv.reader(handle)
                try:
                    raw_headers = next(raw_reader)
                except StopIteration:
                    return
                headers = _deduplicate_headers(raw_headers)
                for raw_row in raw_reader:
                    padded = raw_row + [None] * max(0, len(headers) - len(raw_row))
                    row = dict(zip(headers, padded, strict=False))
                    yield normalize_row(row)
            return

        frame = pd.read_excel(path, dtype=str)
        frame = frame.where(pd.notna(frame), None)
        for row in frame.to_dict(orient="records"):
            yield normalize_row(row)

    def read(self, path: Path, max_rows: int | None = None) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for index, row in enumerate(self.iter_rows(path), start=1):
            if max_rows is not None and index > max_rows:
                break
            rows.append(row)
        return rows


def _deduplicate_headers(headers: list[str]) -> list[str]:
    counts: defaultdict[str, int] = defaultdict(int)
    result: list[str] = []
    for header in headers:
        clean = str(header).strip()
        seen = counts[clean]
        result.append(clean if seen == 0 else f"{clean}.{seen}")
        counts[clean] += 1
    return result
