from pathlib import Path

import pandas as pd

from app.schemas.errors import ValidationIssue


class ErrorReportWriter:
    def write_excel(self, issues: list[ValidationIssue], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = [issue.model_dump(mode="json") for issue in issues]
        frame = pd.DataFrame(
            data,
            columns=[
                "row_number",
                "sku",
                "field_name",
                "error_type",
                "error_message",
                "suggested_fix",
                "severity",
            ],
        )
        frame.to_excel(output_path, index=False)
        return output_path
