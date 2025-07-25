from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.core.consts import JobStatus


class MediaGenerationRequest(BaseModel):
    prompt: str
    width: int = 768
    height: int = 512
    model: str = "realistic-v1"


class MediaGenerationResponse(BaseModel):
    job_id: str
    message: str


class MediaJobResponse(BaseModel):
    id: UUID
    status: JobStatus
    retries: int
    error_message: Optional[str]
    output_url: Optional[str]
    created_at: datetime
    updated_at: datetime