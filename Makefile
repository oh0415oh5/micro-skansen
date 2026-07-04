.PHONY: install run test lint

install:
	pip install -r requirements.txt

run:
	python3 src/server.py

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
