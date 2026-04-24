from typing import Any, cast

import httpx

from app.core.config import settings


class MagentoApiError(RuntimeError):
    pass


def _json_object(response: httpx.Response, operation: str) -> dict[str, Any]:
    body = response.json()
    if not isinstance(body, dict):
        raise MagentoApiError(f"Magento {operation} returned a non-object JSON response.")
    return cast(dict[str, Any], body)


class MagentoClient:
    def __init__(self, base_url: str | None = None, token: str | None = None) -> None:
        self.base_url = (base_url or settings.magento_base_url).rstrip("/")
        self.token = token if token is not None else settings.magento_api_token

    @property
    def headers(self) -> dict[str, str]:
        if not self.token:
            raise MagentoApiError("Magento API token is not configured.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def sku_exists(self, sku: str) -> bool:
        url = f"{self.base_url}/rest/V1/products/{sku}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=self.headers)
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False
        raise MagentoApiError(f"Magento SKU check failed: {response.status_code} {response.text}")

    async def create_or_update_product(self, payload: dict[str, Any]) -> dict[str, Any]:
        sku = payload["product"]["sku"]
        url = f"{self.base_url}/rest/V1/products/{sku}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.put(url, headers=self.headers, json=payload)
        if response.status_code not in {200, 201}:
            raise MagentoApiError(
                f"Magento product upsert failed: {response.status_code} {response.text}"
            )
        return _json_object(response, "product upsert")

    async def set_status(self, sku: str, enabled: bool) -> dict[str, Any]:
        status = 1 if enabled else 2
        payload = {"product": {"sku": sku, "status": status}}
        return await self.create_or_update_product(payload)

    async def upload_media(self, sku: str, media_payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/rest/V1/products/{sku}/media"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, headers=self.headers, json=media_payload)
        if response.status_code not in {200, 201}:
            raise MagentoApiError(
                f"Magento media upload failed: {response.status_code} {response.text}"
            )
        return _json_object(response, "media upload")
