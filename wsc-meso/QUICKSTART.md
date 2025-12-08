# Quick Start Guide - Mesocycle Planner API

## Prerequisites

- Python 3.10+
- Docker Desktop (for MongoDB)
- Git

## 1. Setup MongoDB with Docker

### Start MongoDB (with pre-populated exercise database)

```bash
cd wsc-meso

# Start MongoDB and Mongo Express
docker compose up -d

# Verify containers are running
docker compose ps
```

**Services started:**
- MongoDB: `localhost:27017`
- Mongo Express (Web UI): `http://localhost:8081`

The database will be automatically populated with **440+ exercises** across all muscle groups:
- Pectorals (55 exercises)
- Back/Dorsal (59 exercises)  
- Shoulders (64 exercises)
- Legs (66 exercises)
- Biceps (11 exercises)
- Triceps (10 exercises)
- Abs (15 exercises)
- Forearms (6 exercises)

### View Database

Open Mongo Express in your browser:
```
http://localhost:8081
```

Navigate to: `mesocycle_planner` → `exercises` to see all exercises.

## 2. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## 3. Run Tests

### Unit Tests (no database required)
```bash
PYTHONPATH=.:src pytest tests/unit/ -v
```

### Integration Tests (requires MongoDB)
```bash
# Make sure MongoDB is running
docker compose ps

# Run integration tests
PYTHONPATH=.:src pytest tests/integration/ -v
```

### All Tests with Coverage
```bash
PYTHONPATH=.:src pytest --cov=domain --cov=infrastructure --cov-report=html
open htmlcov/index.html
```

## 4. Start the API Server

```bash
# Set environment variables
cp .env.example .env

# Start server
PYTHONPATH=src:. uvicorn src.openapi_server.main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 5. Test the API

### Get all exercises
```bash
curl http://localhost:8000/api/v1/exercises
```

### Search exercises
```bash
curl "http://localhost:8000/api/v1/exercises/search?q=press"
```

### Filter by muscle group
```bash
curl "http://localhost:8000/api/v1/exercises?muscle_group=pectorals"
```

## Troubleshooting

### Docker not running
```bash
# Start Docker Desktop application first
# Then run:
docker compose up -d
```

### Port already in use
```bash
# Check what's using port 27017
lsof -i :27017

# Stop MongoDB
docker compose down

# Start again
docker compose up -d
```

### Database not populated
```bash
# Restart containers to trigger initialization
docker compose down -v
docker compose up -d
```

## Stop Services

```bash
# Stop containers
docker compose down

# Stop and remove volumes (deletes database)
docker compose down -v
```

## Project Structure

```
wsc-meso/
├── src/openapi_server/     # Auto-generated FastAPI code
├── domain/                 # Business logic (entities, repositories)
├── infrastructure/         # MongoDB, config
│   └── persistence/seed/   # Database initialization scripts
├── tests/                  # Unit & integration tests
├── docker-compose.yml      # MongoDB setup
└── README.md              # Full documentation
```

## Next Steps

1. ✅ MongoDB running with exercises
2. ✅ Tests passing
3. ⏳ Implement use cases in `application/`
4. ⏳ Create controllers in `api/`
5. ⏳ Connect with auto-generated routes

See [README.md](README.md) for complete documentation.
