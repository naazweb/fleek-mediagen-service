from fastapi import FastAPI

from app.core.celery_worker import celery_app

app = FastAPI()
celery_app = celery_app

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
