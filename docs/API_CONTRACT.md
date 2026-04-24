# API Contract

## Health

```http
GET /api/health
```

## Template

```http
GET /api/templates/product-upload
```

Returns Excel template with dropdowns and example row.

## Upload product file

```http
POST /api/uploads/product-file
Content-Type: multipart/form-data
file=<csv/xlsx/xls>
```

Response:

```json
{
  "batch_id": 1,
  "total_rows": 52,
  "status": "validated",
  "message": "Products validated and staged for approval."
}
```

## Download Magento CSV

```http
GET /api/uploads/{batch_id}/magento-csv
```

## Download error report

```http
GET /api/uploads/{batch_id}/error-report
```

## Staged products

```http
GET /api/products/staging
```

## Approve product

```http
POST /api/products/staging/{product_id}/approve
```

## Reject product

```http
POST /api/products/staging/{product_id}/reject
```

## Mappings

```http
GET /api/mappings
POST /api/mappings
```

## Push Magento draft

```http
POST /api/magento/products/{product_id}/push-draft
```

Creates/updates product in Magento with `status=2` by default.
