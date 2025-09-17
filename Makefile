PORT ?= 8000

install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

dev:
	uv run manage.py runserver

migrate:
	uv run manage.py migrate

tests:
	uv run manage.py test

check-lint:
	uv run ruff check

fix-lint:
	uv run ruff check --fix

rmcache:
	find . -name "__pycache__" -exec rm -rf {} +

collectstatic:
	uv run manage.py collectstatic --noinput