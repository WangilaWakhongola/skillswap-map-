# Quick Start Guide - SkillSwap-Map

## 🚀 30-Second Setup

```bash
# 1. Clone and navigate
git clone <repo-url>
cd skillswap-map

# 2. Create environment file
cp .env.example .env

# 3. Start everything
docker-compose up --build

# 4. Create superuser (in another terminal)
docker-compose exec backend python manage.py createsuperuser

# Done! 🎉
```

## 📱 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | User interface |
| **Backend** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/api/schema/swagger/ | Interactive API docs |
| **Admin** | http://localhost:8000/admin/ | Django admin panel |
| **Database** | localhost:5432 | PostgreSQL |
| **Cache** | localhost:6379 | Redis |

## 💻 Common Commands

### Docker
```bash
make up                    # Start all services
make down                  # Stop all services
make logs-backend         # View backend logs
make bash-backend         # Shell into backend
```

### Database
```bash
make migrate              # Run migrations
make migrations           # Create new migrations
make db-reset            # Reset database (⚠️ deletes data)
make superuser           # Create superuser
```

### Development
```bash
make test               # Run all tests
make lint               # Check code style
make format             # Auto-format code
make clean              # Clean temporary files
```

### Local Development (Without Docker)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# In another terminal:
cd frontend
npm install
npm run dev
```

## 📂 Project Structure Quick Reference

```
skillswap-map/
├── backend/              # Django REST API
│   ├── apps/            # Django apps (users, skills, etc.)
│   ├── skillswap/       # Project settings
│   └── manage.py
├── frontend/            # React SPA
│   ├── src/
│   ├── public/
│   └── package.json
├── docker/              # Docker configs
├── docs/                # Documentation
├── .env.example         # Environment template
├── docker-compose.yml   # Docker Compose config
└── Makefile            # Development commands
```

## 🔧 Development Workflow

### 1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make changes
```bash
# Backend: Edit code in backend/apps/
# Frontend: Edit code in frontend/src/
```

### 3. Test locally
```bash
make test       # Run tests
make lint       # Check style
make format     # Format code
```

### 4. Commit changes
```bash
git add .
git commit -m "feat(component): Add feature description"
```

### 5. Push and create PR
```bash
git push origin feature/your-feature-name
# Then create PR on GitHub
```

## 🐛 Troubleshooting

### Port already in use
```bash
# Find process using port
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Database issues
```bash
# Reset database
make db-reset

# Check database connection
docker-compose logs db
```

### Docker issues
```bash
# Rebuild everything
docker-compose down -v
docker-compose up --build

# Check all services
docker-compose ps
```

### Frontend issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 📚 Documentation

- [Full Setup Guide](./docs/SETUP.md)
- [API Documentation](./docs/API.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## 🆘 Getting Help

- 📖 Read the docs
- 🐛 Check existing issues
- 💬 Open a GitHub discussion
- 📧 Email: support@skillswap-map.com

## 🔐 Important Notes

⚠️ **Never commit `.env` file** - Use `.env.example` as template

⚠️ **Don't push to main** - Always use feature branches

⚠️ **Keep dependencies updated** - Regularly update packages

✅ **Write tests** - Aim for >80% coverage

✅ **Write clean code** - Follow PEP8/Prettier

✅ **Document changes** - Update relevant docs

## 🎯 Next Steps

1. ✅ Set up local environment
2. ✅ Read the contributing guidelines
3. ✅ Find an issue to work on
4. ✅ Create a feature branch
5. ✅ Submit a PR

Happy coding! 🎉
