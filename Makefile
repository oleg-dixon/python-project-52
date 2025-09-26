PORT ?= 8000

install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

migrate:
	uv run manage.py migrate

migrate-postgres:
	DJANGO_ENV=production uv run manage.py migrate

check-lint:
	uv run ruff check

fix-lint:
	uv run ruff check --fix

collectstatic:
	uv run manage.py collectstatic --noinput

test:
	make migrate-postgres
	uv run pytest
