# Magento Product Upload Automation System

A production-grade scaffold for a Magento / Adobe Commerce product-upload automation platform designed around GemPundit-style gemstone catalog operations.

This repo is intentionally structured like an industry codebase, not a one-file import script. It includes:

- FastAPI backend
- PostgreSQL persistence
- Alembic migrations
- Pydantic validation layer
- Magento attribute mapping engine
- CSV/Excel import pipeline
- Magento-ready CSV exporter
- Magento REST API client
- Media/image/certificate mapping pipeline
- Error report generator
- React + TypeScript admin UI
- Docker Compose stack
- Unit tests
- Real sample CSV profiling from `samples/Final_Catalog_22-04-2026.csv`

## Core workflow

```text
Staff product details / Excel / CSV / media ZIP
        ↓
Reader normalizes data
        ↓
Validation engine checks required fields, numeric fields, stock, media, SEO, duplicate SKU
        ↓
Field generator calculates ratti, price-per-carat, SEO slugs, stock flags
        ↓
Mapping engine maps human labels to Magento option IDs
        ↓
Products enter staging
        ↓
Catalog manager reviews
        ↓
System exports Magento CSV OR pushes draft products through Magento API
        ↓
Admin publishes
```

## Architecture

```text
backend/
  app/
    api/              FastAPI route layer
    core/             settings, security, logging
    db/               SQLAlchemy models/session
    domain/           Magento/GemPundit field policies
    schemas/          Pydantic request/response models
    services/         validation, mapping, CSV export, Magento client
    workers/          Celery worker stubs
    tests/            backend unit tests

frontend/
  src/
    api/              HTTP client
    components/       reusable UI components
    pages/            dashboard/upload/review/mapping pages

samples/
  Final_Catalog_22-04-2026.csv
  column_profile.json

docs/
  ARCHITECTURE.md
  FIELD_POLICY.md
  SAMPLE_CSV_PROFILE.md
  API_CONTRACT.md
```

## Quick start

### 1. Configure environment

```bash
cp .env.example .env
```

Fill Magento values only when you want API upload. CSV export works without Magento credentials.

### 2. Run with Docker

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

### 3. Run backend locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

### 4. Run tests

```bash
cd backend
pytest
```

### 5. Run frontend locally

```bash
cd frontend
npm install
npm run dev
```

## Import modes

### Mode A: Safe CSV mode

Use this first.

```text
Upload CSV/Excel → Validate → Staging → Export Magento CSV → Import in Magento Admin
```

### Mode B: Magento API draft mode

Use after mappings and validation are proven.

```text
Upload CSV/Excel → Validate → Staging → Push product drafts through API → Manual publish
```

## Important implementation notes

- The sample CSV has 157 columns and includes legacy Magento export/import columns.
- Fields `a`, `a.1`, and `a.2` are preserved through alias mapping:
  - `a` → internal/source id
  - `a.1` → source image path
  - `a.2` → automatic video link
- Existing typo `gemstone_benifits_new` is preserved because production Magento may depend on it.
- Normal staff should not touch raw Magento fields such as `attribute_set_id`, `tax_class_id`, `status`, `small_image`, `thumbnail`, or stock config flags.
- The platform defaults to creating products as disabled/draft until approved.

## Build philosophy

This codebase separates business logic from infrastructure:

- Route layer does not validate catalog rules directly.
- Validation engine is pure and testable.
- Field generation is deterministic.
- Magento API client is isolated.
- CSV export is independent of API upload.
- GemPundit-specific field behavior lives in `domain/field_policy.py`.

That means you can switch from CSV export to direct Magento API upload without rewriting validation and mapping logic.

## Final Magento Model Alignment — 2026-04-24

The codebase has been aligned to the supplied final catalogue export `report240426.csv`.

Key production decisions:

- Export column order is locked to the exact 90-column final Magento model.
- `attribute_set_id` is used as the final model field, not the older `_attribute_set` export column.
- Legacy spellings are intentionally preserved: `comment_explation`, `promotion_baseprice_jewlery`, `gemstone_benifits_new`.
- The reader supports duplicate CSV headers such as `a`, `a`, `a` by normalizing them as `a`, `a.1`, `a.2`, matching pandas-style disambiguation.
- Validation has two modes:
  - `create`: strict blocker mode for new uploads.
  - `legacy_audit`: warning-first mode for existing catalogue cleanup.
- The full `report240426.csv` is not bundled in the zip due to size. The repo includes a profile and first 100-row sample.

Useful files:

```text
backend/app/domain/magento_columns.py
backend/app/domain/field_policy.py
backend/app/services/excel_reader.py
backend/app/services/field_generation.py
backend/app/services/validation.py
backend/app/services/magento_mapper.py
docs/FINAL_CATALOG_PROFILE.md
samples/report240426_profile.json
samples/report240426_first_100_rows.csv
samples/final_model_export_preview.csv
```
