# Architecture

## Goal

Build a controlled Magento product automation platform that prevents raw spreadsheet chaos from reaching production.

## Components

```text
React Admin UI
  ↓
FastAPI API
  ↓
Service Layer
  ↓
PostgreSQL Staging Database
  ↓
CSV Exporter / Magento REST API Client
  ↓
Magento
```

## Backend modules

| Module | Responsibility |
|---|---|
| `api` | HTTP routing only |
| `schemas` | Request/response models |
| `domain` | Field rules, Magento columns, GemPundit taxonomy |
| `services.validation` | Product validation |
| `services.field_generation` | Derived fields |
| `services.magento_mapper` | Magento CSV/API shape |
| `services.media_processor` | Image/certificate/video ZIP handling |
| `services.magento_client` | REST API wrapper |
| `db` | SQLAlchemy persistence |
| `workers` | Background processing |

## Product safety model

Products should be created as `disabled/draft` first. Publishing is a separate admin action.

Direct auto-publishing is intentionally avoided in the base system because one dirty file can wreck catalog quality.
