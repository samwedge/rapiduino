test:
	poetry run pytest tests
	poetry run mypy rapiduino
	poetry run mypy tests
	poetry run flake8 rapiduino
	poetry run flake8 tests
	poetry run black --check --diff --color rapiduino
	poetry run black --check --diff --color tests
	poetry run isort --check --diff --color rapiduino
	poetry run isort --check --diff --color tests

fix:
	poetry run black rapiduino
	poetry run black tests
	poetry run isort rapiduino
	poetry run isort tests