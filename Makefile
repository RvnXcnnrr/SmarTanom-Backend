.PHONY: help install install-dev migrate seed test clean lint format run
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "SmarTanom Backend Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

migrate: ## Run database migrations
	python manage.py migrate

seed: ## Load sample data
	python manage.py seed_data

test: ## Run tests
	python manage.py test

test-coverage: ## Run tests with coverage
	coverage run --source='.' manage.py test
	coverage report
	coverage html

clean: ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -f .coverage

lint: ## Run code linting
	flake8 .
	black --check .
	isort --check-only .

format: ## Format code
	black .
	isort .

run: ## Run development server
	python manage.py runserver

run-prod: ## Run production server with Daphne
	daphne -b 0.0.0.0 -p 8000 smartanom_backend.asgi:application

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

backup: ## Create backup (Linux/Mac only)
	./scripts/backup.sh

setup: ## Setup development environment
	@echo "Setting up development environment..."
	python -m venv .venv
	@echo "Virtual environment created. Please activate it and run 'make install-dev'"

shell: ## Open Django shell
	python manage.py shell

dbshell: ## Open database shell
	python manage.py dbshell

createsuperuser: ## Create superuser
	python manage.py create_superuser

logs: ## Show application logs (for production)
	tail -f /var/log/supervisor/smartanom.log

restart: ## Restart application (for production)
	sudo supervisorctl restart smartanom
