import pytest
from unittest.mock import patch
from app.services.replicate import ReplicateService

@pytest.mark.asyncio
@patch('app.services.replicate.settings.MOCK_REPLICATE', False)
@patch('replicate.async_run')
async def test_generate_image_returns_url(mock_async_run):
    """Test that generate_image returns the correct URL"""
    mock_async_run.return_value = ["https://example.com/generated-image.jpg"]
    
    service = ReplicateService()
    
    result = await service.generate_image("test prompt", width=512, height=512)
    
    assert result == "https://example.com/generated-image.jpg"

@pytest.mark.asyncio
@patch('app.services.replicate.settings.MOCK_REPLICATE', False)
@patch('replicate.async_run')
async def test_generate_image_returns_none_on_empty_output(mock_async_run):
    """Test that generate_image returns None when output is empty"""
    mock_async_run.return_value = []
    
    service = ReplicateService()
    
    result = await service.generate_image("test prompt")
    
    assert result is None

@patch('app.services.replicate.settings.MOCK_REPLICATE', True)
def test_generate_mock_image():
    """Test mock image generation when MOCK_REPLICATE is enabled"""
    service = ReplicateService()
    
    result = service._generate_mock_image("test prompt", 512, 512)
    
    assert result.startswith("data:image/jpeg;base64,")
    assert len(result) > 50  # Should contain base64 data
