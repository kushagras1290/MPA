from pydantic import BaseModel

from app.db.enums import ErrorSeverity


class ValidationIssue(BaseModel):
    row_number: int | None = None
    sku: str | None = None
    field_name: str | None = None
    error_type: str
    error_message: str
    suggested_fix: str | None = None
    severity: ErrorSeverity = ErrorSeverity.ERROR


class ValidationResult(BaseModel):
    valid: bool
    issues: list[ValidationIssue] = []

    @property
    def blocker_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == ErrorSeverity.BLOCKER)
