from fastapi import APIRouter

from app.api.routes import health, magento, mappings, products, templates, uploads

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(mappings.router, prefix="/mappings", tags=["mappings"])
api_router.include_router(magento.router, prefix="/magento", tags=["magento"])
