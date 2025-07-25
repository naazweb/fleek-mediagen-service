from fastapi import APIRouter
from uuid import uuid4, UUID

from app.models.media_gen import MediaGenerationJob
from app.schemas.media_gen import MediaGenerationRequest, MediaGenerationResponse
from app.tasks.media_gen import generate_media_task

router = APIRouter()


@router.post("/generate", response_model=MediaGenerationResponse)
async def generate_media(request: MediaGenerationRequest):
    job_id = str(uuid4())
    job = await MediaGenerationJob.create(
        id=job_id,
        prompt=request.prompt,
        model=request.model,
        width=request.width,
        height=request.height,
        status="queued",
    )
    generate_media_task.delay(
        job_id=str(job.id),
        prompt=job.prompt,
        model_name=job.model,
        width=job.width,
        height=job.height,
    )
    return MediaGenerationResponse(
        job_id=job_id,
        message="Job queued successfully"
    )

