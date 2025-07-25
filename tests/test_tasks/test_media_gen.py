import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.tasks.media_gen import _async_generate_media
from app.core.consts import JobStatus

@pytest.mark.asyncio
@patch('app.tasks.media_gen.Tortoise.init', new_callable=AsyncMock)
@patch('app.tasks.media_gen.Tortoise.close_connections', new_callable=AsyncMock)
@patch('app.tasks.media_gen.MediaGenerationJob.get', new_callable=AsyncMock)
@patch('app.tasks.media_gen.replicate_service.generate_image', new_callable=AsyncMock)
@patch('httpx.AsyncClient')
@patch('app.tasks.media_gen.r2_client.upload_file')
async def test_generate_media_success(mock_upload, mock_client, mock_replicate, mock_get, mock_close, mock_init):
    """Test successful media generation flow"""
    # Setup mocks
    mock_job = MagicMock()
    mock_job.save = AsyncMock()
    mock_get.return_value = mock_job
    
    mock_replicate.return_value = "https://replicate.com/image.jpg"
    
    mock_response = MagicMock()
    mock_response.content = b"image_data"
    mock_response.raise_for_status = MagicMock()
    mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
    
    mock_upload.return_value = "https://r2.com/generated/test-id.jpg"
    
    mock_task = MagicMock()
    mock_task.request.retries = 0
    
    # Execute
    await _async_generate_media(mock_task, "test-id", "test prompt", "model", 512, 512)
    
    # Verify
    assert mock_job.status == JobStatus.DONE.value
    assert mock_job.output_url == "https://r2.com/generated/test-id.jpg"
    mock_upload.assert_called_once_with(b"image_data", "generated/test-id.jpg", "image/jpeg")

@pytest.mark.asyncio
@patch('app.tasks.media_gen.Tortoise.init', new_callable=AsyncMock)
@patch('app.tasks.media_gen.Tortoise.close_connections', new_callable=AsyncMock)
@patch('app.tasks.media_gen.MediaGenerationJob.get', new_callable=AsyncMock)
@patch('app.tasks.media_gen.replicate_service.generate_image', new_callable=AsyncMock)
async def test_generate_media_failure(mock_replicate, mock_get, mock_close, mock_init):
    """Test media generation failure handling"""
    mock_job = MagicMock()
    mock_job.save = AsyncMock()
    mock_get.return_value = mock_job
    
    mock_replicate.side_effect = Exception("API Error")
    
    mock_task = MagicMock()
    mock_task.request.retries = 1
    
    # Execute and verify exception is raised
    with pytest.raises(Exception):
        await _async_generate_media(mock_task, "test-id", "test prompt", "model", 512, 512)
    
    # Verify error handling
    assert mock_job.status == JobStatus.FAILED.value
    assert mock_job.error_message == "API Error"
    assert mock_job.retries == 1