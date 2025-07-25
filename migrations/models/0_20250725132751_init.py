from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "media_generation_jobs" (
    "id" UUID NOT NULL PRIMARY KEY,
    "prompt" TEXT NOT NULL,
    "model" VARCHAR(100) NOT NULL DEFAULT 'realistic-v1',
    "width" INT NOT NULL,
    "height" INT NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'queued',
    "retries" INT NOT NULL DEFAULT 0,
    "error_message" TEXT,
    "output_url" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
