.PHONY: help build up down logs bash test lint format migrate clean setup \
        backend-shell frontend-shell db-reset db-migrations celery-logs

help:
	@echo "SkillSwap-Map - Development Commands"
	@echo "===================================="
	@echo ""
	@echo "Docker Commands:"
	@echo "  make build              Build Docker images"
	@echo "  make up                 Start all services"
	@echo "  make down               Stop all services"
	@echo "  make logs               View service logs"
	@echo "  make logs-backend       View backend logs"
	@echo "  make logs-frontend      View frontend logs"
	@echo ""
	@echo "Database Commands:"
	@echo "  make migrate            Run Django migrations"
	@echo "  make migrations         Create new migrations"
	@echo "  make db-reset           Reset database (WARNING: deletes all data)"
	@echo "  make db-seed            Load sample data"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test               Run all tests"
	@echo "  make test-backend       Run backend tests"
	@echo "  make test-frontend      Run frontend tests"
	@echo "  make lint               Lint all code"
	@echo "  make format             Format all code"
	@echo "  make clean              Remove temporary files"
	@echo ""
	@echo "Shell Access:"
	@echo "  make backend-shell      Access Django shell"
	@echo "  make bash-backend       Access backend container bash"
	@echo "  make bash-frontend      Access frontend container bash"
	@echo ""
	@echo "Setup:"
	@echo "  make setup              Initial setup"
	@echo "  make install-hooks      Install git hooks"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f db

logs-redis:
	docker-compose logs -f redis

logs-celery:
	docker-compose logs -f celery_worker

# Database commands
migrate:
	docker-compose exec backend python manage.py migrate

migrations:
	docker-compose exec backend python manage.py makemigrations

db-reset:
	@echo "WARNING: This will delete all data in the database!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose exec backend python manage.py flush --no-input; \
		docker-compose exec backend python manage.py migrate; \
		echo "Database reset complete"; \
	fi

db-seed:
	docker-compose exec backend python manage.py loaddata initial_data

superuser:
	docker-compose exec backend python manage.py createsuperuser

# Development commands
test:
	docker-compose exec backend python manage.py test
	docker-compose exec frontend npm test

test-backend:
	docker-compose exec backend python manage.py test

test-frontend:
	docker-compose exec frontend npm test

test-coverage:
	docker-compose exec backend coverage run --source='.' manage.py test
	docker-compose exec backend coverage report

lint:
	@echo "Linting backend..."
	docker-compose exec backend flake8 .
	@echo "Linting frontend..."
	docker-compose exec frontend npm run lint

format:
	@echo "Formatting backend..."
	docker-compose exec backend black .
	@echo "Formatting frontend..."
	docker-compose exec frontend npm run format

# Shell access
backend-shell:
	docker-compose exec backend python manage.py shell

bash-backend:
	docker-compose exec backend bash

bash-frontend:
	docker-compose exec frontend sh

bash-db:
	docker-compose exec db psql -U postgres -d skillswap

# Cleaning
clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -name ".coverage" -delete
	docker-compose exec frontend npm run clean 2>/dev/null || true

clean-volumes:
	docker-compose down -v

clean-all:
	docker-compose down -v
	docker system prune -f

# Setup
setup: build up migrate superuser
	@echo "Setup complete!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "Admin: http://localhost:8000/admin/"

# Git hooks
install-hooks:
	@echo "Installing git hooks..."
	@cp scripts/pre-commit .git/hooks/pre-commit 2>/dev/null || echo "Pre-commit hook not found"
	@chmod +x .git/hooks/pre-commit
	@echo "Git hooks installed"

# Utility commands
freeze-requirements:
	docker-compose exec backend pip freeze > backend/requirements.txt

update-requirements:
	docker-compose exec backend pip install --upgrade pip
	docker-compose exec backend pip install -r backend/requirements.txt

install-backend-deps:
	docker-compose exec backend pip install -r backend/requirements.txt

install-frontend-deps:
	docker-compose exec frontend npm install

check-health:
	@echo "Checking services health..."
	@curl -s http://localhost:8000/health && echo "✓ Backend" || echo "✗ Backend"
	@curl -s http://localhost:3000/health && echo "✓ Frontend" || echo "✗ Frontend"
	@docker-compose ps

static-files:
	docker-compose exec backend python manage.py collectstatic --noinput

collectstatic: static-files

celery-logs:
	docker-compose logs -f celery_worker

celery-beat:
	docker-compose exec celery_worker celery -A skillswap beat

# Development utilities
watch-backend:
	docker-compose exec backend python manage.py runserver_plus 0.0.0.0:8000

watch-frontend:
	docker-compose exec frontend npm run dev

dev: up logs

# Production commands
build-prod:
	docker-compose -f docker-compose.yml build

deploy:
	@echo "Deploy commands would go here"
	@echo "Implement based on your hosting platform"

# Documentation
docs:
	@echo "Opening documentation..."
	@open docs/SETUP.md || xdg-open docs/SETUP.md || echo "Please open docs/SETUP.md manually"

# Statistics
stats:
	@echo "Code Statistics"
	@echo "==============="
	@echo ""
	@echo "Backend files:"
	@find backend -name "*.py" -type f | wc -l
	@echo ""
	@echo "Frontend files:"
	@find frontend/src -name "*.jsx" -o -name "*.js" | wc -l
	@echo ""
	@echo "Total lines (backend):"
	@find backend -name "*.py" -type f -exec wc -l {} + | tail -1

.DEFAULT_GOAL := help
