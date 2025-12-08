# Mesocycle Planner - Testing Guide

## Running Tests

### All Tests
```bash
cd wsc-meso
source venv/bin/activate
pip install -r requirements-test.txt
pytest
```

### Unit Tests Only
```bash
pytest tests/unit/
```

### Integration Tests Only
```bash
# Make sure MongoDB is running
docker-compose up -d mongodb
pytest tests/integration/
```

### With Coverage Report
```bash
pytest --cov=domain --cov=infrastructure --cov-report=html
open htmlcov/index.html
```

## Test Structure

```
tests/
├── unit/                  # Unit tests (no external dependencies)
│   └── test_domain_entities.py
├── integration/           # Integration tests (with MongoDB)
│   └── test_repositories.py
└── e2e/                   # End-to-end tests (full API)
    └── test_api.py
```

## Docker Setup for Testing

### Start MongoDB for tests
```bash
docker-compose up -d mongodb
```

### View MongoDB data
```bash
# Access Mongo Express at http://localhost:8081
docker-compose up -d mongo-express
```

### Stop services
```bash
docker-compose down
```

## Test Database

Integration tests use a separate test database: `mesocycle_planner_test`

This database is automatically created and cleaned up after each test run.
