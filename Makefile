.PHONY: up down api web test lint profile-sample

up:
	docker compose up --build

down:
	docker compose down

api:
	cd backend && uvicorn app.main:app --reload

web:
	cd frontend && npm run dev

test:
	cd backend && pytest

profile-sample:
	cd backend && python scripts/profile_csv.py ../samples/Final_Catalog_22-04-2026.csv
