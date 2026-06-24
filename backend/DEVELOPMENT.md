# Development setup guide for CricAuction Backend

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- Git
- Postman or similar API testing tool

## Environment Setup

### 1. Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate
```

### 2. Environment Configuration

```bash
# Copy example env
cp .env.example .env

# Edit .env with your settings
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/cricsauction
SECRET_KEY=your-secret-key-here
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 3. Database Setup

```bash
# Create database (MySQL)
mysql -u root -p
mysql> CREATE DATABASE cricsauction;
mysql> exit;

# Or use Docker
docker run --name mysql-cric -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=cricsauction -p 3306:3306 -d mysql:8.0
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs

## Database Management

### Create Tables
Tables are created automatically on first run, but you can manually create them:

```bash
python -c "from app.db.database import create_db_and_tables; create_db_and_tables()"
```

### Initialize Default Roles

```bash
python -m app.db.init
```

### Database Migrations (Alembic)

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

## API Testing

### Using Swagger UI
Visit: http://localhost:8000/docs

### Using cURL

**Register User**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "player"
  }'
```

**Login**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Get Users**
```bash
curl -X GET "http://localhost:8000/api/v1/users"
```

### Using Postman
1. Import the API documentation
2. Set base URL: http://localhost:8000
3. Set auth header: `Authorization: Bearer <token>`

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_auth.py -v

# Run specific test
pytest app/tests/test_auth.py::test_register_user -v
```

## Code Structure

### Models (app/models/)
- Define database schema using SQLModel

### Schemas (app/schemas/)
- Define request/response validation using Pydantic

### Repositories (app/repositories/)
- Handle database operations

### Services (app/services/)
- Contain business logic

### API Routes (app/api/v1/)
- Define API endpoints

## Common Tasks

### Add New Entity

1. Create model in `app/models/models.py`
2. Create schema in `app/schemas/entity.py`
3. Create repository in `app/repositories/entity_repository.py`
4. Create service in `app/services/entity_service.py`
5. Create routes in `app/api/v1/entity/routes.py`

### Add New Endpoint

1. Add method in service
2. Add route in API handler
3. Test with Swagger UI or cURL

### Database Migration

1. Make model changes
2. Run: `alembic revision --autogenerate -m "description"`
3. Review generated migration
4. Run: `alembic upgrade head`

## Troubleshooting

### Database Connection Error
- Check DATABASE_URL in .env
- Ensure MySQL is running
- Verify credentials

### Port Already in Use
```bash
# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On Unix
lsof -ti :8000 | xargs kill -9
```

### Module Import Errors
```bash
# Ensure you're in virtual environment
pip install -r requirements.txt --force-reinstall
```

### SMTP Error
- Generate app-specific password for Gmail
- Verify SMTP credentials in .env

## Performance Tips

1. Use database indexes on frequently queried columns
2. Implement pagination for list endpoints
3. Cache frequently accessed data with Redis
4. Use connection pooling (configured in SQLModel)
5. Monitor slow queries in logs

## Security Best Practices

1. Never commit `.env` file
2. Use strong SECRET_KEY (generate: `openssl rand -hex 32`)
3. Enable HTTPS in production
4. Implement rate limiting
5. Validate all inputs
6. Use CORS carefully
7. Hash passwords (done with passlib)
8. Implement audit logging

## Deployment

### Docker
```bash
docker-compose up -d
```

### Traditional Server
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Useful Commands

```bash
# Check dependencies
pip list

# Update dependencies
pip install --upgrade -r requirements.txt

# Generate requirements
pip freeze > requirements.txt

# Run linting
flake8 app/

# Format code
black app/

# Type checking
mypy app/
```

## Resources

- FastAPI: https://fastapi.tiangolo.com/
- SQLModel: https://sqlmodel.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- MySQL: https://dev.mysql.com/doc/
- Alembic: https://alembic.sqlalchemy.org/

## Support

For issues, check:
1. Error logs
2. Database connectivity
3. Environment variables
4. Python version compatibility
