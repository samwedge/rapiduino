test:
	poetry run pytest tests
	poetry run mypy rapiduino
	poetry run flake8 rapiduino
	poetry run black --check --diff --color rapiduino
	poetry run isort --check --diff --color rapiduino

fix:
	poetry run black rapiduino
	poetry run isort rapiduino