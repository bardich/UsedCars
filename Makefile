# AutoMaroc - Makefile for development commands

.PHONY: help venv install dev tailwind migrate run docker-up docker-down test clean

# Colors
BLUE=\033[0;34m
GREEN=\033[0;32m
NC=\033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)AutoMaroc - Available Commands$(NC)"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-15s$(NC) %s\n", $$1, $$2}'

venv: ## Create virtual environment
	@echo "Creating virtual environment..."
	python3 -m venv venv

install: ## Install all dependencies
	@echo "Installing Python dependencies..."
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	@echo "Installing Tailwind dependencies..."
	cd theme/static_src && npm install

setup: venv install ## Full setup (venv + install)
	@echo "$(GREEN)Setup complete! Run 'make run' to start developing.$(NC)"

dev: ## Run Django development server
	venv/bin/python manage.py runserver

tailwind: ## Run Tailwind CSS in watch mode
	venv/bin/python manage.py tailwind start

migrate: ## Run database migrations
	venv/bin/python manage.py migrate

makemigrations: ## Create new migrations
	venv/bin/python manage.py makemigrations

shell: ## Open Django shell
	venv/bin/python manage.py shell

createsuperuser: ## Create admin superuser
	venv/bin/python manage.py createsuperuser

collectstatic: ## Collect static files
	venv/bin/python manage.py collectstatic --noinput

test: ## Run tests
	venv/bin/python manage.py test

docker-up: ## Start Docker containers
	docker-compose up -d --build

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

run: ## Start both Django and Tailwind (requires tmux or run in separate terminals)
	@echo "Starting Django development server..."
	@echo "Run 'make tailwind' in another terminal for CSS watch mode"
	venv/bin/python manage.py runserver

full-run: ## Run both servers (Django in background, Tailwind in foreground)
	@echo "Starting Django server in background..."
	venv/bin/python manage.py runserver &
	@echo "Starting Tailwind CSS watch mode..."
	venv/bin/python manage.py tailwind start
