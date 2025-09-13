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

collectstatic:
	uv run manage.py collectstatic --noinput