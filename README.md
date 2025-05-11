# Journal API

A Flask-based REST API for managing journal entries, built with clean architecture and cloud-native deployment in mind.

## Features

- RESTful API endpoints for CRUD operations on journal entries
- PostgreSQL database integration
- Docker containerization
- Clean architecture with blueprints
- Environment-based configuration

## Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (optional)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Running the Application

### Development
```bash
flask run
```

### Production (using Docker)
```bash
docker build -t journal-api .
docker run -p 5000:5000 --env-file .env journal-api
```

## API Endpoints

- `POST /api/v1/entries` - Create a new journal entry
- `GET /api/v1/entries` - List all journal entries
- `GET /api/v1/entries/<id>` - Get a specific journal entry
- `PUT /api/v1/entries/<id>` - Update a journal entry
- `DELETE /api/v1/entries/<id>` - Delete a journal entry

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8
```

## Future Improvements

- Authentication and authorization
- Rate limiting
- API documentation with Swagger/OpenAPI
- Kubernetes deployment
- CI/CD pipeline integration
- Monitoring and logging
- Terraform infrastructure as code 