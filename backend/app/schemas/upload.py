from pydantic import BaseModel


class UploadBatchRead(BaseModel):
    id: int
    source_type: str
    original_file_name: str | None
    total_rows: int
    success_count: int
    failed_count: int
    status: str

    model_config = {"from_attributes": True}


class UploadResponse(BaseModel):
    batch_id: int
    total_rows: int
    status: str
    message: str
