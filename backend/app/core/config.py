from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["local", "dev", "staging", "production"] = "local"
    app_name: str = "Magento Product Automation"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173"]

    database_url: str = "sqlite:///./catalog.db"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720

    magento_base_url: str = "https://www.example.com"
    magento_api_token: str = ""
    magento_store_view: str = "admin"
    magento_default_attribute_set_id: int = 4
    magento_default_tax_class_id: int = 2
    magento_default_website: str = "base"

    media_base_path: Path = Path("/tmp/catalog-media")
    media_public_base_url: str = "https://imgcdn1.gempundit.com/media/catalog/product"

    upload_max_file_mb: int = 100
    default_product_status: int = 2
    default_product_visibility: int = 4
    default_product_type: str = "simple"
    default_product_weight: float = 0.15

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
