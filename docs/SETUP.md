# SkillSwap-Map Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15+ (for local development without Docker)
- Redis (for caching and messaging)

## Quick Start with Docker (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/skillswap-map.git
cd skillswap-map
```

### 2. Create Environment File
```bash
cp .env.example .env
# Edit .env with your configuration
nano .env
```

### 3. Build and Start Services
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Django backend (port 8000)
- React frontend (port 3000)
- Nginx reverse proxy (port 80)

### 4. Create Superuser
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 5. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/schema/swagger/
- Admin Panel: http://localhost:8000/admin/

## Local Development Setup (Without Docker)

### Backend Setup

1. **Clone repository**
```bash
git clone https://github.com/yourusername/skillswap-map.git
cd skillswap-map/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
   - Create PostgreSQL database and user
   - Update database credentials in `.env`

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd skillswap-map/frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create `.env.local`**
```bash
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=SkillSwap-Map
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

## Database Setup

### With Docker
The database is automatically initialized when you run `docker-compose up`.

### Without Docker (Local Development)

1. **Create database**
```bash
createdb skillswap
createuser skillswap_user
```

2. **Grant privileges**
```bash
psql -U postgres -d skillswap -c "ALTER ROLE skillswap_user WITH PASSWORD 'password';"
psql -U postgres -d skillswap -c "GRANT ALL PRIVILEGES ON DATABASE skillswap TO skillswap_user;"
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Load initial data (optional)**
```bash
python manage.py loaddata initial_data
```

## Running Tests

### Backend Tests
```bash
# With Docker
docker-compose exec backend python manage.py test

# Local development
python manage.py test
```

### Frontend Tests
```bash
# With Docker
docker-compose exec frontend npm test

# Local development
npm test
```

## Code Quality

### Backend

**Format code with Black**
```bash
docker-compose exec backend black .
# or locally
black .
```

**Lint with Flake8**
```bash
docker-compose exec backend flake8 .
# or locally
flake8 .
```

**Run linting and tests**
```bash
docker-compose exec backend bash -c "flake8 . && python manage.py test"
```

### Frontend

**Lint code**
```bash
docker-compose exec frontend npm run lint
# or locally
npm run lint
```

**Format code with Prettier**
```bash
docker-compose exec frontend npm run format
# or locally
npm run format
```

## Managing Dependencies

### Backend

**Add new package**
```bash
pip install package_name
pip freeze > requirements.txt
```

### Frontend

**Add new package**
```bash
npm install package_name
```

## Database Migrations

### Create migration after model changes
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Specific app migration
```bash
python manage.py migrate users
```

### Revert migrations
```bash
python manage.py migrate users zero  # Revert all
python manage.py migrate users 0005  # Revert to specific
```

## Static Files

### Collect static files
```bash
python manage.py collectstatic --noinput
```

### Development static files
In development mode, Django automatically serves static files. Ensure `DEBUG=True` in settings.

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find and kill process on port
lsof -i :8000
kill -9 <PID>
```

**Database connection error**
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -l`

**Import errors in Django**
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`
- Reinstall dependencies: `pip install -r requirements.txt`

**Node modules issues**
- Clear cache: `npm cache clean --force`
- Delete node_modules: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`

**Redis connection error**
- Ensure Redis is running: `redis-cli ping`
- Check Redis connection in settings

## Next Steps

1. Read the [API Documentation](./docs/API.md)
2. Review [Contributing Guidelines](./CONTRIBUTING.md)
3. Check out [Deployment Guide](./docs/DEPLOYMENT.md)

## Support

- 📧 Email: support@skillswap-map.com
- 💬 GitHub Issues: Create an issue for bugs or features
- 🐛 Report Security Issues: security@skillswap-map.com
