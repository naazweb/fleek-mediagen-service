import time  # simulate delay
from app.core.celery_worker import celery_app
from app.models.media_gen import MediaGenerationJob


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_media_task(self, job_id: str, prompt: str, model_name: str, width: int, height: int):
    """Celery task to generate media based on the provided parameters.
    args:
        job_id (str): Unique identifier for the media generation job.
        prompt (str): The prompt for media generation.
        model_name (str): The model to be used for generation.
        width (int): Width of the generated media.
        height (int): Height of the generated media.
    
    Returns:
        None
    """
    pass
