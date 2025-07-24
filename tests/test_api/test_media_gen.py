def test_generate_media_success(client):
    """
    Test case for successful media generation
    """
    payload = {
        "prompt": "A panda playing guitar on a beach",
        "width": 768,
        "height": 512,
        "model": "realistic-v1",
    }

    # Send POST request to /generate
    response = client.post("/generate", json=payload)

    assert response.status_code == 200

    # Assert the response body has the expected fields
    data = response.json()
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
