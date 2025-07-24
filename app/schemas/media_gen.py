from pydantic import BaseModel


class MediaGenerationRequest(BaseModel):
    prompt: str
    width: int = 768
    height: int = 512
    model: str = "realistic-v1"


class MediaGenerationResponse(BaseModel):
    job_id: str
    message: str