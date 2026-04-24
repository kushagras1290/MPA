from app.workers.celery_app import celery_app


@celery_app.task(name="catalog.noop")  # type: ignore[untyped-decorator]
def noop() -> str:
    return "ok"
