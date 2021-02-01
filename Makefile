test:
	poetry run coverage run --source=rapiduino -m pytest tests
	poetry run mypy rapiduino tests
	poetry run flake8 rapiduino tests
	poetry run black --check --diff --color rapiduino tests
	poetry run isort --check --diff --color rapiduino tests
	poetry run coverage html
	poetry run coverage report

fix:
	poetry run black rapiduino
	poetry run black tests
	poetry run isort rapiduino
	poetry run isort tests