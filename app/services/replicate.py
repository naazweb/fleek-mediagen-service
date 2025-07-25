import replicate
from PIL import Image, ImageDraw
import io
from loguru import logger
from app.core.config import settings

class ReplicateService:
    def __init__(self):
        replicate.api_token = settings.REPLICATE_API_TOKEN
    
    async def generate_image(self, prompt: str, model: str = "realistic-v1", width: int = 768, height: int = 512) -> str:
        """Generate image using Replicate API or mock PIL image"""
        if settings.MOCK_REPLICATE:
            logger.info(f"Using mock image generation for prompt: {prompt[:50]}...")
            return self._generate_mock_image(prompt, width, height)
        
        logger.info(f"Calling Replicate API for prompt: {prompt[:50]}...")
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
    
    def _generate_mock_image(self, prompt: str, width: int, height: int) -> str:
        """Generate a mock image using PIL"""
        img = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add text with prompt
        text = f"Mock: {prompt[:50]}..."
        draw.text((10, 10), text, fill='black')
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Return base64 data URL for mock
        import base64
        img_b64 = base64.b64encode(img_bytes.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_b64}"

replicate_service = ReplicateService()
