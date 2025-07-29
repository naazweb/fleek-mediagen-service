# Fleek MediaGen Microservice

A scalable, asynchronous microservice for AI-powered media generation using Replicate API with persistent storage in Cloudflare R2.

## Architecture Overview

This microservice follows a clean, modular architecture with clear separation of concerns:

### Core Components

1. **API Layer (FastAPI)**
   - RESTful endpoints for media generation requests and status checks
   - Request validation using Pydantic models
   - Async request handling

2. **Task Queue (Celery)**
   - Asynchronous job processing with Redis as broker/backend
   - Automatic retries with exponential backoff
   - Proper error handling and status tracking

3. **Storage Services**
   - **Database**: PostgreSQL with Tortoise ORM for job metadata
   - **Object Storage**: Cloudflare R2 (S3-compatible) for media files

4. **External Services**
   - **Replicate API**: AI model integration for image generation
   - Mock implementation for testing/development

### Data Flow

1. Client submits generation request → API validates and creates job → Job queued in Celery
2. Worker processes job → Calls Replicate API → Downloads generated image
3. Image uploaded to Cloudflare R2 → Job status and URL updated in database
4. Client can check job status and retrieve result URL when complete

## Technology Stack

- **Framework**: FastAPI (async Python web framework)
- **Task Queue**: Celery with Redis
- **Database**: PostgreSQL with Tortoise ORM (async)
- **Storage**: Cloudflare R2 (via boto3 S3 client)
- **AI Integration**: Replicate API
- **Containerization**: Docker & Docker Compose
- **Migration**: Aerich (for Tortoise ORM)
- **Testing**: pytest with async support
- **Logging**: Loguru

## Project Structure

```
├── app/                      # Application code
│   ├── api/                  # API endpoints
│   │   ├── media_gen.py      # Media generation endpoints
│   │   └── router.py         # API router configuration
│   ├── core/                 # Core application components
│   │   ├── app_factory.py    # FastAPI application factory
│   │   ├── celery_worker.py  # Celery configuration
│   │   ├── config.py         # Application settings
│   │   ├── consts.py         # Constants and enums
│   │   └── logging.py        # Logging configuration
│   ├── models/               # Database models
│   │   └── media_gen.py      # Media generation job model
│   ├── schemas/              # Pydantic schemas
│   │   └── media_gen.py      # Request/response schemas
│   ├── services/             # External service integrations
│   │   ├── cloudflare.py     # Cloudflare R2 client
│   │   └── replicate.py      # Replicate API client
│   └── tasks/                # Celery tasks
│       └── media_gen.py      # Media generation task
├── migrations/              # Database migrations
└── tests/                   # Test suite
    ├── test_api/            # API tests
    ├── test_services/       # Service tests
    └── test_tasks/          # Task tests
```

## Key Services

### Replicate Service

The `ReplicateService` handles image generation through the Replicate API:

- Async interface for API calls
- Configurable model selection
- Mock mode for testing/development (generates placeholder images)
- Error handling and logging

### Cloudflare R2 Client

The `CloudflareR2Client` manages media file storage:

- S3-compatible API via boto3
- Secure credential management
- Configurable bucket and endpoint
- Public URL generation for stored media

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL (for local development)
- Redis (for local development)

### Environment Configuration

1. **Clone and setup:**
   ```bash
   git clone <repo-url>
   cd fleek-mediagen-service
   cp .env.example .env
   ```

2. **Configure environment variables in `.env`:**

### Docker Deployment

1. **Start services:**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations:**
   ```bash
   docker-compose exec app aerich upgrade
   ```

The API will be available at `http://localhost:8000`

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start services:**
   ```bash
   uvicorn app.main:app --reload
   celery -A app.main.celery_app worker --loglevel=info
   ```

### Endpoints

- `POST /generate`: Submit a new media generation job
- `GET /status/{job_id}`: Check the status of a job
- `GET /health-check`: Service health check

## Testing

Run the test suite with:

```bash
python manage.py test
```

For development, you can enable mock mode for Replicate API by setting `MOCK_REPLICATE=True` in your `.env` file.
        
