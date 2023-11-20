install:
	@pip install poetry
	@poetry install

format:
	poetry run isort . --profile black
	poetry run black .

lint:
	poetry run isort --check --profile black .
	poetry run black --check .
	poetry run prospector

run:
	@poetry run python run.py