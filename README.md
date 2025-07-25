# Fleek MediaGen Microservice

## Quick Start with Docker

1. **Clone and setup:**
   ```bash
   git clone <repo-url>
   cd fleek-mediagen-service
   cp .env.example .env
   ```

2. **Start services:**
   ```bash
   docker-compose up --build
   ```

3. **Run migrations:**
   ```bash
   docker-compose exec app aerich upgrade
   ```

The API will be available at `http://localhost:8000`

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start services:**
   ```bash
   uvicorn app.main:app --reload
   celery -A celery_worker.celery_app worker --loglevel=info
   ```