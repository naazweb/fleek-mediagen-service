import replicate
from app.core.config import settings

class ReplicateService:
    def __init__(self):
        replicate.api_token = settings.REPLICATE_API_TOKEN
    
    async def generate_image(self, prompt: str, model: str = "realistic-v1", width: int = 768, height: int = 512) -> str:
        """Generate image using Replicate API and return image URL"""
        output = await replicate.async_run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_outputs": 1,
                "output_format": "jpg",
                "output_quality": 80
            }
        )
        return output[0] if output else None

replicate_service = ReplicateService()
