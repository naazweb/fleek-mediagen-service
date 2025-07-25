from unittest.mock import patch, MagicMock

def test_generate_media_success(client):
    """
    Test case for successful media generation
    """
    with patch('app.api.media_gen.MediaGenerationJob.create') as mock_create, \
         patch('app.api.media_gen.generate_media_task.delay') as mock_task:
        
        mock_job = MagicMock()
        mock_job.id = "test-job-id"
        mock_job.prompt = "A panda playing guitar on a beach"
        mock_job.model = "realistic-v1"
        mock_job.width = 768
        mock_job.height = 512
        mock_create.return_value = mock_job
        
        payload = {
            "prompt": "A panda playing guitar on a beach",
            "width": 768,
            "height": 512,
            "model": "realistic-v1",
        }

        response = client.post("/generate", json=payload)
        data = response.json()

        assert mock_create.called
        assert mock_task.called
        assert response.status_code == 200
        assert "job_id" in data
        assert "message" in data
        assert data["message"] == "Job queued successfully"


def test_generate_media_missing_prompt(client):
    """
    Test case for missing 'prompt' in the request payload
    """
    payload = {
        "width": 768,
        "height": 512,
        "model": "realistic-v1",
    }

    response = client.post("/generate", json=payload)

    # Assert status code is 422 Unprocessable Entity (validation failure)
    assert response.status_code == 422


def test_generate_media_invalid_width(client):
    """
    Test case for invalid 'width' in the request payload
    """
    payload = {
        "prompt": "A panda playing guitar",
        "width": "not-a-number",
        "height": 512,
        "model": "realistic-v1",
    }

    response = client.post("/generate", json=payload)

    # Assert status code is 422
    assert response.status_code == 422
