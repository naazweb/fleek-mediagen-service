from unittest.mock import patch, MagicMock
from app.services.cloudflare import CloudflareR2Client

@patch('boto3.client')
def test_upload_file_returns_url(mock_boto3):
    """Test that upload_file returns the correct URL"""
    mock_client = MagicMock()
    mock_boto3.return_value = mock_client
    
    r2_client = CloudflareR2Client()
    
    file_data = b"test image data"
    key = "test-image.jpg"
    
    result = r2_client.upload_file(file_data, key)
    
    mock_client.put_object.assert_called_once()
    assert result.startswith("https://")
    assert key in result
