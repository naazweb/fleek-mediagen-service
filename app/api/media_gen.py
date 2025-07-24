from fastapi import APIRouter
from uuid import uuid4
from app.schemas.media_gen import MediaGenerationRequest, MediaGenerationResponse

router = APIRouter()


@router.post("/generate", response_model=MediaGenerationResponse)
async def generate_media(request: MediaGenerationRequest):
    job_id = str(uuid4())
    # TODO: Send to media generation queue
    return MediaGenerationResponse(
        job_id=job_id,
        message="Job queued successfully"
    )

