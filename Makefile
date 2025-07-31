install:
	uv sync

lint:
	uv run ruff check

fix:
	uv run ruff check --fix

dev:
	uv run flask --debug --app page_analyzer:app run
