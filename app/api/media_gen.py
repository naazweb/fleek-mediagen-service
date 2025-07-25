from fastapi import APIRouter, HTTPException
from uuid import uuid4, UUID
from loguru import logger

from app.models.media_gen import MediaGenerationJob
from app.schemas.media_gen import MediaGenerationRequest, MediaGenerationResponse, MediaJobResponse
from app.tasks.media_gen import generate_media_task

router = APIRouter()


@router.post("/generate", response_model=MediaGenerationResponse)
async def generate_media(request: MediaGenerationRequest):
    """
    Generate media content using AI models.
    
    Args:
        request: Media generation parameters including prompt, model, and dimensions
        
    Returns:
        MediaGenerationResponse: Job ID and confirmation message
    """
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
    logger.info(f"Job {job_id} queued successfully")
    return MediaGenerationResponse(
        job_id=job_id,
        message="Job queued successfully"
    )


@router.get("/status/{job_id}", response_model=MediaJobResponse)
async def get_job_status(job_id: UUID):
    """
    Get the status of a media generation job.
    
    Args:
        job_id: UUID of the media generation job
        
    Returns:
        MediaJobResponse: Job details including status, output URL, and timestamps
        
    Raises:
        HTTPException: 404 if job not found
    """
    job = await MediaGenerationJob.filter(id=job_id).first()
    if not job:
        logger.warning(f"Job {job_id} not found")
        raise HTTPException(status_code=404, detail="Job not found")
    
    return MediaJobResponse(
        id=job.id,
        status=job.status,
        retries=job.retries,
        error_message=job.error_message,
        output_url=job.output_url,
        created_at=job.created_at,
        updated_at=job.updated_at
    )
