from pydantic import BaseModel, Field


class AttributeMappingCreate(BaseModel):
    attribute_code: str = Field(min_length=1)
    human_value: str = Field(min_length=1)
    magento_label: str = Field(min_length=1)
    magento_option_id: str = Field(min_length=1)
    is_active: bool = True


class AttributeMappingRead(AttributeMappingCreate):
    id: int

    model_config = {"from_attributes": True}
