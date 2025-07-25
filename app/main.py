from app.core.app_factory import create_app
from app.core.celery_worker import celery_app

app = create_app()
celery_app = celery_app

@app.get("/health-check")
async def health_check():
    try:
        return {"status": "healthy", "service": "MediaGen Service"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
