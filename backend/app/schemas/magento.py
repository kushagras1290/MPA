from pydantic import BaseModel


class MagentoPushResponse(BaseModel):
    product_id: str | None = None
    sku: str
    status: str
    message: str
