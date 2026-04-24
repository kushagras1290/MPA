from pathlib import Path
from typing import Any

import pandas as pd

from app.domain.magento_columns import MAGENTO_EXPORT_COLUMNS
from app.services.magento_mapper import MagentoRowMapper


class MagentoCsvExporter:
    def __init__(self) -> None:
        self.mapper = MagentoRowMapper()

    def export(self, products: list[dict[str, Any]], output_path: Path) -> Path:
        rows = self.mapper.to_export_rows(products)
        frame = pd.DataFrame(rows, columns=list(MAGENTO_EXPORT_COLUMNS))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(output_path, index=False, encoding="utf-8-sig")
        return output_path
