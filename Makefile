build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

migrate:
	uv run python3 manage.py migrate

start:
	uv run manage.py runserver 127.0.0.1:8000

collectstatic:
	uv run python3 manage.py collectstatic --no-input

lint:
	uv run ruff check