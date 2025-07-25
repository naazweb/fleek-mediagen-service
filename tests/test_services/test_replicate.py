import pytest
from unittest.mock import patch
from app.services.replicate import ReplicateService

@pytest.mark.asyncio
@patch('replicate.async_run')
async def test_generate_image_returns_url(mock_async_run):
    """Test that generate_image returns the correct URL"""
    mock_async_run.return_value = ["https://example.com/generated-image.jpg"]
    
    service = ReplicateService()
    
    result = await service.generate_image("test prompt", width=512, height=512)
    
    mock_async_run.assert_called_once()
    assert result == "https://example.com/generated-image.jpg"

@pytest.mark.asyncio
@patch('replicate.async_run')
async def test_generate_image_returns_none_on_empty_output(mock_async_run):
    """Test that generate_image returns None when output is empty"""
    mock_async_run.return_value = []
    
    service = ReplicateService()
    
    result = await service.generate_image("test prompt")
    
    mock_async_run.assert_called_once()
    assert result is None
