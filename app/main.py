from fastapi import FastAPI
from app.api.router import api_router
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings

app = FastAPI()
register_tortoise(
    app,
    config=settings.tortoise_config,
    generate_schemas=False,
    add_exception_handlers=True,
)
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
