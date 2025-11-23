# User Service - Development Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **PDM**: Python dependency manager
  ```bash
  pip install --user pdm
  ```
- **Docker Desktop**: [Download Docker](https://www.docker.com/products/docker-desktop/)
  - For WSL2 users, enable WSL integration in Docker Desktop settings
- **Git**: [Download Git](https://git-scm.com/downloads)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Emmanuel-Oyewole/user-service.git
cd user-service
```

### 2. Install Python Dependencies

```bash
# Install all project dependencies
pdm install
```

This will create a virtual environment and install all required packages including:

- FastAPI
- SQLAlchemy
- Alembic
- asyncpg
- Redis
- RabbitMQ clients
- And more...

### 3. Configure Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

**Important:** The default `.env` is configured for local development with Docker. Key settings:

```env
# Service
SERVICE_NAME=User-service
SERVICE_MODE=development
DEBUG=True

# Postgres (Local Docker)
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=userservicedb
POSTGRES_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=password

# RabbitMQ
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=password
RABBITMQ_DEFAULT_HOST=localhost
RABBITMQ_DEFAULT_PORT=5672
```

### 4. Start Docker Services

Start PostgreSQL, Redis, RabbitMQ, and pgAdmin using Docker Compose:

```bash
docker compose -f docker-compose.dev.yml up -d
```

**Verify all services are running:**

```bash
docker compose -f docker-compose.dev.yml ps
```

You should see:

- ✅ `user_service_postgres` - Running on port 5432
- ✅ `user_service_redis` - Running on port 6379
- ✅ `user_service_rabbitmq` - Running on ports 5672 & 15672
- ✅ `user_service-pgadmin-dev` - Running on port 5050

**Check service logs:**

```bash
# View all logs
docker compose -f docker-compose.dev.yml logs

# View specific service logs
docker logs user_service_postgres
docker logs user_service_redis
docker logs user_service_rabbitmq
```

### 5. Run Database Migrations

Create and apply database migrations using Alembic:

```bash
# Generate migration from your models
pdm run alembic revision --autogenerate -m "initial migration"

# Apply migrations to database
pdm run alembic upgrade head
```

**Verify tables were created:**

Access pgAdmin at http://localhost:5050 (credentials: `admin@admin.com` / `user123`)

Or use psql:

```bash
PGPASSWORD=postgres psql -h localhost -U postgres -d userservicedb -c "\dt"
```

### 6. Run the Application

#### Start FastAPI Server

```bash
pdm run dev
```

The API will be available at:

- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Start gRPC Server

In a separate terminal:

```bash
pdm run grpc
```

The gRPC server will run on port `50051`.

**To test the gRPC server:**

```bash
# In another terminal, run the example client
pdm run python examples/grpc_client_example.py
```

See the [gRPC Guide](docs/GRPC_GUIDE.md) for comprehensive documentation on using gRPC.

## 🎯 Quick Reference

### Docker Commands

```bash
# Start all services
docker compose -f docker-compose.dev.yml up -d

# Stop all services
docker compose -f docker-compose.dev.yml down

# Stop and remove volumes (⚠️ deletes all data)
docker compose -f docker-compose.dev.yml down -v

# Restart a specific service
docker compose -f docker-compose.dev.yml restart postgres

# View logs
docker compose -f docker-compose.dev.yml logs -f
```

### Alembic Migration Commands

```bash
# Create a new migration
pdm run alembic revision --autogenerate -m "description"

# Apply all pending migrations
pdm run alembic upgrade head

# Rollback one migration
pdm run alembic downgrade -1

# View migration history
pdm run alembic history

# Show current revision
pdm run alembic current
```

### PDM Commands

```bash
# Install dependencies
pdm install

# Add a new dependency
pdm add package-name

# Add a dev dependency
pdm add -d package-name

# Update dependencies
pdm update

# Run scripts
pdm run dev        # Start FastAPI server
pdm run grpc       # Start gRPC server
pdm run gen-proto  # Generate Python code from .proto files
```

### gRPC Commands

```bash
# Generate Python code from proto files
pdm run gen-proto

# Start gRPC server
pdm run grpc

# Test gRPC with example client
pdm run python examples/grpc_client_example.py
```

## 🔧 Accessing Services

### PostgreSQL Database

**Via pgAdmin (Web UI):**

1. Open http://localhost:5050
2. Login: `admin@admin.com` / `user123`
3. Add server with these settings:
   - **Name**: User Service DB
   - **Host**: `user_service_postgres`
   - **Port**: `5432`
   - **Database**: `userservicedb`
   - **Username**: `postgres`
   - **Password**: `postgres`

**Via psql (Command Line):**

```bash
PGPASSWORD=postgres psql -h localhost -U postgres -d userservicedb
```

**Connection String:**

```
postgresql://postgres:postgres@localhost:5432/userservicedb
```

### Redis

**Via Redis CLI:**

```bash
docker exec -it user_service_redis redis-cli -a password
```

**Test connection:**

```bash
redis-cli -h localhost -p 6379 -a password ping
```

### RabbitMQ

**Management UI:**

- URL: http://localhost:15672
- Username: `admin`
- Password: `password`

**AMQP Connection:**

- Host: `localhost`
- Port: `5672`
- Username: `admin`
- Password: `password`

## 🧪 Running Tests

```bash
# Run all tests
pdm run pytest

# Run with coverage
pdm run pytest --cov=src --cov-report=html

# Run specific test file
pdm run pytest tests/test_users.py

# Run with verbose output
pdm run pytest -v
```

## 🐛 Troubleshooting

### Docker Issues

**Problem: "Cannot connect to Docker daemon"**

```bash
# Start Docker Desktop
# For WSL2, ensure WSL integration is enabled in Docker Desktop settings
```

**Problem: Port already in use**

```bash
# Check what's using the port
sudo lsof -i :5432  # or :6379, :5672, etc.

# Stop the conflicting service or change the port in docker-compose.dev.yml
```

**Problem: Containers won't start**

```bash
# Remove all containers and volumes, then restart
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d
```

### Database Issues

**Problem: "password authentication failed for user postgres"**

```bash
# Remove volumes and recreate database
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d postgres

# Wait 10 seconds for PostgreSQL to initialize
sleep 10

# Run migrations again
pdm run alembic upgrade head
```

**Problem: Alembic can't find tables**

```bash
# Ensure models are imported in src/models/__init__.py
# Verify Base.metadata contains tables:
pdm run python -c "from src.models import Base; print(list(Base.metadata.tables.keys()))"
```

### Python/PDM Issues

**Problem: Module not found errors**

```bash
# Reinstall dependencies
pdm install

# Clear cache and reinstall
rm -rf .venv
pdm install
```

**Problem: Wrong Python version**

```bash
# Check Python version
python --version

# Use specific Python version with PDM
pdm use python3.11
pdm install
```

## 📁 Project Structure

```
user-service/
├── src/
│   ├── api/              # FastAPI routers
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── grpc/             # gRPC service definitions
│   ├── config/           # Configuration & settings
│   ├── utils/            # Utility functions
│   └── main.py           # FastAPI application entry point
├── migration/            # Alembic migrations
│   ├── versions/         # Migration files
│   └── env.py            # Alembic environment config
├── tests/                # Test files
├── proto/                # gRPC proto files
├── docs/                 # Documentation
├── docker-compose.dev.yml # Docker services for development
├── .env                  # Environment variables
├── pyproject.toml        # PDM dependencies & project config
├── alembic.ini           # Alembic configuration
└── README.md             # Project overview
```

## 🔐 Security Notes

⚠️ **Important:** The default credentials are for **development only**.

For production:

1. Use strong, unique passwords
2. Store secrets in a secure vault (AWS Secrets Manager, HashiCorp Vault, etc.)
3. Enable SSL/TLS for all services
4. Use environment-specific `.env` files
5. Never commit `.env` files to version control

## 🤝 Team Workflow

### Daily Development

1. **Pull latest changes:**

   ```bash
   git pull origin main
   ```

2. **Update dependencies:**

   ```bash
   pdm install
   ```

3. **Start Docker services:**

   ```bash
   docker compose -f docker-compose.dev.yml up -d
   ```

4. **Apply any new migrations:**

   ```bash
   pdm run alembic upgrade head
   ```

5. **Start development server:**
   ```bash
   pdm run dev
   ```

### Creating Database Changes

1. **Modify models** in `src/models/`

2. **Generate migration:**

   ```bash
   pdm run alembic revision --autogenerate -m "add user profile fields"
   ```

3. **Review migration** in `migration/versions/`

4. **Apply migration:**

   ```bash
   pdm run alembic upgrade head
   ```

5. **Commit changes:**
   ```bash
   git add migration/versions/* src/models/*
   git commit -m "feat: add user profile fields"
   git push
   ```

### Before Committing

1. Run tests: `pdm run pytest`
2. Check code formatting
3. Ensure migrations are working
4. Update documentation if needed

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PDM Documentation](https://pdm.fming.dev/)
- [Docker Documentation](https://docs.docker.com/)

## 💬 Getting Help

If you encounter issues:

1. Check this setup guide
2. Review error logs: `docker compose -f docker-compose.dev.yml logs`
3. Ask in the team Slack channel
4. Create an issue in the GitHub repository

---

**Happy coding! 🚀**
