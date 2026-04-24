from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/profile_csv.py <csv-path>")

    path = Path(sys.argv[1])
    frame = pd.read_csv(path, encoding="utf-8-sig")
    profile = {
        "file": str(path),
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
        "columns_detail": [
            {
                "name": col,
                "non_null": int(frame[col].notna().sum()),
                "unique": int(frame[col].nunique(dropna=True)),
                "samples": [str(x) for x in frame[col].dropna().astype(str).unique()[:5].tolist()],
            }
            for col in frame.columns
        ],
    }
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
