import asyncio
import httpx
from app.core.celery_worker import celery_app
from app.models.media_gen import MediaGenerationJob
from app.services.replicate import replicate_service
from app.services.cloudflare import r2_client
from app.core.consts import JobStatus
from tortoise import Tortoise


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3, retry_jitter=True)
def generate_media_task(self, job_id: str, prompt: str, model_name: str, width: int, height: int):
    """
    Celery task to generate media based on the provided parameters.
    
    Args:
        job_id (str): Unique identifier for the media generation job
        prompt (str): Text prompt for image generation
        model_name (str): AI model to use for generation
        width (int): Width of the generated image
        height (int): Height of the generated image
    
    Returns:
        None: Updates job status in database
    
    Raises:
        Exception: Re-raises exceptions for Celery retry logic
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(_async_generate_media(self, job_id, prompt, model_name, width, height))


async def _async_generate_media(task, job_id: str, prompt: str, model_name: str, width: int, height: int):
    """
    Async implementation of media generation task.
    
    Complete pipeline:
    1. Update job status to PROCESSING
    2. Generate image using Replicate API
    3. Download generated image
    4. Upload to Cloudflare R2 storage
    5. Update job status to DONE with output URL
    
    On failure:
    - Updates job status to FAILED
    - Stores error message and retry count
    - Re-raises exception for Celery retry logic
    
    Args:
        task: Celery task instance for retry tracking
        job_id (str): Database job identifier
        prompt (str): Image generation prompt
        model_name (str): AI model name
        width (int): Image width
        height (int): Image height
    
    Raises:
        Exception: Any error during the generation pipeline
    """
    from app.core.config import settings
    await Tortoise.init(config=settings.tortoise_config)
    
    try:
        job = await MediaGenerationJob.get(id=job_id)
        job.status = JobStatus.PROCESSING.value
        await job.save()
        
        # Generate image using Replicate
        image_url = await replicate_service.generate_image(prompt, model_name, width, height)
        if not image_url:
            raise Exception("Failed to generate image")
        
        # Download image
        if image_url.startswith('data:image/'):
            # Handle base64 data URL from mock
            import base64
            image_data = base64.b64decode(image_url.split(',')[1])
        else:
            # Download from URL
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                image_data = response.content
        
        # Upload to Cloudflare R2
        key = f"generated/{job_id}.jpg"
        public_url = r2_client.upload_file(image_data, key, "image/jpeg")
        
        # Update job with success
        job.status = JobStatus.DONE.value
        job.output_url = public_url
        await job.save()
        
    except Exception as e:
        # Update job with error
        job = await MediaGenerationJob.get(id=job_id)
        job.status = JobStatus.FAILED.value
        job.error_message = str(e)
        job.retries = task.request.retries
        await job.save()
        
        # Re-raise for Celery retry logic
        raise e
    
    finally:
        await Tortoise.close_connections()
